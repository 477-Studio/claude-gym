package main

import (
	"fmt"
	"time"

	rl "github.com/gen2brain/raylib-go/raylib"
)

// ============================================================================
// BIOME: HOME OFFICE - Cozy single-person workspace
// Animated: code on monitor, steam from mug, plant sway, cloud drift, sleeping cat
// ============================================================================
func (r *Renderer) drawBiomeOffice() {
	time := r.biomeTimer

	// Shift character right so dual monitors are visible
	r.ClaudeOffsetX = 20

	// === CEILING (y=0-12) — warm off-white with wood trim ===
	for y := int32(0); y < 12; y++ {
		t := float32(y) / 12.0
		c := rl.Color{
			R: uint8(245 - t*8),
			G: uint8(238 - t*8),
			B: uint8(228 - t*8),
			A: 255,
		}
		rl.DrawLine(0, y, screenWidth, y, c)
	}
	// Wood trim
	rl.DrawRectangle(0, 12, screenWidth, 2, rl.Color{R: 165, G: 130, B: 90, A: 255})

	// === BACK WALL (y=14-138) — warm sage/beige gradient ===
	for y := int32(14); y < 138; y++ {
		t := float32(y-14) / 124.0
		c := rl.Color{
			R: uint8(210 - t*20),
			G: uint8(215 - t*18),
			B: uint8(200 - t*22),
			A: 255,
		}
		rl.DrawLine(0, y, screenWidth, y, c)
	}

	// === WALL ITEMS ===
	r.drawBookshelf(8, 30)
	r.drawOfficeWindow(85, 24, time)
	r.drawWallArt(240, 40)

	// === BEHIND-CHARACTER ITEMS (drawn before desk, behind Claude) ===
	// Dual monitors — left fully visible, right partially behind character
	r.drawMonitor(116, 100, time)
	r.drawMonitor(164, 100, time)
	r.drawOfficeChairBG(168, 142)

	// === DESK SURFACE (y=138-143) — compact desk ===
	deskX := int32(80)
	deskW := int32(160)
	// Top edge highlight
	rl.DrawRectangle(deskX, 138, deskW, 1, rl.Color{R: 185, G: 150, B: 110, A: 255})
	// Main surface
	rl.DrawRectangle(deskX, 139, deskW, 3, rl.Color{R: 165, G: 130, B: 92, A: 255})
	// Bottom edge shadow
	rl.DrawRectangle(deskX, 142, deskW, 1, rl.Color{R: 140, G: 108, B: 72, A: 255})

	// === DESK ITEMS ===
	r.drawDeskMug(90, 131, time)
	r.drawKeyboard(155, 139)
	r.drawDeskPlant(228, 126, time)

	// === DESK LEGS (below desk surface, y=143-162) ===
	legColor := rl.Color{R: 140, G: 108, B: 72, A: 255}
	legHighlight := rl.Color{R: 155, G: 122, B: 85, A: 255}
	// Left leg
	rl.DrawRectangle(85, 143, 3, 19, legColor)
	rl.DrawRectangle(85, 143, 4, 1, legHighlight)
	// Right leg
	rl.DrawRectangle(235, 143, 3, 19, legColor)
	rl.DrawRectangle(235, 143, 4, 1, legHighlight)

	// === FLOOR (y=162-200) — hardwood planks ===
	r.drawWoodFloor()

	// === CAT on floor ===
	if r.CatAlert && !r.CatPaused {
		r.drawJumpingCat(265, 155, time)
		r.drawCatAlertBanner(265, 155, r.CatAlertText)
	} else {
		r.drawSleepingCat(265, 155, time)
	}
}

// --- HOME OFFICE ELEMENTS ---

