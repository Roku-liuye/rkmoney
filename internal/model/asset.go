package model

import (
	"time"

	"gorm.io/gorm"
)

type Asset struct {
	ID        uint           `gorm:"primaryKey" json:"id"`
	Name      string         `json:"name"`
	Code      string         `json:"code" gorm:"uniqueIndex"`
	Type      string         `json:"type"`
	CreatedAt time.Time      `json:"created_at"`
	UpdatedAt time.Time      `json:"updated_at"`
	DeletedAt gorm.DeletedAt `gorm:"index" json:"-"`
	Prices    []PriceRecord  `json:"prices"`
}

type PriceRecord struct {
	ID        uint           `gorm:"primaryKey" json:"id"`
	AssetID   uint           `json:"asset_id" gorm:"index"`
	Price     float64        `json:"price"`
	Date      time.Time      `json:"date" gorm:"index"`
	CreatedAt time.Time      `json:"created_at"`
	UpdatedAt time.Time      `json:"updated_at"`
	DeletedAt gorm.DeletedAt `gorm:"index" json:"-"`
}
