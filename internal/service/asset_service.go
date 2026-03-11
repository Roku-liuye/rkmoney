package service

import (
	"rkmoney/internal/model"
	"rkmoney/internal/repository"

	"gorm.io/gorm"
)

type AssetService struct {
	db *gorm.DB
}

func NewAssetService(db *gorm.DB) *AssetService {
	return &AssetService{db: db}
}

func (s *AssetService) ListAssets() ([]model.Asset, error) {
	var assets []model.Asset
	if err := s.db.Preload("Prices").Find(&assets).Error; err != nil {
		return nil, err
	}
	return assets, nil
}

func (s *AssetService) GetAsset(id uint) (*model.Asset, error) {
	var asset model.Asset
	if err := s.db.Preload("Prices").First(&asset, id).Error; err != nil {
		return nil, err
	}
	return &asset, nil
}

func (s *AssetService) CreateAsset(asset *model.Asset) (*model.Asset, error) {
	if err := s.db.Create(asset).Error; err != nil {
		return nil, err
	}
	return asset, nil
}

func (s *AssetService) UpdateAsset(id uint, asset *model.Asset) (*model.Asset, error) {
	if err := s.db.Model(&model.Asset{}).Where("id = ?", id).Updates(asset).Error; err != nil {
		return nil, err
	}
	return s.GetAsset(id)
}

func (s *AssetService) DeleteAsset(id uint) error {
	if err := s.db.Delete(&model.Asset{}, id).Error; err != nil {
		return err
	}
	return nil
}

func (s *AssetService) GetAssetPrices(assetID uint) ([]model.PriceRecord, error) {
	var prices []model.PriceRecord
	if err := s.db.Where("asset_id = ?", assetID).Order("date DESC").Find(&prices).Error; err != nil {
		return nil, err
	}
	return prices, nil
}

func (s *AssetService) AddPriceRecord(assetID uint, price *model.PriceRecord) (*model.PriceRecord, error) {
	price.AssetID = assetID
	if err := s.db.Create(price).Error; err != nil {
		return nil, err
	}
	return price, nil
}
