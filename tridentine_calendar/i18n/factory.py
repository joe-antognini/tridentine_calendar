"""Factory for obtaining language strategies."""

from typing import Dict, Type

from .base import BaseLanguageStrategy
from .strategies.english import EnglishStrategy
from .strategies.french import FrenchStrategy
from .strategies.japanese import JapaneseStrategy

STRATEGIES: Dict[str, Type[BaseLanguageStrategy]] = {
    'en': EnglishStrategy,
    'fr': FrenchStrategy,
    'ja': JapaneseStrategy,
}


def register_strategy(
    lang: str,
    strategy_class: Type[BaseLanguageStrategy]
) -> None:
    """Register a new language strategy."""
    STRATEGIES[lang] = strategy_class


def get_strategy(lang: str = 'en') -> BaseLanguageStrategy:
    """Get a strategy instance for the given language code."""
    strategy_cls = STRATEGIES.get(lang, EnglishStrategy)
    return strategy_cls()
