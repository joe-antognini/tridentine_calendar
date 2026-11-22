import datetime as dt

from tridentine_calendar.i18n import Translator
from tridentine_calendar.i18n.strategies.french import FrenchStrategy
from tridentine_calendar.tridentine_calendar import LiturgicalCalendar
from tridentine_calendar.tridentine_calendar import LiturgicalYear


def test_fr_translator_basic():
    translator = Translator(lang='fr')
    assert translator.translate('Monday') == 'Lundi'
    assert translator.translate('Advent') == "l'Avent"
    assert translator.translate('White') == 'Blanc'
    assert translator.get_ordinal(1) == 'premier'
    assert translator.get_ordinal(2) == 'deuxième'


def test_fr_feast_full_name():
    translator = Translator(lang='fr')
    # Normal feast
    assert translator.format_feast_full_name(
        'St. Hilary', 3) == 'la fête de St Hilaire'
    # Elision
    assert translator.format_feast_full_name(
        'The Annunciation', 1) == "la fête de l'Annonciation"
    # Already has "La"
    assert translator.format_feast_full_name(
        'The Circumcision', 1) == 'la fête de la Circoncision'
    # Commemoration
    assert translator.format_feast_full_name(
        'St. Hilary', 4) == 'la commémoraison de St Hilaire'


def test_fr_class_feria():
    translator = Translator(lang='fr')
    assert translator.format_class_feria(
        "Aujourd'hui", 1, True) == "Aujourd'hui est une fête de Ire classe."
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
    assert events[0].full_name() == 'La fête de la Circoncision'

    description = events[0].generate_description()
    assert 'La couleur liturgique est le blanc.' in description
    # Since it is a holy day of obligation, "Aujourd'hui" is used instead of
    # the full name in the class_feria string
    assert "Aujourd'hui est une fête de Ire classe." in description


def test_fr_plural_agreement():
    translator = Translator(lang='fr')

    # Test "Les"
    assert "sont" in translator.format_class_feria("Les martyrs", 2, True)
    assert "n'ont pas" in translator.format_no_special_liturgy("Les Grandes Ô")

    # Test "Sts"
    assert "sont" in translator.format_class_feria("Sts Abdon et Sennen", 3, True)

    # Test "Stes"
    assert "sont" in translator.format_class_feria("Stes Perpétue et Félicité", 3, True)

    # Test outranking plural
    outranking = translator.format_outranking("Les martyrs", "Une fête", True)
    assert outranking == "Les martyrs sont omises."

    # Test outranking singular fixed (starts capitalized)
    outranking_fixed = translator.format_outranking(
        "la commémoraison de Sts Marc et Marcellien", "La fête de St Éphrem", True
    )
    assert outranking_fixed == "La commémoraison de Sts Marc et Marcellien est omise."

    # Test outranking singular this year (starts with Cette année, next word lowercase)
    outranking_year = translator.format_outranking(
        "La commémoraison de Ste Praxède", "Le dimanche", False
    )
    assert outranking_year == "Cette année, la commémoraison de Ste Praxède est omise."

    # Test outranking masculine Sunday (est omis)
    outranking_sunday = translator.format_outranking(
        "le vingt-deuxième dimanche après la Pentecôte",
        "La fête de Le Christ-Roi",
        False
    )
    expected_sunday = (
        "Cette année, le vingt-deuxième dimanche après la Pentecôte est omis."
    )
    assert outranking_sunday == expected_sunday

    # Test holy day plural
    holy = translator.format_holy_day("Les Grandes Ô")
    assert "sont" in holy


def test_fr_fifth_sunday_of_easter():
    cal = LiturgicalCalendar(2024, lang='fr')
    date = dt.date(2024, 5, 5)
    events = cal[date]
    assert len(events) > 0
    assert events[0].name == 'cinquième dimanche de Pâques'


def test_fr_ics_export():
    import icalendar as ical
    cal = LiturgicalCalendar(2024, lang='fr')
    ics_bytes = cal.to_ical()
    assert ics_bytes is not None
    ics = ical.Calendar.from_ical(ics_bytes)
    summaries = [
        str(comp.get('summary'))
        for comp in ics.subcomponents
        if comp.name == 'VEVENT'
    ]
    assert any('Circoncision' in s for s in summaries)
    prefixes = ('La ', 'Le ', "L'", '» ', '› ')
    assert any(s.startswith(prefixes) for s in summaries)


