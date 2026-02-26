package main

import (
	"fmt"
	"math/rand/v2"
	"os"

	rl "github.com/gen2brain/raylib-go/raylib"
)

// AppMode represents the current mode of the application
type AppMode int

const (
	ModeIdle        AppMode = iota // Coffee sip, Tab opens menu
	ModeMenu                       // Overlay with options
	ModePrompting                  // Waving, "Time to exercise!" prompt
	ModePumpUp                     // "Let's do it!" animation, then transition
	ModeCountdown                  // 3-2-1 countdown before exercise
	ModeExercising                 // Looping exercise animation + speech bubble
	ModePaused                     // Esc pressed, character frozen
	ModeSummary                    // Exercise summary overlay
	ModeExerciseLog                // Persistent exercise log with tabs
)

// MenuOption indices
const (
	MenuStartExercise = 0
	MenuSummary       = 1
	MenuOptionCount   = 2
)

// MenuState manages the exercise menu and flow
type MenuState struct {
	Mode            AppMode
	PrevMode        AppMode // mode before entering menu (for Esc to return)
	SelectedOption  int
	CurrentExercise int // index into Exercises slice
	Exercises       []ExerciseConfig
	CurrentRound    []CompletedExercise // exercises done in current round

	// Prompt cooldown: avoid nagging after dismiss
	elapsedTime     float32 // internal clock, updated each frame
	LastDismissTime float32 // elapsedTime when last dismissed
	CooldownSeconds float32 // how long to wait before re-prompting

	// Streak detection
	ConsecutiveToolCalls int // tool_use count since last user prompt
	StreakThreshold      int // how many consecutive tool calls before triggering (default: 3)

	// Exercise auto-advance
	ExerciseTimer    float32 // counts up during ModeExercising, resets on each new exercise
	ExerciseDuration float32 // seconds before auto-advancing (default: 60)
	RecentExercises  []int   // last 2 exercise indices (for no-repeat constraint)

	// Countdown state
	CountdownValue   int     // current number (3, 2, 1)
	CountdownTimer   float32 // time accumulator
	IsFirstExercise  bool    // tracks first vs subsequent for bubble text

	// Exercise log (persistent)
	ExerciseLog  *ExerciseLog
	LogTab           int // 0=Today, 1=Week, 2=Stats
	LogScrollPos     int
	ClearConfirmed   bool // true after first Enter on CLEAR tab

	// Cat alert notification (during exercise modes only)
	CatAlert     bool   // true when cat is jumping
	CatAlertText string // banner text above cat
}

// NewMenuState creates a new menu state with loaded exercises
func NewMenuState(exercises []ExerciseConfig) *MenuState {
	return &MenuState{
		Mode:             ModeIdle,
		Exercises:        exercises,
		CooldownSeconds:  60, // 1 minute
		StreakThreshold:   3,
		ExerciseDuration: 45.0,
		IsFirstExercise:  true,
	}
}

// Update advances the internal timer and auto-advances exercises
func (m *MenuState) Update(dt float32, anim *AnimationSystem) {
	m.elapsedTime += dt
	// Auto-advance exercise after duration
	if m.Mode == ModeExercising {
		m.ExerciseTimer += dt
		if m.ExerciseTimer >= m.ExerciseDuration {
			m.completeCurrentExercise()
			m.advanceExercise()
			m.startPumpUp(anim)
		}
	}
	// Countdown ticker
	if m.Mode == ModeCountdown {
		m.CountdownTimer += dt
		if m.CountdownTimer >= 1.0 {
			m.CountdownTimer -= 1.0
			m.CountdownValue--
			if m.CountdownValue <= 0 {
				m.startExercise(anim)
			}
		}
	}
}

// HandleInput processes keyboard input based on current mode.
// Returns true if input was consumed.
func (m *MenuState) HandleInput(anim *AnimationSystem) bool {
	switch m.Mode {
	case ModeIdle:
		return m.handleIdleInput(anim)
	case ModeMenu:
		return m.handleMenuInput(anim)
	case ModePrompting:
		return m.handlePromptingInput(anim)
	case ModePumpUp:
		// No input during pump-up, it auto-transitions
		return false
	case ModeCountdown:
		return m.handleCountdownInput(anim)
	case ModeExercising:
		return m.handleExercisingInput(anim)
	case ModePaused:
		return m.handlePausedInput(anim)
	case ModeSummary:
		return m.handleSummaryInput(anim)
	case ModeExerciseLog:
		return m.handleExerciseLogInput(anim)
	}
	return false
}

