""" video mixing cut"""

import importlib
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from video.video_mixer import (
        VideoMixer,
        TextParameters,
        VideoParameters,
        TextArgument
    )

_module_lookup = {
    "VideoMixer": "video.video_mixer",
    "TextParameters": "video.video_mixer",
    "VideoParameters": "video.video_mixer",
    "TextArgument": "video.video_mixer"
}

__all__ = list(_module_lookup.keys())


def __getattr__(name: str) -> Any:
    if name in _module_lookup:
        module = importlib.import_module(_module_lookup[name])
        return getattr(module, name)
    raise AttributeError(f"module {__name__} has no attribute {name}")