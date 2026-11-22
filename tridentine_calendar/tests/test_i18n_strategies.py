"""Tests for language strategies and strategy factory."""

import csv
from collections import Counter
from pathlib import Path

import pytest

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


def test_strategy_season_formatting():
    en = Translator('en')
    fr = Translator('fr')
    ja = Translator('ja')

    assert en.format_season_name('Time after Epiphany') == 'the Time after Epiphany'
    assert en.format_season_name('Advent') == 'Advent'

    assert fr.format_season_name('Time after Epiphany') == "le Temps après l'Épiphanie"
    assert fr.format_season_name('Advent') == "l'Avent"

    assert ja.format_season_name('Advent') == '待降節'


def test_strategy_today_and_this_day():
    en = Translator('en')
    fr = Translator('fr')
    ja = Translator('ja')

    assert en.get_today() == 'Today'
    assert en.get_this_day(is_feast=True) == 'This feast'
    assert en.get_this_day(is_feast=False) == 'This feria'

    assert fr.get_today() == "Aujourd'hui"
    assert fr.get_this_day(is_feast=True) == 'Cette fête'
    assert fr.get_this_day(is_feast=False) == 'Cette férie'

    assert ja.get_today() == '今日'
    assert ja.get_this_day(is_feast=True) == 'この祝日'
    assert ja.get_this_day(is_feast=False) == 'この平休日'


def test_strategy_fifth_sunday_of_easter():
    en = Translator('en')
    fr = Translator('fr')
    ja = Translator('ja')

    assert (
        en.format_fifth_sunday_of_easter('Fifth', 'Easter')
        == 'Fifth Sunday after Easter'
    )
    assert fr.format_fifth_sunday_of_easter('5e', 'Pâques') == '5e dimanche de Pâques'
    assert ja.format_fifth_sunday_of_easter('第五', '復活節') == '復活節後第五主日'


def test_strategy_ics_summary():
    en = Translator('en')
    fr = Translator('fr')
    ja = Translator('ja')

    assert en.format_ics_summary('St. Hilary') == 'St. Hilary'
    assert ja.format_ics_summary('St. Hilary') == '聖ヒラリオ'

    # French contracts and capitalizes
    summary = fr.format_ics_summary('The Circumcision')
    assert summary == 'La Circoncision'


def test_strategy_feria_formatting():
    en = Translator('en')
    fr = Translator('fr')
    ja = Translator('ja')

    assert (
        en.format_feria_in_lent(1, 'Monday')
        == 'Monday in the first week of Lent'
    )
    assert (
        en.format_feria_after_ash_wednesday('Thursday')
        == 'Thursday after Ash Wednesday'
    )
    assert en.format_feria_in_passion_week('Tuesday') == 'Tuesday in Passion week'

    assert (
        fr.format_feria_in_lent(1, 'Lundi')
        == 'Lundi de la première semaine de Carême'
    )
    assert (
        fr.format_feria_after_ash_wednesday('Jeudi')
        == 'Jeudi après le Mercredi des Cendres'
    )
    assert (
        fr.format_feria_in_passion_week('Mardi')
        == 'Mardi de la semaine de la Passion'
    )

    assert ja.format_feria_in_lent(1, '月曜日') == '四旬節第一週の月曜日'
    assert ja.format_feria_after_ash_wednesday('木曜日') == '灰の水曜日後の木曜日'
    assert ja.format_feria_in_passion_week('火曜日') == '受難週の火曜日'


def test_calendar_name_and_prodid_localization():
    from tridentine_calendar.tridentine_calendar import LiturgicalCalendar
    import icalendar as ical

    en_trans = Translator('en')
    fr_trans = Translator('fr')
    ja_trans = Translator('ja')

    assert en_trans.get_calendar_name() == 'TLM Calendar'
    assert fr_trans.get_calendar_name() == 'Messe traditionnelle'
    assert ja_trans.get_calendar_name() == '特別形式のミサ暦'

    # Test backward compatibility of translate('Tridentine calendar')
    assert en_trans.translate('Tridentine calendar') == 'TLM Calendar'
    assert fr_trans.translate('Tridentine calendar') == 'Messe traditionnelle'
    assert ja_trans.translate('Tridentine calendar') == '特別形式のミサ暦'

    # Test LiturgicalCalendar.to_ical() PRODID and X-WR-CALNAME
    for lang, expected_name in [
        ('en', 'TLM Calendar'),
        ('fr', 'Messe traditionnelle'),
        ('ja', '特別形式のミサ暦'),
    ]:
        cal = LiturgicalCalendar(2024, lang=lang)
        ics_bytes = cal.to_ical()
        parsed = ical.Calendar.from_ical(ics_bytes)
        expected_prodid = f'-//Joe Antognini//{expected_name}//{lang.upper()}'
        assert parsed.get('prodid') == expected_prodid
        assert parsed.get('x-wr-calname') == expected_name


