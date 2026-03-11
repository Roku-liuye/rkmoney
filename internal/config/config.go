package config

import (
	"fmt"
	"os"

	"github.com/spf13/viper"
)

type Config struct {
	Server   ServerConfig
	Database DatabaseConfig
}

type ServerConfig struct {
	Port string `mapstructure:"port"`
}

type DatabaseConfig struct {
	DSN string `mapstructure:"dsn"`
}

func InitConfig() *Config {
	viper.SetConfigType("env")
	viper.SetConfigName(".env")
	viper.AddConfigPath(".")

	if err := viper.ReadInConfig(); err != nil {
		if _, ok := err.(viper.ConfigFileNotFoundError); ok {
			fmt.Println("No .env file found, using default values")
		} else {
			fmt.Printf("Config file error: %v\n", err)
			os.Exit(1)
		}
	}

	viper.SetDefault("port", ":8080")
	viper.SetDefault("database.dsn", "./data/rkmoney.db")

	var cfg Config
	if err := viper.Unmarshal(&cfg); err != nil {
		fmt.Printf("Failed to unmarshal config: %v\n", err)
		os.Exit(1)
	}

	return &cfg
}
