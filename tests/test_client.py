import unittest
from unittest.mock import MagicMock, patch
from core.client import DownSubClient

class TestDownSubClient(unittest.TestCase):
    def setUp(self):
        self.client = DownSubClient()

    def test_extract_id_youtube(self):
        url1 = "https://youtu.be/BS72fMpsGjk"
        self.assertEqual(self.client._extract_id(url1), "BS72fMpsGjk")
        
        url2 = "https://www.youtube.com/watch?v=BS72fMpsGjk&t=123"
        self.assertEqual(self.client._extract_id(url2), "BS72fMpsGjk")

    def test_extract_id_other(self):
        url = "https://vimeo.com/123456"
        self.assertEqual(self.client._extract_id(url), url)

    @patch('core.client.requests.Session.get')
    def test_get_video_info(self, mock_get):
        # Mock Response
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {"title": "Test Video", "subtitles": []}
        mock_get.return_value = mock_resp
        
        data = self.client.get_video_info("https://youtu.be/test")
        self.assertIn("title", data)
        self.assertTrue(mock_get.called)

if __name__ == "__main__":
    unittest.main()
