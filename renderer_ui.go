package main

import (
	"fmt"
	"strings"

	rl "github.com/gen2brain/raylib-go/raylib"
)

// UI Colors
var (
	uiBgColor      = rl.Color{R: 20, G: 18, B: 30, A: 220}
	uiBorderColor  = rl.Color{R: 80, G: 80, B: 100, A: 255}
	uiTextColor    = rl.Color{R: 220, G: 220, B: 230, A: 255}
	uiDimColor     = rl.Color{R: 140, G: 140, B: 160, A: 255}
	uiHighlight    = rl.Color{R: 255, G: 170, B: 50, A: 255}
	uiAccentColor  = rl.Color{R: 100, G: 180, B: 255, A: 255}
	bubbleBgColor  = rl.Color{R: 255, G: 255, B: 245, A: 240}
	bubbleTextColor = rl.Color{R: 40, G: 40, B: 50, A: 255}
	bannerBgColor  = rl.Color{R: 200, G: 60, B: 60, A: 230}
	bannerTextColor = rl.Color{R: 255, G: 255, B: 255, A: 255}
)

// DrawMenu draws the tab menu overlay
func (r *Renderer) DrawMenu(menu *MenuState) {
	if menu.Mode != ModeMenu {
		return
	}

	// Semi-transparent backdrop
	rl.DrawRectangle(0, 0, screenWidth, screenHeight, rl.Color{R: 0, G: 0, B: 0, A: 100})

	// Measure required width from title and options
	titleText := "EXERCISE MENU"
	options := []string{"Start Exercise", "Exercise Log"}
	padding := int32(24)

	maxW := rl.MeasureText(titleText, 8)
	for _, opt := range options {
		w := rl.MeasureText("> "+opt, 8)
		if w > maxW {
			maxW = w
		}
	}
	boxW := maxW + padding
	if boxW > screenWidth-16 {
		boxW = screenWidth - 16
	}

	boxH := int32(22 + len(options)*16)
	boxX := (screenWidth - boxW) / 2
	boxY := int32(40)

	rl.DrawRectangle(boxX-1, boxY-1, boxW+2, boxH+2, uiBorderColor)
	rl.DrawRectangle(boxX, boxY, boxW, boxH, uiBgColor)

	// Title (centered)
	titleW := rl.MeasureText(titleText, 8)
	rl.DrawText(titleText, boxX+(boxW-titleW)/2, boxY+6, 8, uiAccentColor)

	// Options
	for i, opt := range options {
		y := boxY + 22 + int32(i)*16
		textColor := uiTextColor
		prefix := "  "
		if i == menu.SelectedOption {
			prefix = "> "
			textColor = uiHighlight
			rl.DrawRectangle(boxX+4, y-1, boxW-8, 12, rl.Color{R: 60, G: 55, B: 80, A: 200})
		}
		rl.DrawText(prefix+opt, boxX+8, y, 8, textColor)
	}

	// Hint at bottom
	r.drawHintBar("[Enter] Select  [Esc] Close")
}

// DrawSpeechBubble draws a speech bubble from the character
func (r *Renderer) DrawSpeechBubble(text string) {
	if text == "" {
		return
	}

	lines := strings.Split(text, "\n")
	lineCount := len(lines)

	// Calculate bubble size using actual text measurement
	maxLineW := int32(0)
	for _, line := range lines {
		w := rl.MeasureText(line, 8)
		if w > maxLineW {
			maxLineW = w
		}
	}

	bubbleW := maxLineW + 16
	bubbleH := int32(lineCount*10 + 10)

	// Position above character, centered
	charCenterX := int32(screenWidth / 2)
	bubbleX := charCenterX - bubbleW/2
	bubbleY := int32(90) - bubbleH

	// Clamp to screen
	if bubbleX < 4 {
		bubbleX = 4
	}
	if bubbleX+bubbleW > screenWidth-4 {
		bubbleX = screenWidth - 4 - bubbleW
	}

	// Bubble body
	rl.DrawRectangle(bubbleX, bubbleY, bubbleW, bubbleH, bubbleBgColor)
	rl.DrawRectangleLines(bubbleX, bubbleY, bubbleW, bubbleH, rl.Color{R: 180, G: 180, B: 170, A: 255})

	// Tail (small triangle pointing down toward character)
	tailX := charCenterX
	rl.DrawTriangle(
		rl.Vector2{X: float32(tailX - 4), Y: float32(bubbleY + bubbleH)},
		rl.Vector2{X: float32(tailX + 4), Y: float32(bubbleY + bubbleH)},
		rl.Vector2{X: float32(tailX), Y: float32(bubbleY + bubbleH + 6)},
		bubbleBgColor,
	)

	// Text
	for i, line := range lines {
		rl.DrawText(line, bubbleX+8, bubbleY+5+int32(i)*10, 8, bubbleTextColor)
	}
}

