from src.api.medical.dto.base_dto import CarmelModel
from src.api.medical.dto.progress_note_dto import ProgressNoteResult
from src.api.medical.dto.vs_ns_dto import VsNsSummaryResult
from pydantic import Field


class AllResult (CarmelModel):
  progress_notes_summary: ProgressNoteResult = Field(
      ..., description="경과기록 요약 결과")
  vs_ns_summary: VsNsSummaryResult = Field(
      ..., description="Vital Sign 및 간호기록 요약 결과")
