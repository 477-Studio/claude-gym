package main

import "math/rand/v2"

// AnimationType represents the current animation being played.
// Values match spritesheet row indices in exercise_spritesheet.png.
type AnimationType int

const (
	AnimCoffee     AnimationType = 0 // Row 0: Coffee sip
	AnimWave       AnimationType = 1 // Row 1: Waving/attention
	AnimPumpUp     AnimationType = 2 // Row 2: "Let's do it!" fist pump
	AnimChairDips  AnimationType = 3 // Row 3: Chair dips
	AnimArmCircles AnimationType = 4 // Row 4: Arm circles
	AnimWondering      AnimationType = 5  // Row 5: Looking around (no coffee)
	AnimKneeRaises     AnimationType = 6  // Row 6: Knee raises
	AnimSpinalTwist    AnimationType = 7  // Row 7: Spinal twist
	AnimGluteSqueeze   AnimationType = 8  // Row 8: Glute squeeze
	AnimShoulderRolls  AnimationType = 9  // Row 9: Shoulder rolls
	AnimLegExtensions  AnimationType = 10 // Row 10: Leg extensions
	AnimNeckStretch    AnimationType = 11 // Row 11: Neck stretch
	AnimDeskPushUps    AnimationType = 12 // Row 12: Desk push-ups
	AnimSquats         AnimationType = 13 // Row 13: Bodyweight squats
	AnimCalfRaises     AnimationType = 14 // Row 14: Calf raises
	AnimWallSit        AnimationType = 15 // Row 15: Wall sit
	AnimTorsoRotation  AnimationType = 16 // Row 16: Standing torso rotation
	AnimReverseLunges  AnimationType = 17 // Row 17: Reverse lunges
)

func (a AnimationType) String() string {
	names := map[AnimationType]string{
		AnimCoffee:     "Coffee",
		AnimWave:       "Wave",
		AnimPumpUp:     "PumpUp",
		AnimChairDips:  "ChairDips",
		AnimArmCircles: "ArmCircles",
		AnimWondering:      "Wondering",
		AnimKneeRaises:     "KneeRaises",
		AnimSpinalTwist:    "SpinalTwist",
		AnimGluteSqueeze:   "GluteSqueeze",
		AnimShoulderRolls:  "ShoulderRolls",
		AnimLegExtensions:  "LegExtensions",
		AnimNeckStretch:    "NeckStretch",
		AnimDeskPushUps:    "DeskPushUps",
		AnimSquats:         "Squats",
		AnimCalfRaises:     "CalfRaises",
		AnimWallSit:        "WallSit",
		AnimTorsoRotation:  "TorsoRotation",
		AnimReverseLunges:  "ReverseLunges",
	}
	if name, ok := names[a]; ok {
		return name
	}
	return "Unknown"
}

// AnimationState holds the current state of the character animation
type AnimationState struct {
	CurrentAnim AnimationType
	Frame       int
	Timer       float32
	Queue       []AnimationType
}

// AnimationSystem manages the character animation state machine
type AnimationSystem struct {
	state         *AnimationState
	frameDuration float32
	animLengths   map[AnimationType]int
	loopMode   bool   // When true, animations loop instead of returning to idle
	onComplete func() // Callback when a non-looping animation completes
	paused     bool   // When true, animation freezes on current frame
}

// NewAnimationSystem creates a new animation system
func NewAnimationSystem() *AnimationSystem {
	sys := &AnimationSystem{
		state: &AnimationState{
			CurrentAnim: AnimWondering,
			Frame:       0,
			Timer:       0,
			Queue:       make([]AnimationType, 0),
		},
		frameDuration: 0.084, // ~12 FPS
		animLengths: map[AnimationType]int{
			AnimCoffee:     16,
			AnimWave:       16,
			AnimPumpUp:     16,
			AnimChairDips:  16,
			AnimArmCircles: 16,
			AnimWondering:      16,
			AnimKneeRaises:     16,
			AnimSpinalTwist:    16,
			AnimGluteSqueeze:   16,
			AnimShoulderRolls:  16,
			AnimLegExtensions:  16,
			AnimNeckStretch:    16,
			AnimDeskPushUps:    16,
			AnimSquats:         16,
			AnimCalfRaises:     16,
			AnimWallSit:        16,
			AnimTorsoRotation:  16,
			AnimReverseLunges:  16,
		},
	}
	return sys
}

