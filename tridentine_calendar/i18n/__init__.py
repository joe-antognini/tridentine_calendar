"""Internationalization support."""

from .base import BaseLanguageStrategy
from .factory import get_strategy, register_strategy
from .translator import Translator

__all__ = [
    "BaseLanguageStrategy",
    "Translator",
    "get_strategy",
    "register_strategy",
]
