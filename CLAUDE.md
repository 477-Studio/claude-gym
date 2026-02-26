# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Build Commands

```bash
go build -o cgym .              # Build binary for current platform
./cgym                          # Watch current project's Claude conversations
./cgym watch ~/path/to/project  # Watch specific project
./cgym replay <jsonl-file>      # Replay a conversation file

# Studio mode - asset development with hot reload (not included in release)
go build -tags debug -o cgym . && ./cgym studio
```

## Build Requirements

- **CGO_ENABLED=1** (Raylib needs C bindings)
- **Linux deps**: libgl1-mesa-dev, libxi-dev, libxcursor-dev, libxrandr-dev, libxinerama-dev, libxxf86vm-dev, libwayland-dev, libxkbcommon-dev

## Architecture

Claude Gym is an exercise reminder companion for Claude Code users. It watches JSONL conversation logs and prompts the user to do exercises during natural pause points (plan mode, permission escalations). Features a pixel-art developer character in a home office biome.

### Core Components

**main.go** - Entry point with CLI parsing (`watch`, `replay`, `studio` subcommands). Contains the main game loop, `AppState`, and event handling.

**menu.go** - State machine for the exercise flow: Idle → Menu → Prompting → PumpUp → Exercising → StopConfirm → Summary. Handles all keyboard input per mode. Exercise mode is fully isolated — no external events can interrupt it.

**exercises.go** - Exercise config loader. Reads `exercises.json` for exercise definitions (name, animation row, reps, bubble text).

**animations.go** - Animation state machine managing animation types: Idle, CoffeeSip, Wave, PumpUp, ChairDips, ArmCircles. Each has frame timing, loop mode, and optional completion callbacks.

**watcher.go** - File watcher that monitors `~/.claude/projects/[encoded-path]/*.jsonl`. Parses JSON lines, extracts events, and emits typed `Event` structs through a channel. Supports live tailing and replay modes.

### Renderer Architecture

**renderer.go** - Core renderer struct, initialization, and main Draw loop. Loads `assets/developer/exercise_spritesheet.png`. The `ClaudeOffsetX` field allows biomes to shift the character horizontally.

**renderer_claude.go** - Character sprite drawing: `drawClaude` (sprite sheet rendering with offset support), `drawPlaceholderClaude` (fallback when no sprites loaded).

**renderer_ui.go** - UI overlays: idle hint, menu overlay, exercise prompt bubble, speech bubbles, stop confirmation banner, exercise summary screen.

**biome_office.go** - Home office background: ceiling, wall, bookshelf, window with drifting clouds, dual monitors with scrolling code, desk with keyboard/mug/plant, office chair, sleeping cat, hardwood floor.

### Studio Mode (debug build only)

**studio.go** - Development environment for testing animations. Animation picker, pause/play, frame stepping, speed control.

**hot_reload.go** - Watches `assets/` directory. Auto-reloads textures when PNG files change.

**studio_stub.go** - Empty stub for non-debug builds.

### Sprite Generation

**cmd/devsprite/** - Python scripts that generate the exercise spritesheet:
- `generate.py` - Base developer character (32x32)
- `generate_exercises.py` - Exercise animation spritesheet

### Event Flow

1. Watcher parses JSONL and emits `Event{Type, Details, ...}`
2. `MenuState.HandleEvent()` checks for plan_start/permission_escalation events (only when idle, respects cooldown)
3. If triggered, character waves and prompts "Time to exercise!"
4. User accepts → PumpUp animation → Exercise loop (Tab to advance, Esc → Enter to stop)

## Key Constants

- Screen: 320x200 pixels
- Character: 32x32 pixel frames, scaled 2x
- Window: resizable, maintains aspect ratio

## Studio Mode Controls

```bash
go build -tags debug -o cgym . && ./cgym studio
```

| Key | Action |
|-----|--------|
| `Space` | Pause/play |
| `< >` (or `,` `.`) | Step frame back/forward (when paused) |
| `- +` | Speed down/up (0.125x to 4x) |
| `A` | Open animation picker |
| `R` | Force reload all textures |
| `H` | Toggle help |

## Distribution

npm package (`claude-gym`) with postinstall script (`scripts/install.js`) that downloads pre-built binaries from GitHub releases.

## Important Notes

- The office biome sets `ClaudeOffsetX = 20` to shift the character right so dual monitors are visible
- Exercise mode is completely isolated — no watcher events can interrupt it, only Esc → Enter stops it
- `config.json` holds display settings (scale, fullscreen, debug)
