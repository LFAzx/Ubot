import os
import tempfile

_cookiefile_path = None


def get_youtube_cookiefile():
    """Returns a path to a cookies.txt file built from the YOUTUBE_COOKIES env var
    (Netscape format), or None if that env var isn't set. Used to reduce YouTube's
    'Sign in to confirm you're not a bot' blocks on datacenter IPs like Railway's."""
    global _cookiefile_path
    raw = os.environ.get("YOUTUBE_COOKIES")
    if not raw:
        return None
    if _cookiefile_path is None:
        fd, path = tempfile.mkstemp(suffix=".txt")
        with os.fdopen(fd, "w") as f:
            f.write(raw)
        _cookiefile_path = path
    return _cookiefile_path
