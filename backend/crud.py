from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from models import Asset, PriceRecord, AssetType
from schemas import AssetCreate, AssetUpdate, PriceRecordCreate, AssetTypeCreate


def calculate_daily_value(asset: Asset) -> float:
    purchase_date = asset.purchase_date
    today = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)

    if isinstance(purchase_date, str):
        from datetime import datetime as dt
        purchase_date = dt.fromisoformat(purchase_date.replace('Z', '+00:00').replace('+00:00', ''))

    days = 0

    if asset.sold_date:
        sold_date = asset.sold_date
        if isinstance(sold_date, str):
            from datetime import datetime as dt
            sold_date = dt.fromisoformat(sold_date.replace('Z', '+00:00').replace('+00:00', ''))
        
        if sold_date < purchase_date:
            sold_date = purchase_date
        
        days = (sold_date - purchase_date).days
        if days == 0:
            days = 1
    else:
        if today == purchase_date.replace(hour=0, minute=0, second=0, microsecond=0):
            days = 1
        else:
            days = (today - purchase_date.replace(hour=0, minute=0, second=0, microsecond=0)).days
            if days == 0:
                days = 1

    daily_value = asset.amount / days

    if asset.sold_date and asset.sold_price:
        daily_value = daily_value - (asset.sold_price / days)

    if daily_value < 0:
        daily_value = 0

    return daily_value


def get_assets(db: Session, skip: int = 0, limit: int = 100):
    assets = db.query(Asset).offset(skip).limit(limit).all()
    for asset in assets:
        asset.daily_value = calculate_daily_value(asset)
    return assets


def get_asset(db: Session, asset_id: int):
    asset = db.query(Asset).filter(Asset.id == asset_id).first()
    if asset:
        asset.daily_value = calculate_daily_value(asset)
    return asset


def create_asset(db: Session, asset: AssetCreate):
    db_asset = Asset(
        name=asset.name,
        type=asset.type,
        type_icon=asset.type_icon,
        amount=asset.amount,
        purchase_date=asset.purchase_date,
        daily_value=0.0
    )
    db.add(db_asset)
    db.commit()
    db.refresh(db_asset)
    db_asset.daily_value = calculate_daily_value(db_asset)
    return db_asset


def update_asset(db: Session, asset_id: int, asset: AssetUpdate):
    db_asset = db.query(Asset).filter(Asset.id == asset_id).first()
    if not db_asset:
        return None

    update_data = asset.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_asset, key, value)

    db.commit()
    db.refresh(db_asset)
    db_asset.daily_value = calculate_daily_value(db_asset)
    return db_asset


def delete_asset(db: Session, asset_id: int):
    db_asset = db.query(Asset).filter(Asset.id == asset_id).first()
    if db_asset:
        db.delete(db_asset)
        db.commit()
    return db_asset


def get_asset_prices(db: Session, asset_id: int):
    return db.query(PriceRecord).filter(PriceRecord.asset_id == asset_id).order_by(PriceRecord.date.desc()).all()


def add_price_record(db: Session, asset_id: int, price: PriceRecordCreate):
    db_price = PriceRecord(
        asset_id=asset_id,
        price=price.price,
        date=price.date
    )
    db.add(db_price)
    db.commit()
    db.refresh(db_price)
    return db_price


def sell_asset(db: Session, asset_id: int, sold_date: datetime, sold_price: float):
    db_asset = db.query(Asset).filter(Asset.id == asset_id).first()
    if not db_asset:
        return None

    db_asset.sold_date = sold_date
    db_asset.sold_price = sold_price

    db.commit()
    db.refresh(db_asset)
    db_asset.daily_value = calculate_daily_value(db_asset)
    return db_asset


def get_asset_types(db: Session, skip: int = 0, limit: int = 100, include_custom: bool = True):
    query = db.query(AssetType)
    if not include_custom:
        query = query.filter(AssetType.is_custom == 0)
    types = query.offset(skip).limit(limit).all()
    return types


def get_asset_type(db: Session, type_id: int):
    return db.query(AssetType).filter(AssetType.id == type_id).first()


def create_asset_type(db: Session, type_data: AssetTypeCreate):
    db_type = AssetType(
        name=type_data.name,
        icon=type_data.icon,
        color=type_data.color or "gray",
        is_custom=1
    )
    db.add(db_type)
    db.commit()
    db.refresh(db_type)
    return db_type


def update_asset_type(db: Session, type_id: int, type_data: AssetTypeCreate):
    db_type = db.query(AssetType).filter(AssetType.id == type_id).first()
    if not db_type:
        return None

    update_data = type_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_type, key, value)

    db.commit()
    db.refresh(db_type)
    return db_type


def delete_asset_type(db: Session, type_id: int):
    db_type = db.query(AssetType).filter(AssetType.id == type_id).first()
    if db_type:
        db.delete(db_type)
        db.commit()
    return db_type
