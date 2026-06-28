from tridentine_calendar.i18n import Translator


def test_fr_pape_redundancy():
    translator = Translator(lang='fr')

    # Test case provided by the user
    name = "Pope Melchiades"
    titles = ["Pope", "Martyr"]
    full_name = translator.format_feast_full_name(name, 3, titles)
    # The current (buggy) output is "la fête de st Miltiade, pape (pape, martyr)"
    # The expected output is "la fête de st Miltiade (pape, martyr)"
    assert "pape (" in full_name or not full_name.endswith(", pape")
    assert ", pape (" not in full_name
    assert full_name == "la fête de st Miltiade (pape, martyr)"


def test_fr_papes_redundancy():
    translator = Translator(lang='fr')

    name = "SS. Soter & Caius"
    titles = ["Pope", "Martyr"]
    full_name = translator.format_feast_full_name(name, 3, titles)
    # Current: "la fête de sts Sôter et Caïus, papes (pape, martyr)"
    # Expected: "la fête de sts Sôter et Caïus (pape, martyr)"
    assert ", papes (" not in full_name
    assert full_name == "la fête de sts Sôter et Caïus (pape, martyr)"
