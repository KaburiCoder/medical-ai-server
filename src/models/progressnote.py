from typing import Optional
from sqlalchemy import String, Integer, BigInteger, Text, LargeBinary, CHAR, VARCHAR
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
  pass


class ProgressNote(Base):
  __tablename__ = "progressnote"

  auto: Mapped[int] = mapped_column(
      "prog_auto", BigInteger, primary_key=True, autoincrement=True)
  gubun: Mapped[str] = mapped_column("prog_gubun", CHAR(2), nullable=False)
  saup: Mapped[str] = mapped_column("prog_saup", VARCHAR(2), nullable=False)
  weibgu: Mapped[str] = mapped_column("prog_weibgu", CHAR(1), nullable=False)
  chart: Mapped[str] = mapped_column("prog_chart", VARCHAR(8), nullable=False)
  yuhyung: Mapped[str] = mapped_column(
      "prog_yuhyung", VARCHAR(2), nullable=False)
  jinchal: Mapped[str] = mapped_column(
      "prog_jinchal", VARCHAR(2), nullable=False)
  ymd: Mapped[str] = mapped_column("prog_ymd", VARCHAR(8), nullable=False)
  ibymd: Mapped[str] = mapped_column("prog_ibymd", VARCHAR(8), nullable=False)
  dup: Mapped[int] = mapped_column("prog_dup", Integer, nullable=False)
  time: Mapped[Optional[str]] = mapped_column(
      "prog_time", VARCHAR(6), default="")
  progress: Mapped[Optional[str]] = mapped_column("prog_progress", Text)
  rtf: Mapped[Optional[str]] = mapped_column("prog_rtf", Text)
  username: Mapped[Optional[str]] = mapped_column(
      "prog_username", VARCHAR(20), default="")
  etc1: Mapped[Optional[str]] = mapped_column(
      "prog_etc1", VARCHAR(255), default="")
  etc2: Mapped[Optional[str]] = mapped_column(
      "prog_etc2", VARCHAR(255), default="")
  etc3: Mapped[Optional[str]] = mapped_column(
      "prog_etc3", VARCHAR(255), default="")
  etc4: Mapped[Optional[str]] = mapped_column(
      "prog_etc4", VARCHAR(255), default="")
  etc5: Mapped[Optional[str]] = mapped_column(
      "prog_etc5", VARCHAR(255), default="")
  dc: Mapped[str] = mapped_column(
      "prog_dc", CHAR(1), nullable=False, default="0")
  indate: Mapped[Optional[str]] = mapped_column(
      "prog_indate", VARCHAR(20), default="")
  update: Mapped[Optional[str]] = mapped_column(
      "prog_update", VARCHAR(255), default="")
  dcdate: Mapped[Optional[str]] = mapped_column(
      "prog_dcdate", VARCHAR(255), default="")
  inuser: Mapped[Optional[str]] = mapped_column(
      "prog_inuser", VARCHAR(20), default="")
  upuser: Mapped[Optional[str]] = mapped_column(
      "prog_upuser", VARCHAR(20), default="")
  dcuser: Mapped[Optional[str]] = mapped_column(
      "prog_dcuser", VARCHAR(20), default="")
  insign: Mapped[Optional[bytes]] = mapped_column("prog_insign", LargeBinary)
  upsign: Mapped[Optional[bytes]] = mapped_column("prog_upsign", LargeBinary)
  dcsign: Mapped[Optional[bytes]] = mapped_column("prog_dcsign", LargeBinary)
  incert: Mapped[Optional[str]] = mapped_column("prog_incert", Text)
  upcert: Mapped[Optional[str]] = mapped_column("prog_upcert", Text)
  dccert: Mapped[Optional[str]] = mapped_column("prog_dccert", Text)
  etc6: Mapped[Optional[str]] = mapped_column(
      "prog_etc6", VARCHAR(255), default="")
  etc7: Mapped[Optional[str]] = mapped_column(
      "prog_etc7", VARCHAR(255), default="")
  etc8: Mapped[Optional[str]] = mapped_column(
      "prog_etc8", VARCHAR(255), default="")
  etc9: Mapped[Optional[str]] = mapped_column(
      "prog_etc9", VARCHAR(255), default="")
  etc10: Mapped[Optional[str]] = mapped_column(
      "prog_etc10", VARCHAR(255), default="")
  soapuse: Mapped[str] = mapped_column("prog_soapuse", CHAR(1), nullable=False)
  s: Mapped[Optional[str]] = mapped_column("prog_s", Text)
  srtf: Mapped[Optional[str]] = mapped_column("prog_srtf", Text)
  o: Mapped[Optional[str]] = mapped_column("prog_o", Text)
  ortf: Mapped[Optional[str]] = mapped_column("prog_ortf", Text)
  a: Mapped[Optional[str]] = mapped_column("prog_a", Text)
  artf: Mapped[Optional[str]] = mapped_column("prog_artf", Text)
  p: Mapped[Optional[str]] = mapped_column("prog_p", Text)
  prtf: Mapped[Optional[str]] = mapped_column("prog_prtf", Text)
