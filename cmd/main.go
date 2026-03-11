package main

import (
	"rkmoney/config"
	"rkmoney/internal/handler"
	"rkmoney/internal/middleware"
	"rkmoney/internal/repository"

	"github.com/gin-gonic/gin"
)

func main() {
	cfg := config.InitConfig()
	db := repository.InitDB(cfg.Database.DSN)

	r := gin.Default()

	r.Use(middleware.CORS())

	apiGroup := r.Group("/api")
	{
		handler.RegisterRoutes(apiGroup, db)
	}

	r.Static("/static", "./static")

	r.Run(cfg.Server.Port)
}