func (m *MenuState) handleIdleInput(anim *AnimationSystem) bool {
	if rl.IsKeyPressed(rl.KeyTab) {
		m.PrevMode = m.Mode
		m.Mode = ModeMenu
		m.SelectedOption = MenuStartExercise
		return true
	}
	return false
}

func (m *MenuState) handlePromptingInput(anim *AnimationSystem) bool {
	if rl.IsKeyPressed(rl.KeyY) || rl.IsKeyPressed(rl.KeyEnter) {
		m.advanceExercise()
		m.startPumpUp(anim)
		return true
	}
	if rl.IsKeyPressed(rl.KeyN) || rl.IsKeyPressed(rl.KeyEscape) {
		m.dismissPrompt()
		anim.StartIdleSequence()
		return true
	}
	if rl.IsKeyPressed(rl.KeyTab) {
		m.PrevMode = m.Mode
		m.Mode = ModeMenu
		m.SelectedOption = MenuStartExercise
		return true
	}
	return false
}

// dismissPrompt returns to idle and records the dismiss time for cooldown
func (m *MenuState) dismissPrompt() {
	m.Mode = ModeIdle
	m.LastDismissTime = m.elapsedTime
}

// isExerciseMode returns true if the user is in an exercise session
func (m *MenuState) isExerciseMode() bool {
	switch m.Mode {
	case ModeExercising, ModePaused, ModeCountdown, ModePumpUp:
		return true
	}
	return false
}

// HandleEvent processes watcher events for auto-prompting.
func (m *MenuState) HandleEvent(event Event, anim *AnimationSystem) {
	// Cat alert notifications during exercise modes
	if m.isExerciseMode() {
		switch event.Type {
		case EventTurnComplete:
			m.CatAlert = true
			m.CatAlertText = "Claude Code is done!"
		case EventAskUser, EventPermissionEscalation:
			m.CatAlert = true
			m.CatAlertText = "Claude Code needs you!"
		case EventQuest:
			// User is back at keyboard — dismiss the cat
			m.CatAlert = false
			m.CatAlertText = ""
		}
	}

	// Auto-dismiss prompt if user's attention is needed in Claude Code
	// (no cooldown — only explicit N/Esc dismiss starts cooldown)
	if m.Mode == ModePrompting {
		switch event.Type {
		case EventSuccess, EventError, EventAskUser, EventPlanApproved, EventQuest:
			m.Mode = ModeIdle
			anim.StartIdleSequence()
			return
		}
	}

	// Reset streak on user activity
	switch event.Type {
	case EventQuest, EventAskUser:
		m.ConsecutiveToolCalls = 0
	}

	// Count consecutive tool calls (tool_use events from assistant)
	switch event.Type {
	case EventReading, EventBash, EventWriting, EventTodoUpdate:
		m.ConsecutiveToolCalls++
	}

	// Determine if this event should trigger a prompt
	shouldTrigger := false
	switch event.Type {
	case EventPlanStart:
		shouldTrigger = true
	case EventPermissionEscalation:
		shouldTrigger = true
	case EventSpawnAgent:
		shouldTrigger = true
	case EventPlanApproved:
		shouldTrigger = true
	case EventReading, EventBash, EventWriting, EventTodoUpdate:
		if m.ConsecutiveToolCalls >= m.StreakThreshold {
			shouldTrigger = true
			m.ConsecutiveToolCalls = 0 // reset so it can re-trigger after another streak
		}
	}

	if !shouldTrigger {
		return
	}

	// Only prompt if currently idle
	if m.Mode != ModeIdle {
		return
	}

	// Respect cooldown
	if m.LastDismissTime > 0 && (m.elapsedTime-m.LastDismissTime) < m.CooldownSeconds {
		return
	}

	m.Mode = ModePrompting
	anim.SetLoopMode(true)
	anim.SetAnimation(AnimWave)
}