// DrawPauseBanner draws the paused state banner
func (r *Renderer) DrawPauseBanner() {
	bannerH := int32(20)
	bannerY := int32(4)

	rl.DrawRectangle(0, bannerY, screenWidth, bannerH, bannerBgColor)
	titleText := "Paused"
	hintText := "[Esc] Resume  [Enter] Stop"
	titleW := rl.MeasureText(titleText, 8)
	hintW := rl.MeasureText(hintText, 8)
	rl.DrawText(titleText, (screenWidth-titleW)/2, bannerY+2, 8, bannerTextColor)
	rl.DrawText(hintText, (screenWidth-hintW)/2, bannerY+11, 8, rl.Color{R: 255, G: 200, B: 200, A: 255})
}

// formatDuration formats seconds as HH:MM:SS
func formatDuration(seconds float32) string {
	total := int(seconds)
	h := total / 3600
	m := (total % 3600) / 60
	s := total % 60
	return fmt.Sprintf("%02d:%02d:%02d", h, m, s)
}

// DrawExerciseSummary draws the exercise summary overlay
func (r *Renderer) DrawExerciseSummary(menu *MenuState) {
	// Semi-transparent backdrop
	rl.DrawRectangle(0, 0, screenWidth, screenHeight, rl.Color{R: 0, G: 0, B: 0, A: 120})

	summary := menu.GetRoundSummary()

	// Measure required width from actual text
	padding := int32(20)
	sepGap := int32(10) // gap between columns
	maxNameW := int32(0)
	maxRepsW := int32(0)
	maxTimeW := int32(0)
	var totalDuration float32
	for _, ex := range summary {
		nw := rl.MeasureText(ex.Name, 8)
		rw := rl.MeasureText(ex.Reps, 8)
		tw := rl.MeasureText(formatDuration(ex.Duration), 8)
		if nw > maxNameW {
			maxNameW = nw
		}
		if rw > maxRepsW {
			maxRepsW = rw
		}
		if tw > maxTimeW {
			maxTimeW = tw
		}
		totalDuration += ex.Duration
	}

	// Ensure box fits all possible text
	title := "NICE WORK!"
	emptyText := "No exercises completed yet"
	totalText := fmt.Sprintf("Total: %d exercises  %s", len(summary), formatDuration(totalDuration))

	minW := rl.MeasureText(title, 8) + padding
	if w := rl.MeasureText(emptyText, 8) + padding; w > minW {
		minW = w
	}
	if w := rl.MeasureText(totalText, 8) + padding; w > minW {
		minW = w
	}

	contentW := maxNameW + sepGap + maxRepsW + sepGap + maxTimeW + padding
	boxW := contentW
	if boxW < minW {
		boxW = minW
	}
	// Clamp to screen
	if boxW > screenWidth-16 {
		boxW = screenWidth - 16
	}
	boxX := (screenWidth - boxW) / 2

	lineCount := len(summary)
	if lineCount == 0 {
		lineCount = 1
	}
	boxH := int32(40 + lineCount*12)
	boxY := (screenHeight - boxH) / 2

	// Box
	rl.DrawRectangle(boxX-1, boxY-1, boxW+2, boxH+2, uiBorderColor)
	rl.DrawRectangle(boxX, boxY, boxW, boxH, uiBgColor)

	// Title
	rl.DrawText(title, boxX+10, boxY+6, 8, uiAccentColor)

	// Divider
	rl.DrawRectangle(boxX+8, boxY+17, boxW-16, 1, uiBorderColor)

	if len(summary) == 0 {
		rl.DrawText("No exercises completed yet", boxX+10, boxY+24, 8, uiDimColor)
	} else {
		repsX := boxX + 10 + maxNameW + sepGap
		timeX := repsX + maxRepsW + sepGap
		for i, ex := range summary {
			y := boxY + 22 + int32(i)*12
			rl.DrawText(ex.Name, boxX+10, y, 8, uiTextColor)
			rl.DrawText(ex.Reps, repsX, y, 8, uiDimColor)
			rl.DrawText(formatDuration(ex.Duration), timeX, y, 8, uiDimColor)
		}
	}

	// Total count and time at bottom
	totalY := boxY + boxH - 14
	rl.DrawText(totalText, boxX+10, totalY, 8, uiHighlight)

	r.drawHintBar("[Esc] Close")
}

