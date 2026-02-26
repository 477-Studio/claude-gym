//go:build debug

package main

import (
	"fmt"
	"os"
	"path/filepath"
	"strings"
	"time"

	"github.com/fsnotify/fsnotify"
	rl "github.com/gen2brain/raylib-go/raylib"
)

// HotReloader watches asset files and triggers reloads
type HotReloader struct {
	watcher     *fsnotify.Watcher
	renderer    *Renderer
	reloadQueue chan string
}

// NewHotReloader creates a new hot reloader for the given renderer
func NewHotReloader(renderer *Renderer) (*HotReloader, error) {
	watcher, err := fsnotify.NewWatcher()
	if err != nil {
		return nil, fmt.Errorf("failed to create watcher: %w", err)
	}

	hr := &HotReloader{
		watcher:     watcher,
		renderer:    renderer,
		reloadQueue: make(chan string, 100),
	}

	return hr, nil
}

// Start begins watching for file changes
func (hr *HotReloader) Start() error {
	// Watch assets directory recursively
	assetsPath := "assets"
	err := filepath.Walk(assetsPath, func(path string, info os.FileInfo, err error) error {
		if err != nil {
			return nil // Skip errors
		}
		if info.IsDir() {
			if watchErr := hr.watcher.Add(path); watchErr != nil {
				fmt.Printf("Warning: couldn't watch %s: %v\n", path, watchErr)
			}
		}
		return nil
	})
	if err != nil {
		fmt.Printf("Warning: couldn't walk assets directory: %v\n", err)
	}

	// Start the watcher goroutine
	go hr.watchLoop()

	fmt.Println("Hot reload enabled - watching assets/")
	fmt.Println("  Press R to force reload all textures")

	return nil
}

// watchLoop handles file system events
func (hr *HotReloader) watchLoop() {
	// Debounce timer to avoid multiple reloads for the same file
	debounce := make(map[string]time.Time)
	debounceInterval := 100 * time.Millisecond

	for {
		select {
		case event, ok := <-hr.watcher.Events:
			if !ok {
				return
			}

			// Only care about writes and creates
			if event.Op&(fsnotify.Write|fsnotify.Create) == 0 {
				continue
			}

			// Debounce
			if lastTime, exists := debounce[event.Name]; exists {
				if time.Since(lastTime) < debounceInterval {
					continue
				}
			}
			debounce[event.Name] = time.Now()

			// Check what kind of file changed
			ext := strings.ToLower(filepath.Ext(event.Name))

			if ext == ".png" {
				// PNG file changed - queue for reload
				fmt.Printf("Asset changed: %s\n", event.Name)
				hr.reloadQueue <- event.Name
			}

		case err, ok := <-hr.watcher.Errors:
			if !ok {
				return
			}
			fmt.Printf("Watcher error: %v\n", err)
		}
	}
}

// ProcessReloads should be called from the main thread to process pending reloads
// Returns true if any textures were reloaded
func (hr *HotReloader) ProcessReloads() bool {
	reloaded := false

	// Process all pending reloads (non-blocking)
	for {
		select {
		case path := <-hr.reloadQueue:
			hr.reloadTexture(path)
			reloaded = true
		default:
			return reloaded
		}
	}
}

// reloadTexture reloads a specific texture based on its path
func (hr *HotReloader) reloadTexture(path string) {
	// Normalize the path
	path = filepath.Clean(path)

	// Reload spritesheet if it matches
	if strings.Contains(path, "spritesheet.png") {
		if hr.renderer.spriteSheet.ID != 0 {
			rl.UnloadTexture(hr.renderer.spriteSheet)
		}
		hr.renderer.spriteSheet = rl.LoadTexture(path)
		hr.renderer.hasSprites = true
		fmt.Printf("Reloaded: spritesheet\n")
	} else {
		fmt.Printf("Unknown asset type, skipping: %s\n", path)
	}
}

// ForceReloadAll reloads all textures
func (hr *HotReloader) ForceReloadAll() {
	fmt.Println("Force reloading all textures...")

	// Queue sprite sheet
	hr.reloadQueue <- getAssetPath("developer/exercise_spritesheet.png")
}

// Stop stops the hot reloader
func (hr *HotReloader) Stop() {
	if hr.watcher != nil {
		hr.watcher.Close()
	}
}
