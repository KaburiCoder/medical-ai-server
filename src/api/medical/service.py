from typing import Annotated
from fastapi import Depends
from langchain.agents import create_agent
from langchain.messages import HumanMessage
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import load_only
from src.api.deps import SessionDep
from src.api.medical.dto.base_dto import ChartTermRequestDto
from src.api.medical.dto.progress_note_dto import ProgressNoteResult, SummarizeProgressNoteRequestDto
from src.api.medical.dto.vs_ns_dto import VsNsSummaryResult
from src.api.medical.models.ns import NsModels
from src.api.medical.models.vs import VsModel, VsModels
from src.constants import llm_models
from src.models.ns import Ns
from src.models.progressnote import ProgressNote
from src.models.vs import Vs
from src.utils.format_util import hm_to_time, ymd_to_date


class MedicalService:
  """의료 정보 관련 비즈니스 로직을 담당하는 서비스"""

  def __init__(self, session: AsyncSession):
    self.session = session

  async def summarize_progress_note(self, dto: SummarizeProgressNoteRequestDto):
    histories: list[str] = []
    result = await self.session.scalars(
        select(ProgressNote)
        .where((ProgressNote.gubun == 'A')
               & (ProgressNote.chart == dto.chart)
               & (ProgressNote.ymd >= dto.symd)
               & (ProgressNote.ymd <= dto.eymd))
        .order_by(ProgressNote.ymd.desc())
        .offset(0)
        .limit(30)
        .options(load_only(ProgressNote.auto, ProgressNote.ymd, ProgressNote.time, ProgressNote.progress))
    )

    histories.extend([
        f"**일시**: {ymd_to_date(r.ymd)} {hm_to_time(r.time)}\n**경과기록**: {r.progress}"
        for r in result
    ])

    agent = create_agent(
        model=llm_models.gemini_flash_lite,
        response_format=ProgressNoteResult,
        system_prompt="당신은 의사입니다. 환자의 경과기록을 가지고 필요한 정보를 입력합니다.")

    progressnote_history_text = "\n\n---\n".join(histories)
    response = agent.invoke({
        "messages": [HumanMessage(content=progressnote_history_text)]
    })

    return response['structured_response']

  async def vs_summary(self, dto: ChartTermRequestDto):
    query = select(Vs) \
        .where(Vs.chart == dto.chart,
               Vs.ymd.between(dto.symd, dto.eymd),
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
    result = await self.session.scalars(query)
    vs_all = result.all()

    recent_vs = VsModel()
    recent_vs.add_recently_from_vss(vs_all)

    vs_list = VsModels()
    vs_list.add_recently_from_vss(vs_all)
    vs_list_md = vs_list.get_markdown_table()

    # ns    
    query = select(Ns) \
        .where(Ns.chart == dto.chart,
               Ns.ymd.between(dto.symd, dto.eymd),
               Ns.dc != "1") \
        .order_by(Ns.ymd.desc()) \
        .options(load_only(
            Ns.auto,
            Ns.ymd,
            Ns.time,
            Ns.neyong1,
            Ns.neyong2
        ))

    result = await self.session.scalars(query)

    ns_list = NsModels()
    ns_list.add_from_nss(result)
    ns_list_md = ns_list.get_markdown_table()

    # agent

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

    return response['structured_response']
    # return recent_vs


def get_medical_service(session: SessionDep) -> MedicalService:
  return MedicalService(session)


MedicalServiceDep = Annotated[MedicalService, Depends(get_medical_service)]
