# Phase 02: Core Backend Logic
Status: ✅ Complete
Dependencies: Phase 01

## Objective
Implement the logic to interact with DownSub API, specifically the encryption of the URL to generate the payload.

## Requirements
### Functional
- [x] `CryptoUtils` class to encrypt user input (Reverse engineer from JS if needed).
- [x] `DownSubClient` class to:
    - [x] Fetch initial page.
    - [x] Send request to `get-info`.
    - [x] Parse JSON response.
    - [x] Download subtitle content.
- [x] Unit Test to verify against `cURL+Response` data.

## Implementation Steps
1. [x] Implement `core/crypto_utils.py`.
2. [x] Implement `core/client.py`.
3. [x] Create a test script `tests/test_api.py` to verify logic.

## Files to Create
- `core/crypto_utils.py`
- `core/client.py`
- `tests/test_api.py`

## Notes
- Found Key: `zthxw34cdp6wfyxmpad38v52t3hsz6c5`