def test_outranking_capitalization():
    en_trans = Translator('en')
    fr_trans = Translator('fr')
    ja_trans = Translator('ja')

    # Fixed outranked by fixed: starts directly with feast name -> capitalized
    expected_en_fixed = (
        'The Commemoration of St. Praxedes is outranked by the Feast of '
        'St. Lawrence.'
    )
    assert en_trans.format_outranking(
        'the Commemoration of St. Praxedes', 'the Feast of St. Lawrence', True
    ) == expected_en_fixed

    assert fr_trans.format_outranking(
        'la commémoraison de Ste Praxède', 'la fête de St Laurent', True
    ) == 'La commémoraison de Ste Praxède est omise.'

    assert ja_trans.format_outranking(
        '聖プラクセデス', '聖ラウレンツィオ', True
    ) == '聖プラクセデスは聖ラウレンツィオに優先されます。'

    # Non-fixed (outranked this year): preceded by "This year" / "Cette année, "
    # -> lowercase article
    expected_en_year = (
        'This year the Commemoration of St. Praxedes is outranked by the '
        'Feast of St. Lawrence.'
    )
    assert en_trans.format_outranking(
        'The Commemoration of St. Praxedes', 'the Feast of St. Lawrence', False
    ) == expected_en_year

    assert fr_trans.format_outranking(
        'La commémoraison de Ste Praxède', 'la fête de St Laurent', False
    ) == 'Cette année, la commémoraison de Ste Praxède est omise.'

    assert fr_trans.format_outranking(
        'le vingt-deuxième dimanche après la Pentecôte',
        'la fête de Le Christ-Roi',
        False
    ) == 'Cette année, le vingt-deuxième dimanche après la Pentecôte est omis.'

    assert ja_trans.format_outranking(
        '聖プラクセデス', '聖ラウレンツィオ', False
    ) == '今年は聖プラクセデスは聖ラウレンツィオに優先されます。'


def _find_i18n_csvs() -> list[Path]:
    """Locate translation CSV files under tridentine_calendar/i18n if present."""
    pkg_root = Path(__file__).resolve().parents[1]
    i18n_dir = pkg_root / 'i18n'
    if i18n_dir.exists():
        return sorted(i18n_dir.rglob('*.csv'))
    return []


def _assert_unique_keys(csv_path: Path, key_col: str = 'en') -> None:
    """Assert that every non-empty key in `key_col` appears at most once."""
    with csv_path.open(mode='r', encoding='utf-8', newline='') as fp:
        reader = csv.DictReader(fp)
        assert reader.fieldnames and key_col in reader.fieldnames, (
            f"Missing '{key_col}' column in {csv_path}"
        )

        keys: list[str] = []
        for row_num, row in enumerate(reader, start=2):
            # Guard against unquoted commas causing extra fields in `None`
            assert None not in row, (
                f"Malformed/extra columns in {csv_path} at line {row_num}: {row}"
            )
            raw_key = row.get(key_col)
            if raw_key is not None and raw_key.strip() != '':
                keys.append(raw_key)

    counts = Counter(keys)
    duplicates = {k: v for k, v in counts.items() if v > 1}
    assert not duplicates, (
        f"Duplicate '{key_col}' keys found in {csv_path}: {duplicates}"
    )


def test_french_feasts_seasons_csv_has_unique_en_keys():
    """Ensure `feasts_seasons.csv` has no duplicate `en` keys."""
    # Adjust path if your test file sits in a different directory relative to the CSV.
    candidate_paths = [
        Path(__file__).resolve().parents[1] / 'i18n' / 'fr' / 'feasts_seasons.csv',
        Path(__file__).resolve().parent / 'feasts_seasons.csv',
    ]
    csv_path = next((p for p in candidate_paths if p.exists()), None)
    assert csv_path is not None, 'Could not locate feasts_seasons.csv'

    _assert_unique_keys(csv_path, key_col='en')


@pytest.mark.parametrize('csv_path', _find_i18n_csvs(), ids=lambda p: str(p))
def test_all_i18n_csvs_have_unique_en_keys(csv_path: Path):
    """Ensure all translation CSVs under `i18n/` have unique `en` keys."""
    _assert_unique_keys(csv_path, key_col='en')