func (m *MenuState) handleMenuInput(anim *AnimationSystem) bool {
	if rl.IsKeyPressed(rl.KeyEscape) {
		m.Mode = m.PrevMode
		return true
	}
	if rl.IsKeyPressed(rl.KeyUp) || rl.IsKeyPressed(rl.KeyW) {
		m.SelectedOption--
		if m.SelectedOption < 0 {
			m.SelectedOption = MenuOptionCount - 1
		}
		return true
	}
	if rl.IsKeyPressed(rl.KeyDown) || rl.IsKeyPressed(rl.KeyS) {
		m.SelectedOption++
		if m.SelectedOption >= MenuOptionCount {
			m.SelectedOption = 0
		}
		return true
	}
	if rl.IsKeyPressed(rl.KeyEnter) || rl.IsKeyPressed(rl.KeySpace) {
		switch m.SelectedOption {
		case MenuStartExercise:
			m.advanceExercise()
			m.startPumpUp(anim)
		case MenuSummary:
			m.Mode = ModeExerciseLog
			m.LogTab = 0
			m.LogScrollPos = 0
		}
		return true
	}
	return false
}

func (m *MenuState) handleExercisingInput(anim *AnimationSystem) bool {
	if rl.IsKeyPressed(rl.KeyTab) {
		// Complete current exercise and move to next
		m.completeCurrentExercise()
		m.advanceExercise()
		m.startPumpUp(anim)
		return true
	}
	if rl.IsKeyPressed(rl.KeyEscape) {
		m.PrevMode = ModeExercising
		m.Mode = ModePaused
		anim.SetPaused(true)
		return true
	}
	return false
}

func (m *MenuState) handleCountdownInput(anim *AnimationSystem) bool {
	if rl.IsKeyPressed(rl.KeyEscape) {
		m.PrevMode = ModeCountdown
		m.Mode = ModePaused
		anim.SetPaused(true)
		return true
	}
	return false
}

func (m *MenuState) handlePausedInput(anim *AnimationSystem) bool {
	if rl.IsKeyPressed(rl.KeyEnter) {
		// Complete current exercise, show summary (finishRound deferred to summary dismiss)
		m.completeCurrentExercise()
		m.Mode = ModeSummary
		anim.SetPaused(false)
		anim.StartIdleSequence()
		return true
	}
	if rl.IsKeyPressed(rl.KeyEscape) {
		// Resume to wherever we paused from (countdown or exercising)
		m.Mode = m.PrevMode
		anim.SetPaused(false)
		return true
	}
	return false
}

func (m *MenuState) handleSummaryInput(anim *AnimationSystem) bool {
	if rl.IsKeyPressed(rl.KeyEscape) || rl.IsKeyPressed(rl.KeyEnter) {
		m.finishRound()
		m.IsFirstExercise = true
		m.CatAlert = false
		m.CatAlertText = ""
		m.Mode = ModeIdle
		return true
	}
	return false
}

// startPumpUp begins the pump-up animation before an exercise
func (m *MenuState) startPumpUp(anim *AnimationSystem) {
	m.Mode = ModePumpUp
	anim.SetLoopMode(false)
	anim.SetAnimation(AnimPumpUp)
	anim.SetOnComplete(func() {
		m.startCountdown(anim)
	})
}

// startCountdown begins the 3-2-1 countdown before an exercise
func (m *MenuState) startCountdown(anim *AnimationSystem) {
	m.Mode = ModeCountdown
	m.CountdownValue = 3
	m.CountdownTimer = 0
	// Keep playing the pump-up animation during countdown
	anim.SetLoopMode(true)
	anim.SetAnimation(AnimPumpUp)
}

// startExercise begins the current exercise animation
func (m *MenuState) startExercise(anim *AnimationSystem) {
	m.Mode = ModeExercising
	m.ExerciseTimer = 0 // reset timer for new exercise
	m.IsFirstExercise = false
	if len(m.Exercises) == 0 {
		return
	}
	// Track this exercise in recent history (keep last 2)
	m.RecentExercises = append(m.RecentExercises, m.CurrentExercise)
	if len(m.RecentExercises) > 2 {
		m.RecentExercises = m.RecentExercises[len(m.RecentExercises)-2:]
	}
	ex := m.Exercises[m.CurrentExercise]
	anim.SetLoopMode(true)
	anim.SetAnimation(AnimationType(ex.AnimRow))
}