func (r *Renderer) drawBookshelf(x, y int32) {
	shelfW := int32(36)
	shelfH := int32(100)
	woodDark := rl.Color{R: 120, G: 80, B: 50, A: 255}
	woodMed := rl.Color{R: 140, G: 100, B: 65, A: 255}

	// Outer frame
	rl.DrawRectangle(x, y, shelfW, shelfH, woodDark)
	rl.DrawRectangle(x+2, y+2, shelfW-4, shelfH-4, woodMed)

	// 3 shelves
	shelfPositions := []int32{y + 2, y + 34, y + 66}
	shelfInnerH := int32(28)

	bookColors := []rl.Color{
		{R: 180, G: 60, B: 60, A: 255},   // red
		{R: 60, G: 100, B: 180, A: 255},   // blue
		{R: 60, G: 150, B: 80, A: 255},    // green
		{R: 200, G: 170, B: 60, A: 255},   // yellow
		{R: 140, G: 80, B: 160, A: 255},   // purple
		{R: 200, G: 120, B: 60, A: 255},   // orange
		{R: 100, G: 140, B: 160, A: 255},  // teal
		{R: 180, G: 100, B: 120, A: 255},  // pink
		{R: 100, G: 100, B: 100, A: 255},  // gray
		{R: 160, G: 140, B: 100, A: 255},  // tan
		{R: 80, G: 120, B: 60, A: 255},    // dark green
		{R: 170, G: 80, B: 80, A: 255},    // dark red
		{R: 90, G: 90, B: 150, A: 255},    // dark blue
		{R: 180, G: 150, B: 100, A: 255},  // khaki
		{R: 120, G: 60, B: 100, A: 255},   // dark purple
	}

	for s, sy := range shelfPositions {
		// Shelf background
		rl.DrawRectangle(x+3, sy+1, shelfW-6, shelfInnerH, rl.Color{R: 80, G: 55, B: 35, A: 255})

		// Books on this shelf
		bx := x + 4
		for b := 0; b < 5; b++ {
			ci := (s*5 + b) % len(bookColors)
			bookW := int32(4 + (b % 3))
			bookH := int32(shelfInnerH - 4 - int32(b%3)*2)
			bookY := sy + 1 + (shelfInnerH - bookH)
			rl.DrawRectangle(bx, bookY, bookW, bookH, bookColors[ci])
			// Spine highlight
			rl.DrawRectangle(bx, bookY, 1, bookH, rl.Color{
				R: uint8(min32(int32(bookColors[ci].R)+30, 255)),
				G: uint8(min32(int32(bookColors[ci].G)+30, 255)),
				B: uint8(min32(int32(bookColors[ci].B)+30, 255)),
				A: 255,
			})
			bx += bookW + 1
		}

		// Shelf plank
		rl.DrawRectangle(x+2, sy+shelfInnerH+1, shelfW-4, 3, woodDark)
	}
}

