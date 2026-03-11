package handler

import (
	"rkmoney/internal/model"
	"rkmoney/internal/service"

	"github.com/gin-gonic/gin"
	"gorm.io/gorm"
)

func RegisterRoutes(r *gin.RouterGroup, db *gorm.DB) {
	assetService := service.NewAssetService(db)

	r.GET("/assets", assetService.ListAssets)
	r.POST("/assets", assetService.CreateAsset)
	r.GET("/assets/:id", assetService.GetAsset)
	r.PUT("/assets/:id", assetService.UpdateAsset)
	r.DELETE("/assets/:id", assetService.DeleteAsset)

	r.GET("/assets/:id/prices", assetService.GetAssetPrices)
	r.POST("/assets/:id/prices", assetService.AddPriceRecord)
}
