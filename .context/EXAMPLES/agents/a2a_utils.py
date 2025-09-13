"""Utility helpers for A2A handlers.

Provides a small helper to ensure the repo `src` directory is on sys.path
and a canonical payload normalization function used across A2A handlers.
"""
from __future__ import annotations

import os
import sys
from typing import Any, Type

_SRC_ADDED = False


def ensure_src_in_path() -> None:
    """Ensure the top-level `src` directory is on sys.path once.

    Many A2A handlers import `a2a_protocol` from `src/`. This helper adds the
    correct absolute path once so individual handlers don't each manipulate
    sys.path.
    """
    global _SRC_ADDED
    if _SRC_ADDED:
        return
    # `agents` directory is sibling of `src` in the repo layout
    agents_dir = os.path.dirname(__file__)
    repo_root = os.path.normpath(os.path.join(agents_dir, ".."))
    src_path = os.path.join(repo_root, "src")
    if os.path.isdir(src_path) and src_path not in sys.path:
        sys.path.insert(0, src_path)
    _SRC_ADDED = True


# Run automatically when module is imported so handlers can import a2a_protocol
# at module-level without each file mutating sys.path.
ensure_src_in_path()


def normalize_payload(payload: Any, model_cls: Type) -> Any:
    """Normalize an incoming A2A message payload into an instance of model_cls.

    Supported payload shapes:
    - an instance of model_cls -> returned directly
    - a dict -> used to construct model_cls(**payload)
    - an object with `model_dump()` (Pydantic BaseModel) -> payload.model_dump() used

    Raises any error coming from model construction so handlers can respond
    with a meaningful failure.
    """
    # If it's already the right type, return
    try:
        if isinstance(payload, model_cls):
            return payload
    except Exception:
        # model_cls may be a pydantic model type that doesn't play well with isinstance in some cases
        pass

    # If it's a Pydantic model, use model_dump()
    if hasattr(payload, "model_dump"):
        payload_dict = payload.model_dump()
        return model_cls(**payload_dict)

    # If it's a plain dict-like object
    if isinstance(payload, dict):
        return model_cls(**payload)

    # Fallback: try to coerce via dict(payload) if possible
    try:
        maybe_dict = dict(payload)
        return model_cls(**maybe_dict)
    except Exception as e:
        raise TypeError(f"Cannot normalize payload of type {type(payload)}: {e}")
