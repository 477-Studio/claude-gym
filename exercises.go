package main

import (
	"encoding/json"
	"fmt"
	"os"
)

// ExerciseConfig defines a single exercise type
type ExerciseConfig struct {
	Name    string `json:"name"`
	AnimRow int    `json:"anim_row"`
	Reps    string `json:"reps"`
}

// BubbleText returns the speech bubble text for this exercise
func (e ExerciseConfig) BubbleText() string {
	return fmt.Sprintf("Let's do %s!\n%s", e.Name, e.Reps)
}

// CompletedExercise tracks a single completed exercise
type CompletedExercise struct {
	Name     string
	Reps     string
	Duration float32 // seconds spent on this exercise
}

// LoadExercises reads exercise configs from a JSON file
func LoadExercises(path string) ([]ExerciseConfig, error) {
	data, err := os.ReadFile(path)
	if err != nil {
		return nil, fmt.Errorf("failed to read exercises file: %w", err)
	}

	var exercises []ExerciseConfig
	if err := json.Unmarshal(data, &exercises); err != nil {
		return nil, fmt.Errorf("failed to parse exercises: %w", err)
	}

	if len(exercises) == 0 {
		return nil, fmt.Errorf("no exercises found in %s", path)
	}

	return exercises, nil
}
