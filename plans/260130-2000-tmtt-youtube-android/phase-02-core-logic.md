# Phase 02: Core Logic, Crypto & Network
Status: ⬜ Pending

## Objective
Implement the core subtitle fetching logic: Port AES encryption from Python to Kotlin, implement DownSub API client, and set up the Gemini API client with Smart Fallback.

## Requirements
### Functional
- [ ] `CryptoUtils.encrypt(videoID)` matches Python output.
- [ ] `DownSubClient` successfully fetches subtitle JSON.
- [ ] `GeminiClient` iterates through model list on 429 error.
- [ ] `SubtitleRepository` orchestrates the flow.

## Implementation Steps
1.  [ ] **Crypto Logic**:
    - Implement `EvpBytesToKey` (MD5 based) in Kotlin.
    - Implement AES-256-CBC Encryption/Decryption.
    - Test against Python scripts.
2.  [ ] **DownSub API**:
    - Create `DownSubService` (Retrofit interface).
    - Implement `DownSubRepository`.
3.  [ ] **Gemini API**:
    - Create `GeminiService`.
    - Implement `SmartGeminiClient`:
        - Input: List of Model Strings.
        - Logic: Loop through models until success or list exhausted.
4.  [ ] **Repository Layer**:
    - Combine `DownSub` + `Gemini` into `MainRepository`.

## Files to Create/Modify
- `core/security/CryptoUtils.kt`
- `data/api/DownSubService.kt`
- `data/api/GeminiService.kt`
- `data/network/SmartGeminiClient.kt`
- `data/repository/MainRepositoryImpl.kt`

## Test Criteria
- [ ] Unit Test: `CryptoUtils.encrypt("test")` output is decryptable by Python script.
- [ ] Integration Test: Fetch subtitles for a real YouTube video.
- [ ] Mock Test: Force Gemini fail on first model, succeed on second.

---
Next Phase: [Phase 03 - UI Implementation](phase-03-ui-ux.md)
