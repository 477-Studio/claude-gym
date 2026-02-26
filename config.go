package main

import (
	"encoding/json"
	"os"
)

// Config holds user configuration
type Config struct {
	// Display settings
	Scale      int  `json:"scale"`
	Fullscreen bool `json:"fullscreen"`
	Debug      bool `json:"debug"`
}

// DefaultConfig returns a config with sensible defaults
func DefaultConfig() *Config {
	return &Config{
		Scale:      3,
		Fullscreen: false,
		Debug:      false,
	}
}

// LoadConfig loads configuration from a JSON file
func LoadConfig(path string) *Config {
	config := DefaultConfig()

	data, err := os.ReadFile(path)
	if err != nil {
		// File doesn't exist, use defaults
		return config
	}

	if err := json.Unmarshal(data, config); err != nil {
		// Invalid JSON, use defaults
		return config
	}

	return config
}

// Save writes the config to a JSON file
func (c *Config) Save(path string) error {
	data, err := json.MarshalIndent(c, "", "  ")
	if err != nil {
		return err
	}
	return os.WriteFile(path, data, 0644)
}
