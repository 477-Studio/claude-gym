package main

import (
	"fmt"
	"os"
	"time"

	rl "github.com/gen2brain/raylib-go/raylib"
)

const (
	screenWidth  = 320
	screenHeight = 200
	windowScale  = 2
	windowTitle  = "Claude Gym"
)

// AppState tracks minimal state for Claude Gym
type AppState struct {
	IsActive         bool
	LastActivityTime float32
}

func NewAppState() *AppState {
	return &AppState{}
}

func (s *AppState) Update(dt float32) {
	if s.IsActive {
		s.LastActivityTime += dt
		if s.LastActivityTime > 60.0 {
			s.IsActive = false
		}
	}
}

func (s *AppState) HandleEvent(event Event) {
	if event.Type != EventIdle {
		s.LastActivityTime = 0
		s.IsActive = true
	}
}

// getScaledDestRect calculates destination rectangle that maintains aspect ratio
func getScaledDestRect() rl.Rectangle {
	windowW := float32(rl.GetScreenWidth())
	windowH := float32(rl.GetScreenHeight())

	scaleX := windowW / float32(screenWidth)
	scaleY := windowH / float32(screenHeight)
	scale := scaleX
	if scaleY < scaleX {
		scale = scaleY
	}

	scaledW := float32(screenWidth) * scale
	scaledH := float32(screenHeight) * scale
	offsetX := (windowW - scaledW) / 2
	offsetY := (windowH - scaledH) / 2

	return rl.Rectangle{X: offsetX, Y: offsetY, Width: scaledW, Height: scaledH}
}

func printUsage() {
	fmt.Println(`Claude Gym - Exercise Reminder for Claude Code Users

Usage:
  cgym                    Watch the current directory's latest conversation
  cgym watch [dir]        Watch a specific directory's conversation
  cgym replay <file>      Replay an existing conversation JSONL file

Options:
  -s, --speed <ms>      Replay speed in milliseconds (default: 200)
  -h, --help            Show this help message`)
}

func main() {
	watcher := NewWatcher()
	var err error

	args := os.Args[1:]

	if len(args) == 0 {
		cwd, _ := os.Getwd()
		err = watcher.FindProjectConversation(cwd)
		if err != nil {
			fmt.Fprintf(os.Stderr, "Error: %v\n", err)
			os.Exit(1)
		}
		err = watcher.StartLive()
	} else {
		switch args[0] {
		case "-h", "--help", "help":
			printUsage()
			os.Exit(0)

		case "watch":
			dir := "."
			if len(args) > 1 {
				dir = args[1]
			}
			err = watcher.FindProjectConversation(dir)
			if err != nil {
				fmt.Fprintf(os.Stderr, "Error: %v\n", err)
				os.Exit(1)
			}
			err = watcher.StartLive()

		case "replay":
			if len(args) < 2 {
				fmt.Fprintln(os.Stderr, "Error: replay requires a file path")
				printUsage()
				os.Exit(1)
			}
			filePath := args[1]

			for i := 2; i < len(args); i++ {
				if args[i] == "-s" || args[i] == "--speed" {
					if i+1 < len(args) {
						var speed int
						fmt.Sscanf(args[i+1], "%d", &speed)
						if speed > 0 {
							watcher.ReplaySpeed = time.Duration(speed) * time.Millisecond
						}
					}
				}
			}

			err = watcher.StartReplay(filePath)

		case "studio":
			runStudio()
			os.Exit(0)

		default:
			err = watcher.FindProjectConversation(args[0])
			if err != nil {
				fmt.Fprintf(os.Stderr, "Error: %v\n", err)
				os.Exit(1)
			}
			err = watcher.StartLive()
		}
	}

	if err != nil {
		fmt.Fprintf(os.Stderr, "Error: %v\n", err)
		os.Exit(1)
	}

	fmt.Printf("Watching: %s\n", watcher.FilePath)

	rl.SetConfigFlags(rl.FlagWindowResizable)
	rl.InitWindow(screenWidth*windowScale, screenHeight*windowScale, windowTitle)
	defer rl.CloseWindow()

	rl.SetExitKey(0) // Disable Esc closing the window — we use Esc for menu navigation
	rl.SetTargetFPS(60)

	target := rl.LoadRenderTexture(screenWidth, screenHeight)
	defer rl.UnloadRenderTexture(target)

	config := LoadConfig("config.json")
	renderer := NewRenderer(config)
	animations := NewAnimationSystem()
	appState := NewAppState()

	// Load exercises
	exercisePath := getAssetPath("../exercises.json")
	exercises, exErr := LoadExercises(exercisePath)
	if exErr != nil {
		// Try current directory
		exercises, exErr = LoadExercises("exercises.json")
		if exErr != nil {
			fmt.Fprintf(os.Stderr, "Warning: %v (using defaults)\n", exErr)
			exercises = []ExerciseConfig{
				{Name: "Chair Dips", AnimRow: 3, Reps: "10 reps"},
				{Name: "Arm Circles", AnimRow: 4, Reps: "20 forward + 20 backward"},
			}
		}
	}

	menuState := NewMenuState(exercises)
	exerciseLog := LoadExerciseLog()
	menuState.ExerciseLog = exerciseLog

	for !rl.WindowShouldClose() {
		dt := rl.GetFrameTime()

		// Process events from watcher
		select {
		case event := <-watcher.Events:
			appState.HandleEvent(event)
			menuState.HandleEvent(event, animations)
		default:
		}

		// Handle input — menu takes priority
		menuState.HandleInput(animations)

		// Update systems
		animations.Update(dt)
		appState.Update(dt)
		menuState.Update(dt, animations)
		renderer.UpdateTimer(dt)

		// Sync cat alert state to renderer
		renderer.CatAlert = menuState.CatAlert
		renderer.CatAlertText = menuState.CatAlertText
		renderer.CatPaused = menuState.Mode == ModePaused

		// Render to texture at native resolution
		rl.BeginTextureMode(target)
		rl.ClearBackground(rl.Color{R: 24, G: 20, B: 37, A: 255})
		renderer.Draw(animations.GetState(), menuState)
		rl.EndTextureMode()

		// Draw scaled texture to window
		rl.BeginDrawing()
		rl.ClearBackground(rl.Black)

		sourceRec := rl.Rectangle{X: 0, Y: float32(screenHeight), Width: float32(screenWidth), Height: -float32(screenHeight)}
		destRec := getScaledDestRect()
		rl.DrawTexturePro(target.Texture, sourceRec, destRec, rl.Vector2{}, 0, rl.White)

		rl.EndDrawing()
	}
}
