from fastapi import APIRouter

from src.api.deps import SessionDep

router = APIRouter(prefix="/medical", tags=["medical"])


@router.get("/info")
async def get_medical_info(session: SessionDep):
  return {"message": "의료 정보 엔드포인트"}
