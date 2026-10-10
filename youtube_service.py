import re
from typing import Dict, Any, Optional

def extract_video_id(url: str) -> Optional[str]:
    """Extracts YouTube video ID strictly from valid youtube.com and youtu.be URL formats."""
    if not url:
        return None
    url = url.strip()
    
    # Must belong to valid YouTube domains
    if not ("youtube.com" in url.lower() or "youtu.be" in url.lower()):
        return None

    patterns = [
        r'(?:v=)([0-9A-Za-z_-]{11})',
        r'youtu\.be\/([0-9A-Za-z_-]{11})',
        r'(?:\/embed\/)([0-9A-Za-z_-]{11})',
        r'(?:\/shorts\/)([0-9A-Za-z_-]{11})'
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None

def fetch_youtube_video_title(video_id: str) -> Optional[str]:
    """Fetches video title using YouTube public oEmbed endpoint without API keys."""
    try:
        import requests
        oembed_url = f"https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v={video_id}&format=json"
        res = requests.get(oembed_url, timeout=4)
        if res.status_code == 200:
            return res.json().get("title")
    except Exception:
        pass
    return None

def fetch_youtube_transcript(url: str) -> Dict[str, Any]:
    """
    Attempts to fetch transcript from YouTube using youtube-transcript-api.
    Returns structured result with clear status, optional video title, and explainable failure reasons.
    Never hallucinates or fabricates content if extraction fails.
    """
    video_id = extract_video_id(url)
    if not video_id:
        return {
            "success": False,
            "transcript": "",
            "video_id": None,
            "title": None,
            "error": "Invalid YouTube URL format. Please provide a valid youtube.com or youtu.be link, or paste lecture notes directly."
        }

    try:
        from youtube_transcript_api import YouTubeTranscriptApi
    except ImportError:
        return {
            "success": False,
            "transcript": "",
            "video_id": video_id,
            "title": None,
            "error": "The youtube-transcript-api package is not available. Please paste the transcript or lecture notes directly."
        }

    try:
        raw_text = ""
        # Check modern 1.2+ API vs legacy 0.6+ API
        if hasattr(YouTubeTranscriptApi, "fetch"):
            api_instance = YouTubeTranscriptApi()
            transcript_obj = api_instance.fetch(video_id, languages=['en', 'en-US', 'hi'])
            # FetchedTranscript objects or list of dicts/snippets
            snippets = getattr(transcript_obj, "snippets", transcript_obj)
            raw_text = " ".join([getattr(s, "text", s.get("text", "") if isinstance(s, dict) else str(s)) for s in snippets])
        elif hasattr(YouTubeTranscriptApi, "get_transcript"):
            transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=['en', 'en-US', 'hi'])
            raw_text = " ".join([entry.get("text", "") for entry in transcript_list])
        else:
            raise Exception("Compatible transcript retrieval method not found in installed library.")

        clean_text = re.sub(r'\s+', ' ', raw_text).strip()
        if len(clean_text) < 50:
            return {
                "success": False,
                "transcript": "",
                "video_id": video_id,
                "title": None,
                "error": "The extracted video transcript is too short or empty. Please paste your lecture notes manually."
            }

        # Try retrieving video title via public oEmbed endpoint
        video_title = fetch_youtube_video_title(video_id) or "YouTube Video Lecture"

        return {
            "success": True,
            "transcript": clean_text,
            "video_id": video_id,
            "title": video_title,
            "error": None
        }

    except Exception as e:
        err_msg = str(e).lower()
        if "disabled" in err_msg or "transcriptsdisabled" in err_msg:
            return {
                "success": False,
                "transcript": "",
                "video_id": video_id,
                "title": None,
                "error": "Subtitles/transcripts are disabled for this YouTube video. Please paste your lecture notes manually."
            }
        elif "could not find" in err_msg or "notranscriptfound" in err_msg:
            return {
                "success": False,
                "transcript": "",
                "video_id": video_id,
                "title": None,
                "error": "No English or Hindi captions were found for this video. Please paste the lecture transcript or summary manually."
            }
        else:
            return {
                "success": False,
                "transcript": "",
                "video_id": video_id,
                "title": None,
                "error": f"Could not retrieve video captions ({str(e)}). Please copy and paste the lecture notes manually."
            }
