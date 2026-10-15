"""Server-only conservative allocation ledger; actual supplier fees stay unknown."""
from datetime import datetime
from decimal import Decimal

from sqlalchemy import DateTime, Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class WebModelCall(Base):
    __tablename__ = "web_model_calls"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    provider: Mapped[str] = mapped_column(String(100), nullable=False)
    method: Mapped[str] = mapped_column(String(100), nullable=False)
    state: Mapped[str] = mapped_column(String(40), nullable=False)
    reserved_cny: Mapped[Decimal] = mapped_column(Numeric(12, 6), nullable=False)
    settled_cny: Mapped[Decimal | None] = mapped_column(Numeric(12, 6), nullable=True)
    actual_cost_cny: Mapped[Decimal | None] = mapped_column(Numeric(12, 6), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, index=True)
    finished_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
