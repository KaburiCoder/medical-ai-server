from pydantic import BaseModel, Field
from pydantic.alias_generators import to_camel


class CarmelModel(BaseModel):
  model_config = {"alias_generator": to_camel, "populate_by_name": True}


class ChartTermRequestDto(CarmelModel):
  model_config = {
      "alias_generator": to_camel
  }

  chart: str = Field(
      ...,
      min_length=1,
      max_length=50,
      description="차트번호",
      examples=["00000795"]
  )
  symd: str = Field(
      ...,
      min_length=8,
      max_length=8,
      description="시작일자 (YYYYMMDD)",
      examples=["20240601"]
  )
  eymd: str = Field(
      ...,
      min_length=8,
      max_length=8,
      description="종료일자 (YYYYMMDD)",
      examples=["20251101"]
  )
