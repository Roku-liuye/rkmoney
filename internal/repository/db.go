package repository

import (
	"rkmoney/model"

	"gorm.io/driver/sqlite"
	"gorm.io/gorm"
)

func InitDB(dsn string) *gorm.DB {
	db, err := gorm.Open(sqlite.Open(dsn), &gorm.Config{})
	if err != nil {
		panic("failed to connect database: " + err.Error())
	}

	if err := db.AutoMigrate(
		&model.Asset{},
		&model.PriceRecord{},
	); err != nil {
		panic("failed to migrate database: " + err.Error())
	}

	return db
}
