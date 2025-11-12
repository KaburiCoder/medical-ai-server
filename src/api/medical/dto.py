from typing import Literal
from pydantic import BaseModel, EmailStr, Field
from pydantic.alias_generators import to_camel


class SummarizeProgressNoteRequestDto(BaseModel):
  model_config = {
      "alias_generator": to_camel
  }

  chart: str = Field(..., min_length=1, max_length=50, description="차트번호")
  symd: str = Field(..., min_length=8, max_length=8, description="시작일자 (YYYYMMDD)")
  eymd: str = Field(..., min_length=8, max_length=8, description="종료일자 (YYYYMMDD)")  

class SummarizeProgressNoteResponseDto(BaseModel):
  model_config = {"alias_generator": to_camel, "populate_by_name": True}

  message_test: str = Field(..., description="응답 메시지")
  name_test: str = Field(..., description="실명")
  email: EmailStr = Field(..., description="이메일 주소")
  role: Literal["patient", "doctor", "admin"] = Field(..., description="역할")