func (r *Renderer) drawOfficeWindow(x, y int32, time float32) {
	frameColor := rl.Color{R: 200, G: 195, B: 185, A: 255}
	winW := int32(90)
	winH := int32(70)

	// Outer frame
	rl.DrawRectangle(x, y, winW, winH, frameColor)

	// Window panes (2x2 grid)
	paneW := int32(41)
	paneH := int32(31)

	// Define pane positions
	tlX, tlY := x+2, y+2                       // top-left
	trX, trY := x+winW-2-paneW, y+2             // top-right
	blX, blY := x+2, y+winH-2-paneH             // bottom-left
	brX, brY := x+winW-2-paneW, y+winH-2-paneH // bottom-right

	// --- Golden Gate Bridge scene colors ---
	skyColor := rl.Color{R: 145, G: 200, B: 230, A: 255}
	hillColor := rl.Color{R: 120, G: 140, B: 100, A: 255}
	waterColor := rl.Color{R: 100, G: 140, B: 170, A: 255}
	towerColor := rl.Color{R: 190, G: 75, B: 50, A: 255}
	towerHighlight := rl.Color{R: 210, G: 95, B: 65, A: 255}
	towerShadow := rl.Color{R: 155, G: 55, B: 35, A: 255}
	cableColor := rl.Color{R: 175, G: 65, B: 45, A: 255}

	// Helper: draw bridge scene in a pane
	drawBridgePane := func(px, py, pw, ph int32, isBottom bool) {
		// Sky fill
		rl.DrawRectangle(px, py, pw, ph, skyColor)

		if isBottom {
			// Bottom panes: mostly water with tower bases
			waterTop := py + ph/4
			rl.DrawRectangle(px, waterTop, pw, ph-ph/4, waterColor)
			// Subtle horizontal water lines
			shimmerLight := rl.Color{R: 120, G: 160, B: 185, A: 50}
			for wy := waterTop + 3; wy < py+ph; wy += 4 {
				lx := px + int32(simpleSinF(float64(wy)*0.8))*2 + pw/4
				rl.DrawRectangle(lx, wy, 3, 1, shimmerLight)
			}

			// Bridge tower bases (extending from top of pane, 2px wide)
			t1x := px + pw/3 - 1
			t2x := px + pw*2/3 - 1
			rl.DrawRectangle(t1x, py, 2, ph/3, towerColor)
			rl.DrawRectangle(t1x, py, 1, ph/3, towerHighlight)
			rl.DrawRectangle(t1x+1, py, 1, ph/3, towerShadow)
			rl.DrawRectangle(t2x, py, 2, ph/3, towerColor)
			rl.DrawRectangle(t2x, py, 1, ph/3, towerShadow)
			rl.DrawRectangle(t2x+1, py, 1, ph/3, towerHighlight)

			// Suspender cables in bottom pane
			for sx := t1x + 3; sx < t2x; sx += 3 {
				rl.DrawPixel(sx, py, cableColor)
				rl.DrawPixel(sx, py+1, cableColor)
			}

			// Roadway/deck line across bottom pane (1px thick)
			deckY := py + ph/4 - 1
			rl.DrawRectangle(px, deckY, pw, 1, rl.Color{R: 175, G: 65, B: 45, A: 200})

			// Tower reflections in water (faint, broken dots under towers only)
			reflectColor := rl.Color{R: 155, G: 65, B: 50, A: 55}
			for ry := deckY + 2; ry < deckY+8 && ry < py+ph-1; ry += 3 {
				rl.DrawPixel(t1x, ry, reflectColor)
				rl.DrawPixel(t2x+1, ry, reflectColor)
			}
		} else {
			// Top panes: sky, hills, water strip, towers, cables
			// Distant hills
			hillY := py + ph - 8
			rl.DrawRectangle(px, hillY, pw, 4, hillColor)
			// Hill undulations
			for hx := int32(0); hx < pw; hx += 3 {
				bump := int32(simpleSinF(float64(hx)*0.7)) * 1
				rl.DrawPixel(px+hx, hillY-1+bump, hillColor)
				rl.DrawPixel(px+hx+1, hillY-1+bump, hillColor)
			}

			// Water at bottom of top panes (lightened horizon for depth)
			horizonWater := rl.Color{R: 125, G: 175, B: 205, A: 255}
			rl.DrawRectangle(px, py+ph-4, pw, 4, horizonWater)

			// Bridge towers (2px wide, taller)
			towerH := int32(17)
			t1x := px + pw/3 - 1
			t2x := px + pw*2/3 - 1
			towerBase := py + ph - 4
			rl.DrawRectangle(t1x, towerBase-towerH, 2, towerH, towerColor)
			rl.DrawRectangle(t1x, towerBase-towerH, 1, towerH, towerHighlight)
			rl.DrawRectangle(t1x+1, towerBase-towerH, 1, towerH, towerShadow)
			rl.DrawRectangle(t2x, towerBase-towerH, 2, towerH, towerColor)
			rl.DrawRectangle(t2x, towerBase-towerH, 1, towerH, towerShadow)
			rl.DrawRectangle(t2x+1, towerBase-towerH, 1, towerH, towerHighlight)

			// Tower cross-beams
			beamY1 := towerBase - towerH + 4
			beamY2 := towerBase - towerH/2
			rl.DrawRectangle(t1x, beamY1, 2, 1, towerHighlight)
			rl.DrawRectangle(t2x, beamY1, 2, 1, towerHighlight)
			rl.DrawRectangle(t1x, beamY2, 2, 1, towerHighlight)
			rl.DrawRectangle(t2x, beamY2, 2, 1, towerHighlight)

			// Suspension cables between towers
			t1cx := t1x + 1
			t2cx := t2x
			cableTopY := towerBase - towerH + 1
			span := t2cx - t1cx
			for cx := int32(0); cx <= span; cx++ {
				// Parabolic droop
				t := float32(cx) / float32(span)
				droop := int32(4.0 * t * (1.0 - t) * 7.0)
				rl.DrawPixel(t1cx+cx, cableTopY+droop, cableColor)
			}

			// Vertical suspender cables between towers
			deckY := towerBase - 4
			for cx := int32(3); cx < span; cx += 3 {
				t := float32(cx) / float32(span)
				cableY := cableTopY + int32(4.0*t*(1.0-t)*7.0)
				for sy := cableY; sy <= deckY; sy++ {
					rl.DrawPixel(t1cx+cx, sy, cableColor)
				}
			}

			// Cable to left pane edge
			leftSpan := t1cx - px
			for cx := int32(0); cx < leftSpan; cx++ {
				t := float32(cx) / float32(leftSpan)
				droop := int32((1.0 - t) * 5.0)
				rl.DrawPixel(px+cx, cableTopY+droop, cableColor)
			}

			// Cable to right pane edge
			rightStart := t2cx
			rightSpan := (px + pw) - rightStart
			for cx := int32(0); cx < rightSpan; cx++ {
				t := float32(cx) / float32(rightSpan)
				droop := int32(t * 5.0)
				rl.DrawPixel(rightStart+cx, cableTopY+droop, cableColor)
			}
		}
	}

	// Draw all four panes with bridge scene
	drawBridgePane(tlX, tlY, paneW, paneH, false)
	drawBridgePane(trX, trY, paneW, paneH, false)
	drawBridgePane(blX, blY, paneW, paneH, true)
	drawBridgePane(brX, brY, paneW, paneH, true)

	// Cross dividers
	rl.DrawRectangle(x+paneW+2, y+2, winW-4-paneW*2, winH-4, frameColor)
	rl.DrawRectangle(x+2, y+paneH+2, winW-4, winH-4-paneH*2, frameColor)

	// Drifting cloud (adjusted for wider panes)
	cloudX := int32(simpleSinF(float64(time*0.08)) * 15)
	rl.DrawRectangle(x+15+cloudX, y+8, 12, 3, rl.Color{R: 245, G: 245, B: 248, A: 180})
	rl.DrawRectangle(x+13+cloudX, y+10, 16, 3, rl.Color{R: 245, G: 245, B: 248, A: 150})
	rl.DrawRectangle(x+16+cloudX, y+12, 10, 2, rl.Color{R: 245, G: 245, B: 248, A: 120})

	// Sunlight glow on bottom panes
	for py := y + winH - 2 - paneH; py < y+winH-2; py++ {
		alpha := uint8(40 - 30*float32(py-(y+winH-2-paneH))/float32(paneH))
		rl.DrawRectangle(x+2, py, paneW, 1, rl.Color{R: 255, G: 250, B: 220, A: alpha})
	}

	// Window sill
	rl.DrawRectangle(x-2, y+winH, winW+4, 3, rl.Color{R: 185, G: 180, B: 170, A: 255})
}

