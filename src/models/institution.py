from datetime import datetime, timezone

from sqlalchemy import Boolean, CheckConstraint, DateTime, Index, String, text
from sqlalchemy.orm import Mapped, mapped_column

from src.db.base import Base

class Institution(Base):
    __tablename__ = "institutions"

    __table_args__ = (
        CheckConstraint(
            "institution_type IN ('ubs', 'caf', 'state', 'municipality', 'other')",
            name="check_institution_type",
        ),

        Index(
            "uq_institution_local_stock_owner",
            "is_local_stock_owner",
            unique=True,
            sqlite_where=text("is_local_stock_owner = 1")
        )
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    name: Mapped[str] = mapped_column(String, nullable=False)

    institution_type: Mapped[str] = mapped_column(String, nullable=False)

    is_local_stock_owner: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc)
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc)
    )