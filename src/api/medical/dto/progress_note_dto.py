from typing import Optional
from pydantic import BaseModel,  Field
from pydantic.alias_generators import to_camel
 
from src.api.medical.dto.base_dto import CarmelModel, ChartTermRequestDto


class SOAP(BaseModel):
  subjective: Optional[str] = Field(None, description="환자의 주관적 증상 및 호소")
  objective: Optional[str] = Field(None, description="의사의 객관적 관찰 및 검사 결과")
  assessment: Optional[str] = Field(None, description="의사의 평가 및 판단")
  plan: Optional[str] = Field(None, description="치료 및 추후 계획")


class ProgressNoteResult(CarmelModel):
  summary: str = Field(..., description="경과기록 전체 요약")
  main_diagnosis: list[str] = Field(..., description="주진단명 또는 주요 진단 코드")
  chief_complaint: Optional[str] = Field(None, description="주요 증상 및 호소")
  soap: SOAP = Field(..., description="SOAP 및 주진단 정보")
  precautions: str = Field(
      ..., description="AI가 도출한 주의 사항 없을 시 빈문자열")
  start_date: str = Field(...,
                          description="요약에 사용된 처음 일시(yyyy-MM-dd HH:mm:ss)")
  end_date: str = Field(
      ..., description="요약에 사용된 마지막 일시(yyyy-MM-dd HH:mm:ss)")


class SummarizeProgressNoteRequestDto(ChartTermRequestDto):
  pass
