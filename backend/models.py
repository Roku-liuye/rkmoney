from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey, Index
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base


class Asset(Base):
    __tablename__ = "assets"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    type = Column(String, nullable=True)
    type_icon = Column(String, nullable=True)
    amount = Column(Float)
    purchase_date = Column(String)
    sold_date = Column(String, nullable=True)
    sold_price = Column(Float, default=0.0)
    daily_value = Column(Float, default=0.0)
    created_at = Column(String, default=datetime.utcnow().isoformat())
    updated_at = Column(String, default=datetime.utcnow().isoformat())

    prices = relationship("PriceRecord", back_populates="asset", cascade="all, delete-orphan")


class PriceRecord(Base):
    __tablename__ = "price_records"

    id = Column(Integer, primary_key=True, index=True)
    asset_id = Column(Integer, ForeignKey("assets.id", ondelete="CASCADE"), index=True)
    price = Column(Float)
    date = Column(String, index=True)
    created_at = Column(String, default=datetime.utcnow().isoformat())
    updated_at = Column(String, default=datetime.utcnow().isoformat())

    asset = relationship("Asset", back_populates="prices")


class AssetType(Base):
    __tablename__ = "asset_types"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    icon = Column(String)
    color = Column(String, default="gray")
    is_custom = Column(Integer, default=0)
    created_at = Column(String, default=datetime.utcnow().isoformat())
