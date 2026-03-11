from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import get_db, engine
from models import Base
import crud
import schemas

Base.metadata.create_all(bind=engine)

app = FastAPI(title="rkmoney API", description="资产价值管理 API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/api/assets", response_model=schemas.AssetResponse, status_code=201)
def create_asset(asset: schemas.AssetCreate, db: Session = Depends(get_db)):
    db_asset = crud.create_asset(db, asset)
    return schemas.AssetResponse(code=201, data=db_asset)


@app.get("/api/assets", response_model=schemas.AssetsResponse)
def read_assets(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    assets = crud.get_assets(db, skip=skip, limit=limit)
    return schemas.AssetsResponse(code=200, data=assets)


@app.get("/api/assets/{asset_id}", response_model=schemas.AssetResponse)
def read_asset(asset_id: int, db: Session = Depends(get_db)):
    db_asset = crud.get_asset(db, asset_id=asset_id)
    if db_asset is None:
        raise HTTPException(status_code=404, detail="Asset not found")
    return schemas.AssetResponse(code=200, data=db_asset)


@app.put("/api/assets/{asset_id}", response_model=schemas.AssetResponse)
def update_asset(asset_id: int, asset: schemas.AssetUpdate, db: Session = Depends(get_db)):
    db_asset = crud.update_asset(db, asset_id=asset_id, asset=asset)
    if db_asset is None:
        raise HTTPException(status_code=404, detail="Asset not found")
    return schemas.AssetResponse(code=200, data=db_asset)


@app.delete("/api/assets/{asset_id}", response_model=schemas.SuccessResponse)
def delete_asset(asset_id: int, db: Session = Depends(get_db)):
    db_asset = crud.delete_asset(db, asset_id=asset_id)
    if db_asset is None:
        raise HTTPException(status_code=404, detail="Asset not found")
    return schemas.SuccessResponse(code=200)


@app.post("/api/assets/{asset_id}/sell", response_model=schemas.AssetResponse)
def sell_asset(asset_id: int, sold_date: str, sold_price: float, db: Session = Depends(get_db)):
    try:
        from datetime import datetime
        date_obj = datetime.fromisoformat(sold_date.replace('Z', '+00:00').replace('+00:00', ''))
    except:
        raise HTTPException(status_code=400, detail="Invalid date format")
    
    db_asset = crud.sell_asset(db, asset_id=asset_id, sold_date=date_obj, sold_price=sold_price)
    if db_asset is None:
        raise HTTPException(status_code=404, detail="Asset not found")
    return schemas.AssetResponse(code=200, data=db_asset)


@app.get("/api/assets/{asset_id}/prices", response_model=schemas.PriceResponse)
def read_asset_prices(asset_id: int, db: Session = Depends(get_db)):
    prices = crud.get_asset_prices(db, asset_id=asset_id)
    return schemas.PriceResponse(code=200, data=prices)


@app.post("/api/assets/{asset_id}/prices", response_model=schemas.PriceResponse)
def create_price_record(asset_id: int, price: schemas.PriceRecordCreate, db: Session = Depends(get_db)):
    db_price = crud.add_price_record(db, asset_id=asset_id, price=price)
    return schemas.PriceResponse(code=201, data=[db_price])


@app.post("/api/calculate-daily-value", response_model=schemas.DailyValueResponse)
def calculate_daily_value(req: schemas.DailyValueRequest, db: Session = Depends(get_db)):
    try:
        from datetime import datetime
        purchase_date = datetime.fromisoformat(req.purchase_date.replace('Z', '+00:00').replace('+00:00', ''))
    except:
        raise HTTPException(status_code=400, detail="Invalid date format")
    
    today = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    purchase = purchase_date.replace(hour=0, minute=0, second=0, microsecond=0)

    if today == purchase:
        daily_value = req.amount
    else:
        days = (today - purchase).days
        if days == 0:
            days = 1
        daily_value = req.amount / days

    return schemas.DailyValueResponse(code=200, data={"daily_value": daily_value})
