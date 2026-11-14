"""Tests for language strategies and strategy factory."""

from tridentine_calendar.i18n import (
    BaseLanguageStrategy,
    Translator,
    get_strategy,
    register_strategy,
)
from tridentine_calendar.i18n.strategies.english import EnglishStrategy
from tridentine_calendar.i18n.strategies.french import FrenchStrategy
from tridentine_calendar.i18n.strategies.japanese import JapaneseStrategy


def test_get_strategy():
    assert isinstance(get_strategy('en'), EnglishStrategy)
    assert isinstance(get_strategy('fr'), FrenchStrategy)
    assert isinstance(get_strategy('ja'), JapaneseStrategy)
    # Default fallback is English
    assert isinstance(get_strategy('unknown_lang'), EnglishStrategy)


def test_register_strategy():
    class MockLatinStrategy(BaseLanguageStrategy):
        lang_code = 'la'

        def format_feast_full_name(self, name, rank, titles=None, is_feast=True):
            return f"Festum {name}"

        def format_class_feria(self, name, rank, is_feast):
            return f"{name} classis {rank}"

        def format_color(self, color):
            return f"Color: {color}"

        def format_titles(self, titles, plural=False):
            return ", ".join(titles)

    register_strategy('la', MockLatinStrategy)
    strat = get_strategy('la')
    assert isinstance(strat, MockLatinStrategy)
    assert strat.format_feast_full_name('Sancti Joseph', 1) == "Festum Sancti Joseph"

    # Translator facade also instantiates the registered strategy
    trans = Translator(lang='la')
    assert trans.lang == 'la'
    assert trans.format_feast_full_name('Sancti Joseph', 1) == "Festum Sancti Joseph"


def test_translator_facade_backward_compatibility():
    # Test class-level TEMPLATES
    assert 'en' in Translator.TEMPLATES
    assert 'fr' in Translator.TEMPLATES
    assert 'ja' in Translator.TEMPLATES

    trans_en = Translator('en')
    assert trans_en.lang == 'en'
    assert trans_en.get_ordinal(1) == 'First'
    assert trans_en.translate('Monday') == 'Monday'
    assert trans_en._contract('de le') == 'de le'

    trans_fr = Translator('fr')
    assert trans_fr.lang == 'fr'
    assert trans_fr.get_ordinal(1) == 'premier'
    assert trans_fr.translate('Monday') == 'Lundi'
    assert trans_fr._contract('de le vin') == 'du vin'
    assert trans_fr._is_plural('Les apôtres') is True
    assert trans_fr._is_plural('St Pierre') is False

    trans_ja = Translator('ja')
    assert trans_ja.lang == 'ja'
    assert trans_ja.get_ordinal(1) == '第一'
    assert trans_ja.translate('Monday') == '月曜日'
    assert trans_ja.format_titles(['Bishop', 'Confessor']) == '司教、証聖者'


def test_translator_lang_setter():
    trans = Translator('en')
    assert trans.lang == 'en'
    assert trans.translate('Monday') == 'Monday'

    # Switch language via setter
    trans.lang = 'fr'
    assert trans.lang == 'fr'
    assert trans.translate('Monday') == 'Lundi'
