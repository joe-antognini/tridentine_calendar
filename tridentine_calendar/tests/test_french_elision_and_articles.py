import datetime as dt

from tridentine_calendar.i18n.strategies.french import FrenchStrategy
from tridentine_calendar.tridentine_calendar import LiturgicalYear


def test_ordinals_huit_and_onze_do_not_elide():
    """French ordinals 8 and 11 (and 18, 28) must not elide to l'/d'."""
    strategy = FrenchStrategy()

    assert strategy._contract('le huitième dimanche') == 'le huitième dimanche'
    assert strategy._contract('le onzième dimanche') == 'le onzième dimanche'
    assert strategy._contract('de huitième') == 'de huitième'
    assert strategy._contract('de onzième') == 'de onzième'


def test_hungary_and_albert_elision_and_title():
    """Verify 'Hongrie' has no elision and 'Albert le Grand' keeps 'St'."""
    strategy = FrenchStrategy()

    assert strategy._contract('de Hongrie') == 'de Hongrie'
    assert strategy._contract('de l\'Hongrie') == 'de Hongrie'

    full_albert = strategy.format_feast_full_name(
        'St. Albert the Great', rank=2, titles=['Doctor'], is_feast=True
    )
    assert 'St Albert le Grand' in full_albert
    assert 'l\'Albert le Grand' not in full_albert


def test_feast_articles_and_contractions():
    """Verify definite articles and contractions in French feast formatting."""
    strategy = FrenchStrategy()

    assert 'la fête de la Conversion de St Paul' in strategy.format_feast_full_name(
        'Conversion of St. Paul', rank=2, is_feast=True
    )
    assert 'la fête de la Décollation' in strategy.format_feast_full_name(
        'The Beheading of John the Baptist', rank=2, is_feast=True
    )
    assert 'la fête du Christ-Roi' in strategy.format_feast_full_name(
        'Christ the King', rank=1, is_feast=True
    )


def test_feast_starting_with_fete_and_peter_pence():
    """Verify feasts starting with 'Fête' and Peter's Pence formatting."""
    strategy = FrenchStrategy()

    cross_name = strategy.format_feast_full_name(
        'Roodmas', rank=2, is_feast=True
    )
    assert (
        cross_name.startswith('La Fête de la Croix')
        or 'la Fête de la Croix' in cross_name
    )
    assert 'fête de la fête' not in cross_name.lower()

    class_desc = strategy.format_class_feria(
        'La Fête de la Croix', rank=2, is_feast=True
    )
    assert class_desc.startswith('La Fête de la Croix est ')

    outranked_desc = strategy.format_outranking(
        'La Fête de la Croix', 'quinzième dimanche après la Pentecôte', False
    )
    assert outranked_desc == 'Cette année, la Fête de la Croix est omise.'

    peter_pence = strategy.format_ics_summary("Peter's Pence")
    assert (
        peter_pence == 'le Denier de Saint-Pierre'
        or 'Denier de Saint-Pierre' in peter_pence
    )


def test_liturgical_year_2026_fr_spot_checks():
    """End-to-end check on 2026 French calendar entries for elision regressions."""
    cal_2026 = LiturgicalYear(2026, lang='fr')
    ics_text = cal_2026.to_ical().to_ical().decode('utf-8', errors='ignore')

    for bad_snippet in (
        "L'huitième",
        "l'huitième",
        "L'onzième",
        "l'onzième",
        "de l'Hongrie",
        "l'Albert le Grand",
        "de Le Christ-Roi",
        "de Denier de Saint-Pierre",
    ):
        assert (
            bad_snippet not in ics_text
        ), f"Found ungrammatical snippet: {bad_snippet}"


def test_french_saint_pairs_no_apostrophe_before_et():
    """Saint pairs must use ' et ' without an apostrophe attached to 'et'."""
    strategy = FrenchStrategy()

    cyrille_methode = strategy.format_feast_full_name(
        'SS. Cyril and Methodius', rank=3, is_feast=True
    )
    assert 'Cyrille et Méthode' in cyrille_methode
    assert "Cyrill'et" not in cyrille_methode

    corneille_cyprien = strategy.format_feast_full_name(
        'Pope Cornelius & St. Cyprian', rank=3, is_feast=True
    )
    assert 'Corneille et St Cyprien' in corneille_cyprien
    assert "Corneill'et" not in corneille_cyprien


def test_french_calendar_july_7_and_sept_16_no_et_apostrophe():
    """End-to-end check on July 7 and Sept 16 in French for 'et' typos."""
    cal_2026 = LiturgicalYear(2026, lang='fr')

    for target_date in (dt.date(2026, 7, 7), dt.date(2026, 9, 16)):
        day_texts = []
        for idx, event in enumerate(cal_2026[target_date]):
            day_texts.append(event.name)
            day_texts.append(event.full_name(capitalize=True))
            day_texts.append(
                event.generate_description(
                    html_formatting=False, ranking_feast=(idx == 0)
                )
            )
        combined = '\n'.join(day_texts)
        assert (
            "'et " not in combined
        ), f"Found apostrophe before 'et' on {target_date}: {combined}"
        assert (
            "’et " not in combined
        ), f"Found curly apostrophe before 'et' on {target_date}: {combined}"