// SetPaused pauses or unpauses the animation
func (a *AnimationSystem) SetPaused(p bool) {
	a.paused = p
}

// Update advances the animation state
func (a *AnimationSystem) Update(deltaTime float32) {
	if a.paused {
		return
	}
	a.state.Timer += deltaTime

	if a.state.Timer >= a.frameDuration {
		a.state.Timer -= a.frameDuration
		a.state.Frame++

		animLen := a.animLengths[a.state.CurrentAnim]
		if a.state.Frame >= animLen {
			a.onAnimationComplete()
		}
	}
}

// onAnimationComplete handles animation end
func (a *AnimationSystem) onAnimationComplete() {
	if len(a.state.Queue) > 0 {
		a.state.CurrentAnim = a.state.Queue[0]
		a.state.Queue = a.state.Queue[1:]
		a.state.Frame = 0
	} else if a.loopMode {
		a.state.Frame = 0
	} else {
		// Fire callback before returning to idle
		if a.onComplete != nil {
			cb := a.onComplete
			a.onComplete = nil
			cb()
			return
		}
		// Pick next idle animation randomly
		a.advanceIdleSequence()
	}
}

// advanceIdleSequence picks the next idle animation randomly (80% wondering, 20% coffee)
func (a *AnimationSystem) advanceIdleSequence() {
	if rand.Float64() < 0.2 {
		a.state.CurrentAnim = AnimCoffee
	} else {
		a.state.CurrentAnim = AnimWondering
	}
	a.state.Frame = 0
}

// StartIdleSequence starts an idle animation (random pick)
func (a *AnimationSystem) StartIdleSequence() {
	if rand.Float64() < 0.2 {
		a.state.CurrentAnim = AnimCoffee
	} else {
		a.state.CurrentAnim = AnimWondering
	}
	a.state.Frame = 0
	a.state.Timer = 0
	a.state.Queue = nil
	a.onComplete = nil
	a.loopMode = false
}

// SetLoopMode enables/disables loop mode
func (a *AnimationSystem) SetLoopMode(enabled bool) {
	a.loopMode = enabled
}

// SetOnComplete sets a callback for when the current animation finishes (non-loop mode)
func (a *AnimationSystem) SetOnComplete(cb func()) {
	a.onComplete = cb
}

// SetAnimation sets the current animation directly
func (a *AnimationSystem) SetAnimation(anim AnimationType) {
	a.state.CurrentAnim = anim
	a.state.Frame = 0
	a.state.Timer = 0
	a.state.Queue = nil
	a.onComplete = nil
}

// GetState returns the current animation state for rendering
func (a *AnimationSystem) GetState() *AnimationState {
	return a.state
}

// GetAnimationLength returns the frame count for the current animation
func (a *AnimationSystem) GetAnimationLength() int {
	return a.animLengths[a.state.CurrentAnim]
}

// SetFrame sets the current frame directly (for debug stepping)
func (a *AnimationSystem) SetFrame(frame int) {
	animLen := a.animLengths[a.state.CurrentAnim]
	if frame < 0 {
		frame = animLen - 1
	} else if frame >= animLen {
		frame = 0
	}
	a.state.Frame = frame
	a.state.Timer = 0
}

// StepFrame advances or rewinds by one frame (for debug stepping)
func (a *AnimationSystem) StepFrame(delta int) {
	a.SetFrame(a.state.Frame + delta)
}

// GetAllAnimations returns all available animation types
func (a *AnimationSystem) GetAllAnimations() []AnimationType {
	return []AnimationType{
		AnimCoffee, AnimWave, AnimPumpUp, AnimChairDips, AnimArmCircles, AnimWondering,
		AnimKneeRaises, AnimSpinalTwist, AnimGluteSqueeze, AnimShoulderRolls, AnimLegExtensions, AnimNeckStretch,
		AnimDeskPushUps, AnimSquats, AnimCalfRaises, AnimWallSit, AnimTorsoRotation, AnimReverseLunges,
	}
}