func (r *Renderer) drawWallArt(x, y int32) {
	bezelW := int32(94)
	bezelH := int32(18)
	bezelColor := rl.Color{R: 45, G: 45, B: 50, A: 255}
	screenColor := rl.Color{R: 15, G: 20, B: 15, A: 255}
	lcdGreen := rl.Color{R: 0, G: 220, B: 80, A: 255}

	// Center the wider display at the original call site
	cx := x + (24-bezelW)/2

	// Dark plastic bezel
	rl.DrawRectangle(cx, y, bezelW, bezelH, bezelColor)
	// Inner LCD screen
	screenX := cx + 2
	screenW := bezelW - 4
	rl.DrawRectangle(screenX, y+2, screenW, bezelH-4, screenColor)
	// Wall-mount shadow
	rl.DrawRectangle(cx+1, y+bezelH, bezelW-2, 1, rl.Color{R: 35, G: 35, B: 38, A: 255})

	// Live UTC time
	now := time.Now().UTC()
	dateLine := fmt.Sprintf("UTC %04d-%02d-%02d", now.Year(), now.Month(), now.Day())
	timeLine := fmt.Sprintf("%02d:%02d:%02d", now.Hour(), now.Minute(), now.Second())

	dateW := rl.MeasureText(dateLine, 8)
	dateX := screenX + (screenW-dateW)/2
	rl.DrawText(dateLine, dateX, y+3, 8, lcdGreen)
	timeW := rl.MeasureText(timeLine, 8)
	timeX := screenX + (screenW-timeW)/2
	rl.DrawText(timeLine, timeX, y+10, 8, lcdGreen)
}

