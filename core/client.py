import requests
import re
import json
import logging
from urllib.parse import urlparse, parse_qs
from core.crypto_utils import CryptoUtils

class DownSubClient:
    BASE_URL = "https://downsub.com"
    API_URL = "https://get-info.downsub.com"
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Referer": "https://downsub.com/",
            "Origin": "https://downsub.com"
        })
        self.logger = logging.getLogger(__name__)

    def _extract_id(self, url: str) -> str:
        """
        Extracts ID for YouTube, or returns URL for others.
        """
        # Simple YouTube ID extraction
        # https://youtu.be/ID
        # https://www.youtube.com/watch?v=ID
        
        if "youtu.be" in url:
            path = urlparse(url).path
            return path.strip("/")
        elif "youtube.com" in url:
            query = parse_qs(urlparse(url).query)
            if "v" in query:
                return query["v"][0]
        
        # Fallback: return trimmed URL or just let it be
        return url

    def get_video_info(self, url: str):
        """
        Fetches subtitle info for the given video URL.
        """
        # 1. Prepare Payload
        video_id = self._extract_id(url)
        self.logger.info(f"Processing ID/URL: {video_id}")
        
        # Input to encryption is JSON string of the ID
        encrypted_payload = CryptoUtils.encrypt(video_id)
        
        # 2. Call API
        target_url = f"{self.API_URL}/{encrypted_payload}"
        self.logger.debug(f"Fetching Info from: {target_url}")
        
        try:
            resp = self.session.get(target_url)
            resp.raise_for_status()
            data = resp.json()
            return data
        except Exception as e:
            self.logger.error(f"API Request Failed: {e}")
            raise

    def download_subtitle(self, subtitle_entry, title: str):
        """
        Downloads the subtitle content.
        subtitle_entry: The dict object from 'subtitles' list in get_video_info response.
        title: Video title (for filename suggestion if needed).
        """
        # subtitle_entry has 'url' which is the ENCRYPTED payload for download
        # and 'urlSubtitle' from main response? 
        # Actually 'url' in subtitle_entry is just the payload.
        # We need to construct the download URL.
        
        # Format: https://download.subtitle.to/?title=...&url=...&type=raw
        # Or use the 'url' from the entry directly if it's a full URL? 
        # In Response_2.txt: "url": "eyJjdCI6..." (This is payload).
        # In Response_2.txt root: "urlSubtitle": "https://subtitle2.downsub.com/"
        
        # We should use the domain from 'urlSubtitle' or fallback.
        
        base_dl_url = "https://subtitle2.downsub.com" # Default fallback
        # Ideally we pass the base_dl_url from the get_video_info response if possible, 
        # but here we might need to be flexible.
        
        payload = subtitle_entry.get('url')
        if not payload:
            raise ValueError("No download URL in subtitle entry")
            
        params = {
            "title": title,
            "url": payload,
            "type": "raw" # srt or txt?
        }
        
        # Try download
        try:
            # Note: cURL 5 uses subtitle2.downsub.com
            dl_url = f"{base_dl_url}/"
            self.logger.info(f"Downloading from {dl_url}...")
            
            resp = self.session.get(dl_url, params=params)
            resp.raise_for_status()
            return resp.text
        except Exception as e:
            self.logger.error(f"Download request failed: {e}")
            raise

