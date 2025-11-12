from typing import Optional
from sqlalchemy import String, Integer, BigInteger, Text, LargeBinary, CHAR, VARCHAR
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
  pass


class Ns(Base):
  __tablename__ = "ns"

  auto: Mapped[int] = mapped_column(
      "ns_auto", BigInteger, primary_key=True, autoincrement=True)
  saup: Mapped[str] = mapped_column("ns_saup", VARCHAR(2), nullable=False)
  chart: Mapped[str] = mapped_column("ns_chart", VARCHAR(8), nullable=False)
  ibymd: Mapped[str] = mapped_column("ns_ibymd", VARCHAR(8), nullable=False)
  ymd: Mapped[str] = mapped_column("ns_ymd", VARCHAR(8), nullable=False)
  dup: Mapped[int] = mapped_column("ns_dup", Integer, nullable=False)
  time: Mapped[str] = mapped_column("ns_time", VARCHAR(8), nullable=False)
  teymd: Mapped[Optional[str]] = mapped_column(
      "ns_teymd", VARCHAR(8), default="")
  yuhyung: Mapped[Optional[str]] = mapped_column(
      "ns_yuhyung", VARCHAR(2), default="")
  bscode: Mapped[Optional[str]] = mapped_column(
      "ns_bscode", VARCHAR(9), default="")
  jinchal: Mapped[Optional[str]] = mapped_column(
      "ns_jinchal", VARCHAR(2), default="")
  suname: Mapped[Optional[str]] = mapped_column(
      "ns_suname", VARCHAR(50), default="")
  jumin: Mapped[Optional[str]] = mapped_column(
      "ns_jumin", VARCHAR(48), default="")
  nurse: Mapped[Optional[str]] = mapped_column(
      "ns_nurse", VARCHAR(10), default="")
  weymd: Mapped[Optional[str]] = mapped_column(
      "ns_weymd", VARCHAR(8), default="")
  neyong1: Mapped[Optional[str]] = mapped_column("ns_neyong1", Text)
  neyong2: Mapped[Optional[str]] = mapped_column("ns_neyong2", Text)
  username: Mapped[Optional[str]] = mapped_column(
      "ns_username", VARCHAR(20), default="")
  ntpsauto: Mapped[Optional[int]] = mapped_column(
      "ns_ntpsauto", BigInteger, default=0)
  etc1: Mapped[Optional[str]] = mapped_column(
      "ns_etc1", VARCHAR(10), default="")
  etc2: Mapped[Optional[str]] = mapped_column(
      "ns_etc2", VARCHAR(20), default="")
  etc3: Mapped[Optional[str]] = mapped_column(
      "ns_etc3", VARCHAR(5), default="0")
  etc4: Mapped[Optional[str]] = mapped_column(
      "ns_etc4", VARCHAR(255), default="")
  etc5: Mapped[Optional[str]] = mapped_column(
      "ns_etc5", VARCHAR(255), default="")
  dc: Mapped[str] = mapped_column(
      "ns_dc", CHAR(1), nullable=False, default="0")
  neyong1rtf: Mapped[Optional[str]] = mapped_column("ns_neyong1rtf", Text)
  neyong2rtf: Mapped[Optional[str]] = mapped_column("ns_neyong2rtf", Text)
  indate: Mapped[Optional[str]] = mapped_column(
      "ns_indate", VARCHAR(20), default="")
  update: Mapped[Optional[str]] = mapped_column(
      "ns_update", VARCHAR(20), default="")
  dcdate: Mapped[Optional[str]] = mapped_column(
      "ns_dcdate", VARCHAR(20), default="")
  upuser: Mapped[Optional[str]] = mapped_column(
      "ns_upuser", VARCHAR(20), default="")
  dcuser: Mapped[Optional[str]] = mapped_column(
      "ns_dcuser", VARCHAR(20), default="")
  insign: Mapped[Optional[bytes]] = mapped_column("ns_insign", LargeBinary)
  upsign: Mapped[Optional[bytes]] = mapped_column("ns_upsign", LargeBinary)
  dcsign: Mapped[Optional[bytes]] = mapped_column("ns_dcsign", LargeBinary)
  incert: Mapped[Optional[str]] = mapped_column("ns_incert", Text)
  upcert: Mapped[Optional[str]] = mapped_column("ns_upcert", Text)
  dccert: Mapped[Optional[str]] = mapped_column("ns_dccert", Text)
  etc6: Mapped[Optional[str]] = mapped_column(
      "ns_etc6", VARCHAR(255), default="")
  etc7: Mapped[Optional[str]] = mapped_column(
      "ns_etc7", VARCHAR(255), default="")
  etc8: Mapped[Optional[str]] = mapped_column(
      "ns_etc8", VARCHAR(255), default="")
  etc9: Mapped[Optional[str]] = mapped_column(
      "ns_etc9", VARCHAR(255), default="")
  etc10: Mapped[Optional[str]] = mapped_column(
      "ns_etc10", VARCHAR(255), default="")
  shift: Mapped[Optional[str]] = mapped_column(
      "ns_shift", VARCHAR(1), default="D")