func (r *Renderer) drawMonitor(x, y int32, time float32) {
	// Stand
	rl.DrawRectangle(x+16, y+30, 8, 8, rl.Color{R: 70, G: 70, B: 75, A: 255})
	rl.DrawRectangle(x+12, y+37, 16, 3, rl.Color{R: 80, G: 80, B: 85, A: 255})
	// Bezel
	rl.DrawRectangle(x, y, 40, 30, rl.Color{R: 45, G: 45, B: 50, A: 255})
	// Screen
	rl.DrawRectangle(x+2, y+2, 36, 26, rl.Color{R: 30, G: 35, B: 45, A: 255})

	// Code lines with slow scroll
	codeScroll := int32(time * 0.5)
	lineColors := []rl.Color{
		{R: 100, G: 200, B: 130, A: 255}, // green
		{R: 180, G: 180, B: 200, A: 255}, // gray
		{R: 220, G: 170, B: 100, A: 255}, // orange
		{R: 130, G: 170, B: 220, A: 255}, // blue
		{R: 180, G: 180, B: 200, A: 255}, // gray
		{R: 200, G: 120, B: 160, A: 255}, // pink
	}
	for i := int32(0); i < 8; i++ {
		lineY := y + 4 + i*3
		lineIdx := (i + codeScroll) % int32(len(lineColors))
		c := lineColors[lineIdx]
		indent := int32(((i + codeScroll/2) % 3) * 3)
		lineW := int32(10 + ((i*7 + codeScroll) % 15))
		if lineW > 30 {
			lineW = 30
		}
		rl.DrawRectangle(x+4+indent, lineY, lineW, 1, c)
	}

	// Cursor blink
	if int32(time)%2 == 0 {
		cursorY := y + 4 + 6*3
		rl.DrawRectangle(x+8, cursorY, 2, 2, rl.Color{R: 200, G: 200, B: 220, A: 255})
	}
}

func (r *Renderer) drawKeyboard(x, y int32) {
	rl.DrawRectangle(x, y, 36, 4, rl.Color{R: 60, G: 60, B: 65, A: 255})
	rl.DrawRectangle(x+1, y, 34, 3, rl.Color{R: 75, G: 75, B: 80, A: 255})
	for row := int32(0); row < 2; row++ {
		for col := int32(0); col < 8; col++ {
			kx := x + 2 + col*4
			ky := y + row*2
			rl.DrawPixel(kx, ky, rl.Color{R: 90, G: 90, B: 95, A: 255})
			rl.DrawPixel(kx+1, ky, rl.Color{R: 95, G: 95, B: 100, A: 255})
		}
	}
}