def test_fr_omitted_commemorations_ics():
    import icalendar as ical
    cal = LiturgicalCalendar(2024, lang='fr')
    ics_bytes = cal.to_ical()
    ics = ical.Calendar.from_ical(ics_bytes)
    descriptions = [
        str(comp.get('description'))
        for comp in ics.subcomponents
        if comp.name == 'VEVENT'
    ]
    # 18 juin (Sts Marc et Marcellien)
    expected_marc = (
        'La commémoraison de Sts Marc et Marcellien (martyrs) est omise.'
    )
    assert any(d.startswith(expected_marc) for d in descriptions)

    # 19 juin (Sts Gervase et Protase)
    expected_gervase = (
        'La commémoraison de Sts Gervase et Protase (martyrs) est omise.'
    )
    assert any(d.startswith(expected_gervase) for d in descriptions)

    # 8 août (Sts Cyriacus...)
    expected_cyriacus = (
        'La commémoraison de Sts Cyriaque, Large et Smaragde (martyrs) '
        'est omise.'
    )
    assert any(d.startswith(expected_cyriacus) for d in descriptions)


def test_fr_omitted_sunday_ics():
    import icalendar as ical
    # 25 oct 2026: Christ the King outranks 22nd Sunday after Pentecost
    cal26 = LiturgicalCalendar(2026, lang='fr')
    ics26 = ical.Calendar.from_ical(cal26.to_ical())
    desc26 = [
        str(comp.get('description'))
        for comp in ics26.subcomponents
        if comp.name == 'VEVENT'
    ]
    expected_sunday_26 = (
        'Cette année, le vingt-deuxième dimanche après la Pentecôte est omis.'
    )
    assert any(d.startswith(expected_sunday_26) for d in desc26)

    # 1 nov 2020: All Saints outranks 22nd Sunday after Pentecost
    cal20 = LiturgicalCalendar(2020, lang='fr')
    ics20 = ical.Calendar.from_ical(cal20.to_ical())
    desc20 = [
        str(comp.get('description'))
        for comp in ics20.subcomponents
        if comp.name == 'VEVENT'
    ]
    assert any(d.startswith(expected_sunday_26) for d in desc20)


def _lent_commemoration_descriptions_for_date(
    year: int, target_date: dt.date
) -> list[str]:
    """Return event descriptions generated in French for a given Lenten date."""
    cal_year = LiturgicalYear(year, lang='fr')
    return [
        event.generate_description(html_formatting=False, ranking_feast=(idx == 0))
        for idx, event in enumerate(cal_year[target_date])
    ]


def test_french_lent_commemoration_female_saint_agreement():
    """Check Lenten commemoration agreement for a female saint (e.g., Mar 9, 2026)."""
    # In 2026, Ash Wednesday is Feb 18, so Mar 9 is in Lent (2nd week of Lent).
    descriptions = _lent_commemoration_descriptions_for_date(2026, dt.date(2026, 3, 9))
    joined = '\n'.join(descriptions)

    assert 'il sera ordinairement célébré' not in joined
    assert 'elle sera ordinairement célébrée' in joined


def test_french_lent_commemoration_plural_saints_agreement():
    """Check Lenten commemoration agreement for plural saints (e.g., Mar 7, 2026)."""
    # Mar 7, 2026 falls during Lent after Ash Wednesday (Feb 18, 2026).
    descriptions = _lent_commemoration_descriptions_for_date(2026, dt.date(2026, 3, 7))
    joined = '\n'.join(descriptions)

    assert 'il sera ordinairement célébré' not in joined
    assert 'elle sera ordinairement célébrée' in joined


def test_french_spouse_of_bvm_title():
    strategy = FrenchStrategy()
    formatted = strategy.format_feast_full_name(
        'St. Joseph',
        rank=1,
        titles=['Spouse of the Blessed Virgin Mary', 'Confessor'],
        is_feast=True,
    )
    assert 'Spouse of the Blessed Virgin Mary' not in formatted
    assert 'Époux' in formatted or 'époux' in formatted
    assert 'confesseur' in formatted.lower()