// DrawCountdown draws the 3-2-1 countdown in a speech bubble
func (r *Renderer) DrawCountdown(menu *MenuState) {
	text := fmt.Sprintf("%d", menu.CountdownValue)
	r.DrawSpeechBubble(text)
}

// DrawExerciseHint draws the bottom hint for exercising mode
func (r *Renderer) DrawExerciseHint() {
	r.drawHintBar("[Tab] Next exercise  [Esc] Pause")
}

// DrawPromptBubble draws the auto-prompt speech bubble
func (r *Renderer) DrawPromptBubble() {
	r.DrawSpeechBubble("Time to exercise!\nY or Enter to start")
	r.drawHintBar("[Y/Enter] Start  [N] Dismiss  [Tab] Menu")
}

// DrawIdleHint draws the Tab hint when idle
func (r *Renderer) DrawIdleHint() {
	r.drawHintBar("[Tab] Exercise menu")
}

// drawHintBar draws a hint text bar at the bottom of the screen
func (r *Renderer) drawHintBar(text string) {
	y := int32(screenHeight - 12)
	rl.DrawRectangle(0, y, screenWidth, 12, rl.Color{R: 0, G: 0, B: 0, A: 150})
	textW := rl.MeasureText(text, 8)
	x := (screenWidth - textW) / 2
	rl.DrawText(text, x, y+2, 8, uiDimColor)
}

// DrawExerciseLog draws the persistent exercise log overlay with tabs
func (r *Renderer) DrawExerciseLog(menu *MenuState) {
	// Semi-transparent backdrop
	rl.DrawRectangle(0, 0, screenWidth, screenHeight, rl.Color{R: 0, G: 0, B: 0, A: 120})

	boxW := int32(260)
	if boxW > screenWidth-16 {
		boxW = screenWidth - 16
	}
	boxH := int32(155)
	boxX := (screenWidth - boxW) / 2
	boxY := int32(14)

	// Box
	rl.DrawRectangle(boxX-1, boxY-1, boxW+2, boxH+2, uiBorderColor)
	rl.DrawRectangle(boxX, boxY, boxW, boxH, uiBgColor)

	// Tab bar
	tabNames := []string{"TODAY", "TREND", "STATS", "CLEAR"}
	tabX := boxX + 8
	for i, name := range tabNames {
		color := uiDimColor
		if i == menu.LogTab {
			color = uiHighlight
		}
		rl.DrawText(name, tabX, boxY+6, 8, color)
		tabX += rl.MeasureText(name, 8) + 12
	}
	// Divider under tabs
	rl.DrawRectangle(boxX+4, boxY+17, boxW-8, 1, uiBorderColor)

	contentY := boxY + 22
	contentH := boxH - 40 // space for footer
	footerY := boxY + boxH - 14

	log := menu.ExerciseLog
	if log == nil {
		rl.DrawText("No log available", boxX+10, contentY, 8, uiDimColor)
		r.drawHintBar("[</>] Tab  [Esc] Close")
		return
	}

	switch menu.LogTab {
	case 0:
		r.drawLogToday(log, menu, boxX, contentY, boxW, contentH, footerY)
	case 1:
		r.drawLogTrend(log, menu, boxX, contentY, boxW, contentH, footerY)
	case 2:
		r.drawLogStats(log, menu, boxX, contentY, boxW, contentH, footerY)
	case 3:
		r.drawLogClear(boxX, contentY, boxW, contentH, menu.ClearConfirmed)
	}

	hint := "[</>] Tab  [Esc] Close"
	if menu.LogTab == 0 || menu.LogTab == 1 || menu.LogTab == 2 { // Today, Trend, Stats have scrolling
		hint = "[</>] Tab  [Up/Dn] Scroll  [Esc]"
	} else if menu.LogTab == 3 { // CLEAR tab
		if menu.ClearConfirmed {
			hint = "[Enter] DELETE  [Esc] Back"
		} else {
			hint = "[Enter] Confirm  [Esc] Cancel"
		}
	}
	r.drawHintBar(hint)
}