func (r *Renderer) drawDeskMug(x, y int32, time float32) {
	mugColor := rl.Color{R: 230, G: 230, B: 225, A: 255}
	mugShadow := rl.Color{R: 200, G: 200, B: 195, A: 255}
	rl.DrawRectangle(x, y, 7, 8, mugColor)
	rl.DrawRectangle(x, y+7, 7, 1, mugShadow)
	// Coffee inside
	rl.DrawRectangle(x+1, y, 5, 2, rl.Color{R: 90, G: 55, B: 25, A: 255})
	// Handle
	rl.DrawPixel(x+7, y+2, mugShadow)
	rl.DrawPixel(x+8, y+3, mugShadow)
	rl.DrawPixel(x+8, y+4, mugShadow)
	rl.DrawPixel(x+7, y+5, mugShadow)
	// Gentle steam
	sway := int32(simpleSinF(float64(time*0.8)) * 2)
	alpha1 := uint8(100 + 50*simpleSinF(float64(time*1.2)))
	alpha2 := uint8(80 + 40*simpleSinF(float64(time*1.2+1)))
	rl.DrawPixel(x+2+sway, y-2, rl.Color{R: 200, G: 200, B: 210, A: alpha1})
	rl.DrawPixel(x+4-sway, y-3, rl.Color{R: 200, G: 200, B: 210, A: alpha2})
	rl.DrawPixel(x+3+sway, y-4, rl.Color{R: 200, G: 200, B: 210, A: alpha1 / 2})
}

func (r *Renderer) drawDeskPlant(x, y int32, time float32) {
	potColor := rl.Color{R: 180, G: 100, B: 70, A: 255}
	potDark := rl.Color{R: 150, G: 80, B: 55, A: 255}
	rl.DrawRectangle(x, y+6, 10, 7, potColor)
	rl.DrawRectangle(x-1, y+5, 12, 2, potDark)
	// Soil
	rl.DrawRectangle(x+1, y+5, 8, 1, rl.Color{R: 60, G: 45, B: 30, A: 255})
	// Leaves with sway
	sway := int32(simpleSinF(float64(time*0.5)) * 1)
	leafGreen := rl.Color{R: 60, G: 140, B: 70, A: 255}
	leafLight := rl.Color{R: 80, G: 170, B: 90, A: 255}
	// Stem
	rl.DrawPixel(x+5, y+4, leafGreen)
	rl.DrawPixel(x+5, y+3, leafGreen)
	rl.DrawPixel(x+5, y+2, leafGreen)
	// Left leaves
	rl.DrawPixel(x+3+sway, y+1, leafGreen)
	rl.DrawPixel(x+2+sway, y, leafLight)
	// Right leaves
	rl.DrawPixel(x+7-sway, y+1, leafGreen)
	rl.DrawPixel(x+8-sway, y, leafLight)
	// Top leaves
	rl.DrawPixel(x+4+sway, y-1, leafLight)
	rl.DrawPixel(x+6-sway, y-1, leafGreen)
	rl.DrawPixel(x+5, y-2, leafLight)
}

func (r *Renderer) drawOfficeChairBG(x, y int32) {
	// Chair back (visible above seat, behind character)
	chairColor := rl.Color{R: 55, G: 55, B: 60, A: 255}
	chairLight := rl.Color{R: 65, G: 65, B: 70, A: 255}

	// Back rest
	rl.DrawRectangle(x, y-18, 16, 18, chairColor)
	rl.DrawRectangle(x+1, y-17, 14, 16, chairLight)

	// Seat (partially visible)
	rl.DrawRectangle(x-4, y, 24, 4, chairColor)
}

