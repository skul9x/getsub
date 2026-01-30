# 💡 SPEC: YouTube Subtitle Downloader (PySide6)

**Created:** 2026-01-30
**Tech Stack:** Python 3.10+, PySide6, Requests, PyCryptodome (potential)

---

## 1. Problem & Solution
*   **Problem:** User needs to download subtitles from YouTube (and other sites) via `downsub.com`.
*   **Solution:** A Desktop App (PySide6) that mimics `downsub.com`'s API flow to fetch and download subtitles.

## 2. Architecture
### 2.1. Logic Flow (Reverse Engineered)
1.  **Init**: GET `https://downsub.com` (Setup cookies/headers).
2.  **Encrypt**: User inputs `[YOUTUBE_URL]`. App must encrypt this to generate `[PAYLOAD_1]`.
    *   *Note: Encryption uses AES-CBC (likely). Key/IV must be extracted or hardcoded.*
3.  **Get Info**: GET `https://get-info.downsub.com/[PAYLOAD_1]`.
    *   Response: JSON with list of subtitles. Each subtitle has a `url` field (`[PAYLOAD_2]`).
4.  **Download**: GET `https://download.subtitle.to/?title=...&url=[PAYLOAD_2]&type=raw`.
    *   Response: The subtitle content (SRT/TXT).

### 2.2. Component Design (MVC)
*   **Model (`core/`)**:
    *   `DownSubClient`: Manages `requests.Session`.
    *   `CryptoUtils`: Handles the encryption generation (Crucial).
    *   `Subtitle`: Data class for subtitle info.
*   **View (`ui/`)**:
    *   `MainWindow`: Main GUI.
    *   `UrlInput`: Input field.
    *   `ResultTable`: Shows available languages (Language, Translated, Action).
*   **Controller (`main.py`)**:
    *   Connects View signals to Model actions.

---

## 3. Data Structures
### 3.1. Subtitle Item
```python
@dataclass
class SubtitleItem:
    language: str
    code: str
    download_payload: str  # The encrypted 'url' from API
    is_auto_generated: bool
```

---

## 4. Key Challenges & Risks
*   **Encryption Key:** The logic relies on generating the correct payload. If `downsub.com` changes keys, the app breaks.
    *   *Mitigation:* Logic to extract key from JS or allow user to update config.
*   **Rate Labeling:** The site might block automated requests.
    *   *Mitigation:* Use random User-Agents and Delays.

---

## 5. Implementation Phases
### Phase 1: Setup & UI Skeleton
*   Project structure.
*   PySide6 basic window.
*   Logging setup.

### Phase 2: Core Logic (The API)
*   Implement `DownSubClient`.
*   Implement `CryptoUtils` (Attempt to replicate JS encryption).
*   Verify with Unit Tests using provided cURL data.

### Phase 3: UI Integration
*   Connect UI to Logic.
*   Display results in Table.
*   Implement "Download" button behavior (File Save Dialog).

### Phase 4: Polish
*   Error handling (Network timeout).
*   Progress bar.
*   Threading (Don't freeze UI).
