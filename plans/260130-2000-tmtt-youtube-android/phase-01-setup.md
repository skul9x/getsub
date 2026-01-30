# Phase 01: Setup Environment & Core Architecture
Status: ⬜ Pending

## Objective
Initialize the Android project, configure build scripts with necessary dependencies (Jetpack Compose, Hilt, Retrofit, Room), and set up the basic project structure (MVVM/Clean).

## Requirements
### Functional
- [ ] Project compiles and runs on an Android Emulator/Device.
- [ ] Dependency Injection (Hilt) is working.
- [ ] Navigation Graph is set up (Home -> Result -> Settings).

### Non-Functional
- [ ] Uses Material 3 Design System.
- [ ] Secure API Key management (Secrets Gradle Plugin or local.properties).

## Implementation Steps
1.  [ ] **Initialize Project**: Create new Android Studio project (Empty Compose Activity).
2.  [ ] **Gradle Setup**:
    - Add Hilt (Dagger) dependencies & plugin.
    - Add Retrofit + OkHttp.
    - Add Room Database.
    - Add Coil (Image Loading).
    - Add Navigation Compose.
3.  [ ] **Package Structure**:
    - `com.tmtt.youtube`
        - `core` (di, utils)
        - `data` (api, db, repo)
        - `domain` (models, usecases)
        - `ui` (screens, theme, components)
4.  [ ] **Secrets Management**:
    - Configure `local.properties` to hold `GEMINI_API_KEY_DEFAULT` (dummy for now).
    - Expose via `BuildConfig`.
5.  [ ] **Base Theme**:
    - Create `TmTtTheme` with Dark Mode colors.

## Files to Create/Modify
- `build.gradle.kts` (Project & App module)
- `gradle.properties`
- `app/src/main/AndroidManifest.xml`
- `app/src/main/java/com/tmtt/youtube/TmTtApp.kt` (Hilt App class)
- `app/src/main/java/com/tmtt/youtube/ui/theme/Color.kt` (Commercial Palette)

## Test Criteria
- [ ] Build is successful (`./gradlew assembleDebug`).
- [ ] App launches and shows a "Hello TmTt" text.
- [ ] Hilt Graph validates without errors.

---
Next Phase: [Phase 02 - Core Logic & Crypto](phase-02-core-logic.md)