func (r *Renderer) drawLogToday(log *ExerciseLog, menu *MenuState, boxX, contentY, boxW, contentH, footerY int32) {
	breakdown := log.TodayBreakdown()

	// Title
	titleText := "Today's Stats"
	titleW := rl.MeasureText(titleText, 8)
	rl.DrawText(titleText, boxX+(boxW-titleW)/2, contentY, 8, uiAccentColor)

	listY := contentY + 16
	listH := contentH - 16

	if len(breakdown) == 0 {
		rl.DrawText("No exercises today", boxX+10, listY+4, 8, uiDimColor)
		rl.DrawText("Today: 0 exercises", boxX+10, footerY, 8, uiHighlight)
		return
	}

	maxVisible := int(listH / 12)
	if menu.LogScrollPos > len(breakdown)-maxVisible {
		menu.LogScrollPos = len(breakdown) - maxVisible
	}
	if menu.LogScrollPos < 0 {
		menu.LogScrollPos = 0
	}

	// Measure columns
	sepGap := int32(8)
	maxNameW := int32(0)
	maxCountW := int32(0)
	for _, ts := range breakdown {
		nw := rl.MeasureText(ts.Name, 8)
		cw := rl.MeasureText(fmt.Sprintf("%dx", ts.Count), 8)
		if nw > maxNameW {
			maxNameW = nw
		}
		if cw > maxCountW {
			maxCountW = cw
		}
	}

	countX := boxX + 10 + maxNameW + sepGap
	timeX := countX + maxCountW + sepGap

	var totalCount int
	var totalDuration float32
	for _, ts := range breakdown {
		totalCount += ts.Count
		totalDuration += ts.TotalDuration
	}

	end := menu.LogScrollPos + maxVisible
	if end > len(breakdown) {
		end = len(breakdown)
	}
	for i := menu.LogScrollPos; i < end; i++ {
		ts := breakdown[i]
		y := listY + int32(i-menu.LogScrollPos)*12
		rl.DrawText(ts.Name, boxX+10, y, 8, uiTextColor)
		rl.DrawText(fmt.Sprintf("%dx", ts.Count), countX, y, 8, uiDimColor)
		rl.DrawText(formatDuration(ts.TotalDuration), timeX, y, 8, uiDimColor)
	}

	// Footer
	rl.DrawRectangle(boxX+4, footerY-4, boxW-8, 1, uiBorderColor)
	totalText := fmt.Sprintf("Today: %dx  %s", totalCount, formatDuration(totalDuration))
	rl.DrawText(totalText, boxX+10, footerY, 8, uiHighlight)
}

func (r *Renderer) drawLogStats(log *ExerciseLog, menu *MenuState, boxX, contentY, boxW, contentH, footerY int32) {
	breakdown := log.TypeBreakdown()

	// Title
	titleText := "All Time Stats"
	titleW := rl.MeasureText(titleText, 8)
	rl.DrawText(titleText, boxX+(boxW-titleW)/2, contentY, 8, uiAccentColor)

	listY := contentY + 16
	listH := contentH - 16

	if len(breakdown) == 0 {
		rl.DrawText("No exercises recorded", boxX+10, listY+4, 8, uiDimColor)
		rl.DrawText("All time: 0 exercises", boxX+10, footerY, 8, uiHighlight)
		return
	}

	maxVisible := int(listH / 12)
	if menu.LogScrollPos > len(breakdown)-maxVisible {
		menu.LogScrollPos = len(breakdown) - maxVisible
	}
	if menu.LogScrollPos < 0 {
		menu.LogScrollPos = 0
	}

	// Measure columns
	sepGap := int32(8)
	maxNameW := int32(0)
	maxCountW := int32(0)
	for _, ts := range breakdown {
		nw := rl.MeasureText(ts.Name, 8)
		cw := rl.MeasureText(fmt.Sprintf("%dx", ts.Count), 8)
		if nw > maxNameW {
			maxNameW = nw
		}
		if cw > maxCountW {
			maxCountW = cw
		}
	}

	countX := boxX + 10 + maxNameW + sepGap
	timeX := countX + maxCountW + sepGap

	var totalCount int
	var totalDuration float32
	for _, ts := range breakdown {
		totalCount += ts.Count
		totalDuration += ts.TotalDuration
	}

	end := menu.LogScrollPos + maxVisible
	if end > len(breakdown) {
		end = len(breakdown)
	}
	for i := menu.LogScrollPos; i < end; i++ {
		ts := breakdown[i]
		y := listY + int32(i-menu.LogScrollPos)*12
		rl.DrawText(ts.Name, boxX+10, y, 8, uiTextColor)
		rl.DrawText(fmt.Sprintf("%dx", ts.Count), countX, y, 8, uiDimColor)
		rl.DrawText(formatDuration(ts.TotalDuration), timeX, y, 8, uiDimColor)
	}

	// Footer
	rl.DrawRectangle(boxX+4, footerY-4, boxW-8, 1, uiBorderColor)
	totalText := fmt.Sprintf("All time: %dx  %s", totalCount, formatDuration(totalDuration))
	rl.DrawText(totalText, boxX+10, footerY, 8, uiHighlight)
}

