class _Sentinel:
    def __repr__(self):
        return "<sentinel>"


sentinel = _Sentinel()

METHODS = ["GET", "POST", "PUT", "DELETE", "HEAD", "OPTIONS", "TRACE"]

DEFAULT_IGNORE_FILES = [
    "__init__.py",
    "__main__.py",
]