# Phase 03: UI Integration
Status: ✅ Complete
Dependencies: Phase 01, Phase 02

## Objective
Connect the Backend Logic (`DownSubClient`) to the Frontend UI (`MainWindow`).

## Requirements
### Functional
- [x] Create `ui/worker.py` for threading (QThread).
- [x] Update `ui/main_window.py` to use `DownSubClient` and `Worker`.
    - [x] Add Imports
    - [x] Initialize Client
    - [x] Implement `on_get_subtitles` with Worker
    - [x] Implement `on_info_received` and table population
    - [x] Implement `on_download_clicked`
- [x] Table row rendering (helper function).

## Implementation Steps
1. [x] Create `ui/worker.py`.
2. [x] Update `ui/main_window.py`.

## Files Modified
- `ui/main_window.py`
- `ui/worker.py`

---
Next Phase: [Phase 04](phase-04-polish.md)
