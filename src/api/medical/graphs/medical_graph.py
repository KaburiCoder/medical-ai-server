from typing import Sequence, TypedDict

from langchain.agents import create_agent
from langchain.messages import HumanMessage
from langgraph.func import END, START
from langgraph.graph import StateGraph
from langgraph.pregel import Pregel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import load_only

from src.api.medical.dto.progress_note_dto import ProgressNoteResult
from src.api.medical.dto.vs_ns_dto import VsNsSummaryResult
from src.api.medical.models.ns import NsModels
from src.api.medical.models.vs import VsModel, VsModels
from src.api.medical.service import ProgressNote
from src.constants import llm_models
from src.models.ns import Ns
from src.models.vs import Vs
from src.utils.format_util import hm_to_time, ymd_to_date


class State(TypedDict, total=False):
  input: 'StateInput'
  session: AsyncSession
  db_data: 'DBData'
  progress_notes_summary: ProgressNoteResult
  vs_ns_summary: VsNsSummaryResult


class StateInput(TypedDict):
  chart: str
  symd: str
  eymd: str


class DBData(TypedDict, total=False):
  progressnotes: Sequence[ProgressNote]
  vss: Sequence[Vs]
  nss: Sequence[Ns]


builder = StateGraph[State](State)


async def read_db_datas(state: State) -> State:
  input = state.get('input') or {}
  session = state.get('session')
  if session is None:
    raise ValueError("AsyncSession is required in state")

  # progressnote 조회
  result = await session.scalars(
      select(ProgressNote)
      .where((ProgressNote.gubun == 'A')
             & (ProgressNote.chart == input['chart'])
             & (ProgressNote.ymd >= input['symd'])
             & (ProgressNote.ymd <= input['eymd']))
      .order_by(ProgressNote.ymd.desc())
      .offset(0)
      .limit(30)
      .options(load_only(ProgressNote.auto, ProgressNote.ymd, ProgressNote.time, ProgressNote.progress))
  )

  progressnotes = result.all()

  # 간호기록 조회
  query = select(Ns) \
      .where(Ns.chart == input['chart'],
             Ns.ymd.between(input['symd'], input['eymd']),
             Ns.dc != "1") \
      .order_by(Ns.ymd.desc()) \
      .options(load_only(
          Ns.auto,
          Ns.ymd,
          Ns.time,
          Ns.neyong1,
          Ns.neyong2
      ))

  result = await session.scalars(query)
  nss = result.all()

  # 바이탈사인 조회
  query = select(Vs) \
      .where(Vs.chart == input['chart'],
             Vs.ymd.between(input['symd'], input['eymd']),
             Vs.dc != "1") \
      .order_by(Vs.ymd.desc()) \
      .options(load_only(
          Vs.auto,
          Vs.ymd,
          Vs.hulap2,
          Vs.hulap1,
          Vs.maekbak,
          Vs.weight,
          Vs.cheon,
          Vs.hohup,
          Vs.spo2,
      ))
  result = await session.scalars(query)
  vss = result.all()
  return {"db_data": {"progressnotes": progressnotes, "nss": nss, "vss": vss}, }


async def create_progressnote_summary(state: State) -> State:
  histories = [
      f"**일시**: {ymd_to_date(r.ymd)} {hm_to_time(r.time)}\n**경과기록**: {r.progress}"
      for r in state.get('db_data', {}).get('progressnotes', [])
  ]
  agent = create_agent(
      model=llm_models.gemini_flash_lite,
      response_format=ProgressNoteResult,
      system_prompt="당신은 의사입니다. 환자의 경과기록을 가지고 필요한 정보를 입력합니다.")

  progressnote_history_text = "\n\n---\n".join(histories)
  response = agent.invoke({
      "messages": [HumanMessage(content=progressnote_history_text)]
  })

  result: ProgressNoteResult = response['structured_response']
  return {"progress_notes_summary": result}


async def create_ns_vs_summary(state: State) -> State:
  # ? === vs ===
  vss = state.get('db_data', {}).get('vss', [])
  recent_vs = VsModel()
  recent_vs.add_recently_from_vss(vss)

  vs_list = VsModels()
  vs_list.add_recently_from_vss(vss)
  vs_list_md = vs_list.get_markdown_table()

  # ? === ns ===
  nss = state.get('db_data', {}).get('nss', [])
  ns_list = NsModels()
  ns_list.add_from_nss(nss)
  ns_list_md = ns_list.get_markdown_table()

  agent = create_agent(
      model=llm_models.gemini_flash,
      response_format=VsNsSummaryResult,
      system_prompt="""당신은 의사입니다.
환자의 활력징후와 간호기록을 다음 내용을 작성합니다.
- 바이탈 사인 종합 요약 정보
- 간호기록 종합 요약 정보
- 주의사항
- 의료진 임상 의견
- 전체 임상 평가
- 주요 소견

활력징후와 간호기록은 각각 마크다운 표 형식으로 제공됩니다.""")

  response = await agent.ainvoke({
      "messages": [HumanMessage(content=f"""# 활력징후 기록
{vs_list_md}

---
# 간호기록
{ns_list_md}""")]
  })

  result : VsNsSummaryResult = response['structured_response']
  return {"vs_ns_summary": result}
  return state

# ! === Define the workflow structure === #
builder.add_node('read_db_datas', read_db_datas)
builder.add_node('create_progressnote_summary', create_progressnote_summary)
builder.add_node('create_ns_vs_summary', create_ns_vs_summary)

builder.add_edge(START, 'read_db_datas')
builder.add_edge('read_db_datas', 'create_progressnote_summary')
builder.add_edge('read_db_datas', 'create_ns_vs_summary')

builder.add_edge('create_progressnote_summary', END)
builder.add_edge('create_ns_vs_summary', END)
# ! === Add nodes to the workflow === #
workflow = builder.compile()
