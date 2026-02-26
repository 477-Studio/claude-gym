package main

import (
	"fmt"
	"os"
	"path/filepath"

	rl "github.com/gen2brain/raylib-go/raylib"
)

// getAssetPath returns the path to an asset file, checking both relative to
// the executable (for npm installs) and relative to cwd (for development)
func getAssetPath(relativePath string) string {
	if exe, err := os.Executable(); err == nil {
		exeDir := filepath.Dir(exe)
		if resolved, err := filepath.EvalSymlinks(exe); err == nil {
			exeDir = filepath.Dir(resolved)
		}
		npmAssetPath := filepath.Join(exeDir, "..", "assets", relativePath)
		if _, err := os.Stat(npmAssetPath); err == nil {
			return npmAssetPath
		}
		sameDirPath := filepath.Join(exeDir, "assets", relativePath)
		if _, err := os.Stat(sameDirPath); err == nil {
			return sameDirPath
		}
	}
	return filepath.Join("assets", relativePath)
}

const (
	spriteFrameWidth  = 32
	spriteFrameHeight = 32
	claudeScale       = 2
)

// Renderer handles all drawing operations
type Renderer struct {
	config      *Config
	spriteSheet rl.Texture2D
	hasSprites  bool

	// Biome timer (for animations like clock, code scroll)
	biomeTimer float32

	// ClaudeOffsetX allows biomes to shift the character horizontally
	ClaudeOffsetX float32

	// Cat alert state (synced from MenuState each frame)
	CatAlert     bool
	CatAlertText string
	CatPaused    bool // true when exercise is paused — cat sleeps even if alert
}

// NewRenderer creates a new renderer with loaded assets
func NewRenderer(config *Config) *Renderer {
	r := &Renderer{
		config: config,
	}

	// Load developer character sprite sheet
	spritePath := getAssetPath("developer/exercise_spritesheet.png")
	if _, err := os.Stat(spritePath); err == nil {
		r.spriteSheet = rl.LoadTexture(spritePath)
		r.hasSprites = true
		fmt.Println("Loaded sprite sheet from:", spritePath)
	} else {
		fmt.Println("No sprite sheet found, using placeholder graphics")
	}

	return r
}

// UpdateTimer advances the biome animation timer
func (r *Renderer) UpdateTimer(dt float32) {
	r.biomeTimer += dt
}

// Draw renders the current animation state with menu overlays
func (r *Renderer) Draw(state *AnimationState, menu *MenuState) {
	r.drawBackground()
	r.drawClaude(state)

	// UI overlays based on menu mode
	if menu != nil {
		switch menu.Mode {
		case ModeIdle:
			r.DrawIdleHint()
		case ModeMenu:
			r.DrawMenu(menu)
		case ModePrompting:
			r.DrawPromptBubble()
		case ModePumpUp:
			if ex := menu.GetCurrentExercise(); ex != nil {
				if menu.IsFirstExercise {
					r.DrawSpeechBubble("Let's start!")
				} else {
					r.DrawSpeechBubble("Next exercise!")
				}
			}
		case ModeCountdown:
			r.DrawCountdown(menu)
		case ModeExercising:
			if ex := menu.GetCurrentExercise(); ex != nil {
				r.DrawSpeechBubble(ex.BubbleText())
			}
			r.DrawExerciseHint()
		case ModePaused:
			if menu.PrevMode == ModeCountdown {
				r.DrawSpeechBubble("Get ready...")
			} else if ex := menu.GetCurrentExercise(); ex != nil {
				r.DrawSpeechBubble(ex.BubbleText())
			}
			r.DrawPauseBanner()
		case ModeSummary:
			r.DrawExerciseSummary(menu)
		case ModeExerciseLog:
			r.DrawExerciseLog(menu)
		}
	}

	if r.config.Debug {
		r.drawDebug(state)
	}
}

func (r *Renderer) drawBackground() {
	r.ClaudeOffsetX = 0
	r.drawBiomeOffice()
}

func (r *Renderer) drawDebug(state *AnimationState) {
	rl.DrawText(state.CurrentAnim.String(), 5, 5, 8, rl.Green)
	frameText := fmt.Sprintf("Frame: %d", state.Frame)
	rl.DrawText(frameText, 5, 15, 8, rl.Green)
	fpsText := fmt.Sprintf("FPS: %d", rl.GetFPS())
	rl.DrawText(fpsText, 5, 25, 8, rl.Green)
}

// Unload frees all loaded textures
func (r *Renderer) Unload() {
	if r.spriteSheet.ID != 0 {
		rl.UnloadTexture(r.spriteSheet)
	}
}
