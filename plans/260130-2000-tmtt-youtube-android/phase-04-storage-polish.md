# Phase 04: Final Polish & Verification
Status: ⬜ Pending

## Objective
Finalize the app with polish, error handling, and regression testing. (Storage requirement removed).

## Requirements
### Functional
- [ ] Settings persist API Keys using DataStore/SharedPreferences.
- [ ] App handles errors gracefully (Invalid URL, No Subtitles found).
- [ ] TTS Engine checks (prompt if not installed).

## Implementation Steps
1.  [ ] **Settings Logic**:
    - Implement `SettingsRepository` using DataStore.
    - Persist: List of API Keys, Preferred Models, TTS Speed.
2.  [ ] **Polish**:
    - Add Error States (No Internet, Invalid URL).
    - Add "Copied to Clipboard" toast for Summary.
    - Optimize Startup time.
3.  [ ] **Verification**:
    - Run full flow: Link -> Summary -> TTS.
    - Verify "No Storage" policy (Nothing remains after cache clear).

## Files to Create/Modify
- `data/repository/SettingsRepository.kt`
- `ui/screens/settings/SettingsViewModel.kt`
- `ui/screens/result/ResultScreen.kt` (Polish)

## Test Criteria
- [ ] API keys survive app restart.
- [ ] App does NOT save video history.
- [ ] TTS works reliably.