func (r *Renderer) drawLogTrend(log *ExerciseLog, menu *MenuState, boxX, contentY, boxW, contentH, footerY int32) {
	days := log.DailyTrend()

	// Title
	titleText := "Daily Trend"
	titleW := rl.MeasureText(titleText, 8)
	rl.DrawText(titleText, boxX+(boxW-titleW)/2, contentY, 8, uiAccentColor)

	listY := contentY + 16
	listH := contentH - 16

	if len(days) == 0 {
		rl.DrawText("No data yet", boxX+10, listY+4, 8, uiDimColor)
		return
	}

	maxVisible := int(listH / 12)
	if menu.LogScrollPos > len(days)-maxVisible {
		menu.LogScrollPos = len(days) - maxVisible
	}
	if menu.LogScrollPos < 0 {
		menu.LogScrollPos = 0
	}

	// Measure columns (same layout as Today/Stats)
	sepGap := int32(8)
	maxNameW := int32(0)
	maxCountW := int32(0)
	for _, d := range days {
		nw := rl.MeasureText(d.Date.Format("Jan 2"), 8)
		cw := rl.MeasureText(fmt.Sprintf("%dx", d.Count), 8)
		if nw > maxNameW {
			maxNameW = nw
		}
		if cw > maxCountW {
			maxCountW = cw
		}
	}
	countX := boxX + 10 + maxNameW + sepGap
	timeX := countX + maxCountW + sepGap

	end := menu.LogScrollPos + maxVisible
	if end > len(days) {
		end = len(days)
	}
	for i := menu.LogScrollPos; i < end; i++ {
		d := days[i]
		y := listY + int32(i-menu.LogScrollPos)*12

		rl.DrawText(d.Date.Format("Jan 2"), boxX+10, y, 8, uiTextColor)
		rl.DrawText(fmt.Sprintf("%dx", d.Count), countX, y, 8, uiDimColor)
		rl.DrawText(formatDuration(d.TotalDuration), timeX, y, 8, uiDimColor)
	}

	// Footer
	rl.DrawRectangle(boxX+4, footerY-4, boxW-8, 1, uiBorderColor)
	rl.DrawText(fmt.Sprintf("%d days tracked", len(days)), boxX+10, footerY, 8, uiHighlight)
}

func (r *Renderer) drawLogClear(boxX, contentY, boxW, contentH int32, confirmed bool) {
	centerY := contentY + contentH/2 - 10

	if confirmed {
		warn := "This cannot be undone!"
		warnW := rl.MeasureText(warn, 8)
		rl.DrawText(warn, boxX+(boxW-warnW)/2, centerY, 8, rl.Red)

		hint := "[Enter] DELETE   [Esc] Back"
		hintW := rl.MeasureText(hint, 8)
		rl.DrawText(hint, boxX+(boxW-hintW)/2, centerY+14, 8, uiDimColor)
	} else {
		msg := "Clear all exercise data?"
		msgW := rl.MeasureText(msg, 8)
		rl.DrawText(msg, boxX+(boxW-msgW)/2, centerY, 8, bannerBgColor)

		hint := "[Enter] Confirm   [Esc] Cancel"
		hintW := rl.MeasureText(hint, 8)
		rl.DrawText(hint, boxX+(boxW-hintW)/2, centerY+14, 8, uiDimColor)
	}
}