func (r *Renderer) drawSleepingCat(x, y int32, time float32) {
	catColor := rl.Color{R: 80, G: 75, B: 70, A: 255}
	catLight := rl.Color{R: 100, G: 95, B: 88, A: 255}

	// Breathing: gentle vertical pulse
	breathe := int32(simpleSinF(float64(time*0.6)) * 1)

	// Curled body (oval shape)
	rl.DrawRectangle(x, y+2+breathe, 14, 6, catColor)
	rl.DrawRectangle(x+1, y+1+breathe, 12, 8, catColor)
	// Lighter belly highlight
	rl.DrawRectangle(x+3, y+3+breathe, 8, 4, catLight)

	// Head (tucked in)
	rl.DrawRectangle(x-1, y+1+breathe, 5, 5, catColor)
	// Ear
	rl.DrawPixel(x-1, y+breathe, catColor)
	rl.DrawPixel(x+2, y+breathe, catColor)

	// Tail with wag
	tailWag := int32(simpleSinF(float64(time*1.0)) * 2)
	rl.DrawPixel(x+13, y+4+breathe, catColor)
	rl.DrawPixel(x+14, y+3+breathe+tailWag, catColor)
	rl.DrawPixel(x+15, y+2+breathe+tailWag, catColor)

	// Zzz
	zFloat := simpleSinF(float64(time * 0.4))
	zAlpha := uint8(120 + 60*zFloat)
	zY := y - 3 + int32(zFloat*2)
	rl.DrawPixel(x+4, zY, rl.Color{R: 180, G: 180, B: 200, A: zAlpha})
	rl.DrawPixel(x+5, zY-1, rl.Color{R: 180, G: 180, B: 200, A: zAlpha})
}

func (r *Renderer) drawJumpingCat(x, y int32, time float32) {
	catColor := rl.Color{R: 80, G: 75, B: 70, A: 255}
	catLight := rl.Color{R: 100, G: 95, B: 88, A: 255}

	// Bounce animation
	bounce := int32(simpleSinF(float64(time*4.0)) * 10)
	if bounce > 0 {
		bounce = 0 // only jump up, not down through floor
	}

	by := y + bounce // bounced y position

	// Body (upright, standing)
	rl.DrawRectangle(x+2, by-4, 8, 10, catColor)
	rl.DrawRectangle(x+3, by-3, 6, 8, catLight)

	// Head (on top)
	rl.DrawRectangle(x+1, by-9, 10, 6, catColor)
	rl.DrawRectangle(x+2, by-8, 8, 4, catLight)

	// Ears (triangular)
	rl.DrawPixel(x+1, by-10, catColor)
	rl.DrawPixel(x+2, by-10, catColor)
	rl.DrawPixel(x+9, by-10, catColor)
	rl.DrawPixel(x+10, by-10, catColor)

	// Eyes (wide open, alert!)
	eyeColor := rl.Color{R: 220, G: 200, B: 60, A: 255} // bright yellow
	rl.DrawPixel(x+3, by-7, eyeColor)
	rl.DrawPixel(x+8, by-7, eyeColor)

	// Front legs
	rl.DrawRectangle(x+3, by+6, 2, 4, catColor)
	rl.DrawRectangle(x+7, by+6, 2, 4, catColor)

	// Tail (up and alert)
	tailWag := int32(simpleSinF(float64(time*3.0)) * 2)
	rl.DrawPixel(x+10, by-2, catColor)
	rl.DrawPixel(x+11, by-3, catColor)
	rl.DrawPixel(x+12+tailWag, by-4, catColor)
	rl.DrawPixel(x+13+tailWag, by-5, catColor)

	// Exclamation mark above head (blinks)
	if int32(time*3)%2 == 0 {
		rl.DrawRectangle(x+5, by-14, 2, 3, rl.Color{R: 255, G: 220, B: 60, A: 255})
		rl.DrawRectangle(x+5, by-10, 2, 1, rl.Color{R: 255, G: 220, B: 60, A: 255})
	}
}

