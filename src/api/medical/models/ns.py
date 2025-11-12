from typing import Iterable
from pydantic import BaseModel, Field
 
from src.models.ns import Ns


class NsModel(BaseModel):
  date: str
  time: str
  nursing_diagnosis: str = Field(..., description="간호 문제")
  nursing_intervention: str = Field(..., description="간호 처치")

class NsModels(list[NsModel]):
  def add_from_nss(self, nss: Iterable[Ns]) -> None:
    for ns in nss:
      ns_model = NsModel(
          date=ns.ymd,
          time=ns.time,
          nursing_diagnosis=ns.neyong1 or "",
          nursing_intervention=ns.neyong2 or ""
      )
      self.append(ns_model)

  def get_markdown_table(self):
    import pandas as pd
    pd_ns = pd.DataFrame([ns_model.model_dump() for ns_model in self])
    pd_ns = pd_ns.rename(columns={
        "date": "작성일자",
        "time": "작성시간",
        "nursing_diagnosis": "간호 문제",
        "nursing_intervention": "간호 처치"
    })
    return pd_ns.to_markdown(index=False)