package main

import (
	"encoding/json"
	"fmt"
	"os"
	"path/filepath"
	"sort"
	"time"
)

// LogEntry represents a single persisted exercise record
type LogEntry struct {
	Name        string    `json:"name"`
	Reps        string    `json:"reps"`
	Duration    float32   `json:"duration"`
	CompletedAt time.Time `json:"completed_at"`
}

// TypeSummary holds aggregated stats for one exercise type
type TypeSummary struct {
	Name          string
	Count         int
	TotalDuration float32
}

// ExerciseLog manages persistent exercise history
type ExerciseLog struct {
	Version  int        `json:"version"`
	Entries  []LogEntry `json:"entries"`
	filePath string
}

// logFilePath returns the platform-standard path for the exercise log:
//   macOS:  ~/Library/Application Support/claude-gym/exercise-log.json
//   Linux:  ~/.config/claude-gym/exercise-log.json
func logFilePath() string {
	configDir, err := os.UserConfigDir()
	if err != nil {
		home, err := os.UserHomeDir()
		if err != nil {
			return "claude-gym-log.json"
		}
		return filepath.Join(home, ".claude-gym", "exercise-log.json")
	}
	return filepath.Join(configDir, "claude-gym", "exercise-log.json")
}

// LoadExerciseLog reads the log from disk, returning an empty log on error
func LoadExerciseLog() *ExerciseLog {
	path := logFilePath()
	log := &ExerciseLog{
		Version:  1,
		filePath: path,
	}

	data, err := os.ReadFile(path)
	if err != nil {
		return log
	}

	if err := json.Unmarshal(data, log); err != nil {
		fmt.Fprintf(os.Stderr, "Warning: corrupt exercise log, starting fresh\n")
		log.Entries = nil
	}
	log.filePath = path
	return log
}

// Save writes the log to disk
func (l *ExerciseLog) Save() error {
	dir := filepath.Dir(l.filePath)
	if err := os.MkdirAll(dir, 0755); err != nil {
		return err
	}
	data, err := json.MarshalIndent(l, "", "  ")
	if err != nil {
		return err
	}
	return os.WriteFile(l.filePath, data, 0644)
}

// AddEntries appends completed exercises with current timestamp
func (l *ExerciseLog) AddEntries(exercises []CompletedExercise) {
	now := time.Now()
	for _, ex := range exercises {
		l.Entries = append(l.Entries, LogEntry{
			Name:        ex.Name,
			Reps:        ex.Reps,
			Duration:    ex.Duration,
			CompletedAt: now,
		})
	}
}

// Clear empties the log and saves
func (l *ExerciseLog) Clear() error {
	l.Entries = nil
	return l.Save()
}

// TodayEntries returns entries from today (local time)
func (l *ExerciseLog) TodayEntries() []LogEntry {
	now := time.Now()
	year, month, day := now.Date()
	loc := now.Location()
	startOfDay := time.Date(year, month, day, 0, 0, 0, 0, loc)

	var result []LogEntry
	for _, e := range l.Entries {
		if e.CompletedAt.In(loc).After(startOfDay) || e.CompletedAt.In(loc).Equal(startOfDay) {
			result = append(result, e)
		}
	}
	return result
}

// DayBucket holds aggregated stats for one calendar day
type DayBucket struct {
	Date          time.Time
	Count         int
	TotalDuration float32 // seconds
}

// DailyTrend returns per-day stats sorted most recent first
func (l *ExerciseLog) DailyTrend() []DayBucket {
	if len(l.Entries) == 0 {
		return nil
	}

	loc := time.Now().Location()
	buckets := make(map[string]*DayBucket)

	for _, e := range l.Entries {
		local := e.CompletedAt.In(loc)
		day := time.Date(local.Year(), local.Month(), local.Day(), 0, 0, 0, 0, loc)
		key := day.Format("2006-01-02")
		b, ok := buckets[key]
		if !ok {
			b = &DayBucket{Date: day}
			buckets[key] = b
		}
		b.Count++
		b.TotalDuration += e.Duration
	}

	result := make([]DayBucket, 0, len(buckets))
	for _, b := range buckets {
		result = append(result, *b)
	}
	sort.Slice(result, func(i, j int) bool {
		return result[i].Date.After(result[j].Date)
	})
	return result
}

// TodayBreakdown returns per-exercise-type stats for today, sorted by total duration desc
func (l *ExerciseLog) TodayBreakdown() []TypeSummary {
	entries := l.TodayEntries()
	return typeBreakdownFromEntries(entries)
}

func typeBreakdownFromEntries(entries []LogEntry) []TypeSummary {
	byName := make(map[string]*TypeSummary)
	for _, e := range entries {
		ts, ok := byName[e.Name]
		if !ok {
			ts = &TypeSummary{Name: e.Name}
			byName[e.Name] = ts
		}
		ts.Count++
		ts.TotalDuration += e.Duration
	}

	result := make([]TypeSummary, 0, len(byName))
	for _, ts := range byName {
		result = append(result, *ts)
	}
	sort.Slice(result, func(i, j int) bool {
		return result[i].TotalDuration > result[j].TotalDuration
	})
	return result
}

// TypeBreakdown returns per-exercise-type stats sorted by total duration desc
func (l *ExerciseLog) TypeBreakdown() []TypeSummary {
	byName := make(map[string]*TypeSummary)
	for _, e := range l.Entries {
		ts, ok := byName[e.Name]
		if !ok {
			ts = &TypeSummary{Name: e.Name}
			byName[e.Name] = ts
		}
		ts.Count++
		ts.TotalDuration += e.Duration
	}

	result := make([]TypeSummary, 0, len(byName))
	for _, ts := range byName {
		result = append(result, *ts)
	}
	sort.Slice(result, func(i, j int) bool {
		return result[i].TotalDuration > result[j].TotalDuration
	})
	return result
}