func (r *Renderer) drawCatAlertBanner(x, y int32, text string) {
	fontSize := int32(8)
	padding := int32(8)
	lineSpacing := int32(2)

	// Split text into two lines: "Claude Code" on top, rest on bottom
	line1 := "Claude Code"
	line2 := ""
	if text == "Claude Code is done!" {
		line2 = "is done!"
	} else if text == "Claude Code needs you!" {
		line2 = "needs you!"
	} else {
		line1 = text
	}

	line1W := rl.MeasureText(line1, fontSize)
	line2W := rl.MeasureText(line2, fontSize)
	maxW := line1W
	if line2W > maxW {
		maxW = line2W
	}

	bannerW := maxW + padding*2
	bannerH := fontSize*2 + lineSpacing + padding*2

	// Position banner above cat
	bx := x + 6 - bannerW/2
	by := y - 65

	// Clamp to screen bounds
	if bx < 2 {
		bx = 2
	}
	if bx+bannerW > screenWidth-2 {
		bx = screenWidth - 2 - bannerW
	}

	// Claude Code orange/terracotta for text
	claudeColor := rl.Color{R: 217, G: 119, B: 60, A: 255}
	borderColor := rl.Color{R: 180, G: 180, B: 170, A: 255}

	// Same style as exercise speech bubble
	rl.DrawRectangle(bx, by, bannerW, bannerH, bubbleBgColor)
	rl.DrawRectangleLines(bx, by, bannerW, bannerH, borderColor)

	// Tail pointing down toward cat
	tailX := x + 6
	rl.DrawTriangle(
		rl.Vector2{X: float32(tailX - 3), Y: float32(by + bannerH)},
		rl.Vector2{X: float32(tailX + 3), Y: float32(by + bannerH)},
		rl.Vector2{X: float32(tailX), Y: float32(by + bannerH + 4)},
		bubbleBgColor,
	)

	// Text left-aligned
	rl.DrawText(line1, bx+padding, by+padding, fontSize, claudeColor)
	if line2 != "" {
		rl.DrawText(line2, bx+padding, by+padding+fontSize+lineSpacing, fontSize, claudeColor)
	}
}

func (r *Renderer) drawWoodFloor() {
	baseColor := rl.Color{R: 155, G: 120, B: 80, A: 255}
	darkPlank := rl.Color{R: 140, G: 108, B: 70, A: 255}
	lightPlank := rl.Color{R: 168, G: 132, B: 90, A: 255}
	groove := rl.Color{R: 125, G: 95, B: 60, A: 255}

	// Base
	rl.DrawRectangle(0, 162, screenWidth, 38, baseColor)

	// Horizontal plank lines
	plankH := int32(8)
	for py := int32(162); py < 200; py += plankH {
		rl.DrawLine(0, py, screenWidth, py, groove)
	}

	// Vertical stagger pattern (brick-like)
	plankW := int32(40)
	for row := int32(0); row < 5; row++ {
		py := int32(162) + row*plankH
		offset := int32(0)
		if row%2 == 1 {
			offset = plankW / 2
		}
		for px := offset; px < screenWidth; px += plankW {
			rl.DrawLine(px, py, px, py+plankH, groove)
			// Alternate plank shading
			if ((px/plankW)+row)%3 == 0 {
				rl.DrawRectangle(px+1, py+1, plankW-2, plankH-2, darkPlank)
			} else if ((px/plankW)+row)%3 == 1 {
				rl.DrawRectangle(px+1, py+1, plankW-2, plankH-2, lightPlank)
			}
		}
	}

	// Baseboard at wall-floor junction
	rl.DrawRectangle(0, 162, screenWidth, 2, rl.Color{R: 130, G: 100, B: 65, A: 255})
}

func min32(a, b int32) int32 {
	if a < b {
		return a
	}
	return b
}
