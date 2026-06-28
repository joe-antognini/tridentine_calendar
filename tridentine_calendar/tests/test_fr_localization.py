import datetime as dt
from tridentine_calendar.i18n import Translator
from tridentine_calendar.tridentine_calendar import LiturgicalCalendar


def test_fr_translator_basic():
    translator = Translator(lang='fr')
    assert translator.translate('Monday') == 'Lundi'
    assert translator.translate('Advent') == 'Avent'
    assert translator.translate('White') == 'Blanc'
    assert translator.get_ordinal(1) == 'premier'
    assert translator.get_ordinal(2) == 'deuxième'


def test_fr_feast_full_name():
    translator = Translator(lang='fr')
    # Normal feast
    assert translator.format_feast_full_name(
        'St. Hilary', 3) == 'la fête de st Hilaire'
    # Elision (handled by L'Annonciation in CSV)
    assert translator.format_feast_full_name(
        'The Annunciation', 1) == 'L\'Annonciation'
    # Already has "La"
    assert translator.format_feast_full_name(
        'The Circumcision', 1) == 'La Circoncision'
    # Commemoration
    assert translator.format_feast_full_name(
        'St. Hilary', 4) == 'la commémoraison de st Hilaire'


def test_fr_class_feria():
    translator = Translator(lang='fr')
    assert translator.format_class_feria(
        'Aujourd\'hui', 1, True) == 'Aujourd\'hui est une fête de Ire classe.'
    assert translator.format_class_feria(
        'Cette férie', 3, False) == 'Cette férie est une férie de IIIe classe.'


def test_fr_liturgical_calendar_output():
    # Test generation for a specific date in French
    cal = LiturgicalCalendar(2024, lang='fr')
    # Jan 1st 2024 is Octave of Christmas / Circumcision
    date = dt.date(2024, 1, 1)
    events = cal[date]
    assert len(events) > 0
    # The first event should be Circumcision
    assert events[0].name == 'The Circumcision'
    assert events[0].full_name() == 'La Circoncision'

    description = events[0].generate_description()
    assert 'La couleur liturgique est le blanc.' in description
    # Since it is a holy day of obligation, "Aujourd'hui" is used instead of
    # the full name in the class_feria string
    assert "Aujourd'hui est une fête de Ire classe." in description
