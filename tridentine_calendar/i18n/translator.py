"""Translator class for internationalization support."""

from typing import Dict, List, Optional

from .base import BaseLanguageStrategy
from .factory import get_strategy
from .strategies.english import EnglishStrategy
from .strategies.french import FrenchStrategy
from .strategies.japanese import JapaneseStrategy


class Translator:
    """Handles translations and localized string formatting."""

    TEMPLATES = {
        'en': EnglishStrategy.TEMPLATES,
        'fr': FrenchStrategy.TEMPLATES,
        'ja': JapaneseStrategy.TEMPLATES,
    }

    def __init__(self, lang: str = 'en'):
        self.strategy: BaseLanguageStrategy = get_strategy(lang)

    @property
    def lang(self) -> str:
        return self.strategy.lang_code

    @lang.setter
    def lang(self, value: str) -> None:
        self.strategy = get_strategy(value)

    @property
    def translations(self) -> Dict[str, str]:
        return self.strategy.translations

    @property
    def templates(self) -> Dict[str, str]:
        return self.strategy.templates

    @property
    def ordinals(self) -> Dict[int, str]:
        return self.strategy.ordinals

    @property
    def weekdays(self) -> Dict[str, str]:
        return self.strategy.weekdays

    def translate(self, text: str) -> str:
        return self.strategy.translate(text)

    def _contract(self, text: str) -> str:
        return self.strategy._contract(text)

    def _is_plural(self, name: str) -> bool:
        return self.strategy._is_plural(name)

    def get_ordinal(self, n: int) -> str:
        return self.strategy.get_ordinal(n)

    def format_feast_full_name(
        self,
        name: str,
        rank: int,
        titles: Optional[List[str]] = None,
        is_feast: bool = True
    ) -> str:
        return self.strategy.format_feast_full_name(
            name, rank, titles=titles, is_feast=is_feast)

    def format_class_feria(self, name: str, rank: int, is_feast: bool) -> str:
        return self.strategy.format_class_feria(name, rank, is_feast)

    def format_color(self, color: str) -> str:
        return self.strategy.format_color(color)

    def format_outranking(
        self,
        feast: str,
        outranking_feast: str,
        is_fixed_outranked_by_fixed: bool
    ) -> str:
        return self.strategy.format_outranking(
            feast, outranking_feast, is_fixed_outranked_by_fixed)

    def format_holy_day(self, name: str) -> str:
        return self.strategy.format_holy_day(name)

    def format_no_special_liturgy(self, name: str) -> str:
        return self.strategy.format_no_special_liturgy(name)

    def format_commemoration(self) -> str:
        return self.strategy.format_commemoration()

    def format_lent_commemoration(self, feast_name: str, feria_name: str) -> str:
        return self.strategy.format_lent_commemoration(feast_name, feria_name)

    def format_more_info(self, name: str) -> str:
        return self.strategy.format_more_info(name)

    def format_titles(self, titles: List[str], plural: bool = False) -> str:
        return self.strategy.format_titles(titles, plural=plural)

    def _load_csv(
        self,
        resource_path: str,
        en_col: str = 'en',
        lang_col: Optional[str] = None
    ) -> None:
        self.strategy._load_csv(resource_path, en_col, lang_col)

    def __getattr__(self, name: str):
        return getattr(self.strategy, name)
