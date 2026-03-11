from pydantic import BaseModel, field_serializer, field_validator
from datetime import datetime, date
from typing import Optional, List


class AssetBase(BaseModel):
    name: str
    type: Optional[str] = None
    type_icon: Optional[str] = None
    amount: float
    purchase_date: str

    @field_validator('purchase_date')
    @classmethod
    def validate_purchase_date(cls, v):
        try:
            datetime.fromisoformat(v.replace('Z', '+00:00'))
        except:
            raise ValueError('Invalid date format, expected YYYY-MM-DD')
        return v


class AssetCreate(AssetBase):
    pass


class AssetUpdate(BaseModel):
    name: Optional[str] = None
    type: Optional[str] = None
    type_icon: Optional[str] = None
    amount: Optional[float] = None
    purchase_date: Optional[str] = None
    sold_date: Optional[str] = None
    sold_price: Optional[float] = None

    @field_validator('purchase_date', 'sold_date')
    @classmethod
    def validate_date(cls, v):
        if v is not None:
            try:
                datetime.fromisoformat(v.replace('Z', '+00:00'))
            except:
                raise ValueError('Invalid date format, expected YYYY-MM-DD')
        return v


class PriceRecordBase(BaseModel):
    price: float
    date: str

    @field_validator('date')
    @classmethod
    def validate_date(cls, v):
        try:
            datetime.fromisoformat(v.replace('Z', '+00:00'))
        except:
            raise ValueError('Invalid date format, expected YYYY-MM-DD')
        return v


class PriceRecordCreate(PriceRecordBase):
    pass


class PriceRecord(PriceRecordBase):
    id: int
    asset_id: int
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True


class Asset(AssetBase):
    id: int
    sold_date: Optional[str] = None
    sold_price: Optional[float] = None
    daily_value: float
    created_at: str
    updated_at: str
    prices: List[PriceRecord] = []

    class Config:
        from_attributes = True


class AssetResponse(BaseModel):
    code: int
    data: Asset


class AssetsResponse(BaseModel):
    code: int
    data: List[Asset]


class PriceResponse(BaseModel):
    code: int
    data: List[PriceRecord]


class DailyValueRequest(BaseModel):
    amount: float
    purchase_date: str


class DailyValueResponse(BaseModel):
    code: int
    data: dict


class SuccessResponse(BaseModel):
    code: int
    data: Optional[dict] = None