// completeCurrentExercise records the current exercise as done and persists it immediately
func (m *MenuState) completeCurrentExercise() {
	if len(m.Exercises) == 0 {
		return
	}
	if m.ExerciseTimer < 10.0 {
		return // skipped too quickly, don't count
	}
	ex := m.Exercises[m.CurrentExercise]
	completed := CompletedExercise{
		Name:     ex.Name,
		Reps:     ex.Reps,
		Duration: m.ExerciseTimer,
	}
	m.CurrentRound = append(m.CurrentRound, completed)

	// Persist immediately so data survives window close
	if m.ExerciseLog != nil {
		m.ExerciseLog.AddEntries([]CompletedExercise{completed})
		if err := m.ExerciseLog.Save(); err != nil {
			fmt.Fprintf(os.Stderr, "Warning: failed to save exercise log: %v\n", err)
		}
	}
}

// advanceExercise picks a random exercise, avoiding the last 2
func (m *MenuState) advanceExercise() {
	m.ExerciseTimer = 0 // reset so stale timer can't record a ghost exercise
	if len(m.Exercises) == 0 {
		return
	}
	// Build candidate list excluding recent exercises
	var candidates []int
	for i := range m.Exercises {
		excluded := false
		for _, r := range m.RecentExercises {
			if i == r {
				excluded = true
				break
			}
		}
		if !excluded {
			candidates = append(candidates, i)
		}
	}
	if len(candidates) == 0 {
		candidates = make([]int, len(m.Exercises))
		for i := range candidates {
			candidates[i] = i
		}
	}
	m.CurrentExercise = candidates[rand.IntN(len(candidates))]
}

// finishRound ends the current round (entries already persisted individually)
func (m *MenuState) finishRound() {
	m.CurrentRound = nil
}

// GetCurrentExercise returns the current exercise config, or nil if none
func (m *MenuState) GetCurrentExercise() *ExerciseConfig {
	if len(m.Exercises) == 0 {
		return nil
	}
	ex := m.Exercises[m.CurrentExercise]
	return &ex
}

// GetRoundSummary returns the current round's completed exercises
func (m *MenuState) GetRoundSummary() []CompletedExercise {
	return m.CurrentRound
}

func (m *MenuState) handleExerciseLogInput(anim *AnimationSystem) bool {
	if rl.IsKeyPressed(rl.KeyEscape) {
		if m.ClearConfirmed {
			m.ClearConfirmed = false
			return true
		}
		m.Mode = m.PrevMode
		return true
	}
	if rl.IsKeyPressed(rl.KeyLeft) {
		m.LogTab--
		if m.LogTab < 0 {
			m.LogTab = 3
		}
		m.LogScrollPos = 0
		m.ClearConfirmed = false
		return true
	}
	if rl.IsKeyPressed(rl.KeyRight) {
		m.LogTab++
		if m.LogTab > 3 {
			m.LogTab = 0
		}
		m.LogScrollPos = 0
		m.ClearConfirmed = false
		return true
	}
	if rl.IsKeyPressed(rl.KeyEnter) && m.LogTab == 3 {
		if !m.ClearConfirmed {
			m.ClearConfirmed = true
		} else {
			if m.ExerciseLog != nil {
				if err := m.ExerciseLog.Clear(); err != nil {
					fmt.Fprintf(os.Stderr, "Warning: failed to clear exercise log: %v\n", err)
				}
			}
			m.ClearConfirmed = false
			m.LogTab = 0
			m.LogScrollPos = 0
		}
		return true
	}
	if rl.IsKeyPressed(rl.KeyUp) {
		if m.LogScrollPos > 0 {
			m.LogScrollPos--
		}
		return true
	}
	if rl.IsKeyPressed(rl.KeyDown) {
		m.LogScrollPos++
		return true
	}
	return false
}

