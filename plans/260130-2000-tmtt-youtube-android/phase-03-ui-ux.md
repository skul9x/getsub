# Phase 03: UI/UX Implementation (Jetpack Compose)
Status: ⬜ Pending

## Objective
Build the user interface with a "Commercial/Premium" vibe. Implement Home, Result, and Settings screens with animations and TTS integration.

## Requirements
### Functional
- [ ] User can paste URL and see loading state.
- [ ] Result screen shows Video Title, Thumbnail, and Summary.
- [ ] TTS Floating Action Button plays/pauses audio.
- [ ] Settings screen allows editing API Keys and Models.

### Non-Functional
- [ ] Dark Mode with gradient backgrounds.
- [ ] Smooth transitions between screens.
- [ ] Glassmorphism effects on cards.

## Implementation Steps
1.  [ ] **Design System**:
    - Define Custom Colors (Gradients), Typography (Google Fonts).
    - Create reusable `GlassCard`, `GradientButton`.
2.  [ ] **Home Screen**:
    - URL Input Field (Rounded, blurred background).
    - "Paste & Go" Button.
    - Recent History List (Horizontal Scroll).
3.  [ ] **Result Screen**:
    - Top: Youtube Thumbnail (Coil).
    - Middle: TabRow (Summary | Raw Subtitles).
    - Content: Markdown Text rendering.
    - FAB: TTS Control (Play/Stop icon).
4.  [ ] **Settings Screen**:
    - List of API Keys (Add/Delete).
    - Model Preference List (Reorderable if possible, or simple list).
    - Model Fallback Toggle.

## Files to Create/Modify
- `ui/screens/home/HomeScreen.kt`
- `ui/screens/result/ResultScreen.kt`
- `ui/screens/settings/SettingsScreen.kt`
- `ui/components/GlassCard.kt`

## Test Criteria
- [ ] UI looks premium (no default Material colors).
- [ ] TTS button reads the text correctly.
- [ ] Navigation works smoothly.

---
Next Phase: [Phase 04 - Local Storage & Final Polish](phase-04-storage-polish.md)
