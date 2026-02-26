package main

import rl "github.com/gen2brain/raylib-go/raylib"

func (r *Renderer) drawClaude(state *AnimationState) {
	scaledW := float32(spriteFrameWidth * claudeScale)
	scaledH := float32(spriteFrameHeight * claudeScale)

	// Position character in center of scene (biomes can shift via ClaudeOffsetX)
	x := float32(screenWidth/2) - scaledW/2 + r.ClaudeOffsetX
	y := float32(160) - scaledH + 10

	if r.hasSprites {
		frameX := float32(state.Frame * spriteFrameWidth)
		frameY := float32(int(state.CurrentAnim) * spriteFrameHeight)

		sourceRec := rl.Rectangle{
			X:      frameX,
			Y:      frameY,
			Width:  spriteFrameWidth,
			Height: spriteFrameHeight,
		}

		destRec := rl.Rectangle{
			X:      x,
			Y:      y,
			Width:  scaledW,
			Height: scaledH,
		}

		rl.DrawTexturePro(r.spriteSheet, sourceRec, destRec, rl.Vector2{}, 0, rl.White)
	} else {
		r.drawPlaceholderClaude(int(x), int(y), state)
	}
}

func (r *Renderer) drawPlaceholderClaude(x, y int, state *AnimationState) {
	color := rl.Color{R: 217, G: 119, B: 87, A: 255}
	bobOffset := 0
	if state.CurrentAnim == AnimCoffee || state.CurrentAnim == AnimWondering {
		bobOffset = int(state.Frame/10) % 2
	}
	rl.DrawRectangle(int32(x+8), int32(y+20), 16, 24, color)
	rl.DrawCircle(int32(x+16), int32(y+14+bobOffset), 10, color)
	rl.DrawCircle(int32(x+13), int32(y+12+bobOffset), 2, rl.White)
	rl.DrawCircle(int32(x+19), int32(y+12+bobOffset), 2, rl.White)
}
