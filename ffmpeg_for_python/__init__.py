# ffmpeg-and-python/__init__.py

from .ffmpeg import FFmpeg
from .exeptions import FFmpegExceptions

__all__ = ['FFmpeg', 'FFmpegExceptions']
if __name__ == '__main__':
    raise RuntimeError("no escope!")
