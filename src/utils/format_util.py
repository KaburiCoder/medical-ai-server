from datetime import datetime


def ymd_to_date(ymd: str) -> str:
  dt = datetime.strptime(ymd, "%Y%m%d")
  return dt.strftime("%Y-%m-%d")


def hm_to_time(hm: str | None) -> str:
  if hm is None:
    return ""
  try:
    dt = datetime.strptime(hm, "%H%M%S")
  except ValueError:
    return ""
  return dt.strftime("%H:%M:%S")
