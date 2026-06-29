import datetime as dt
from tridentine_calendar.i18n import Translator
from tridentine_calendar.tridentine_calendar import LiturgicalCalendar

def test_repro():
    translator = Translator(lang='fr')

    # Issue 1: "La fête de Quatre-Temps de l'Avent" vs "Les Quatre-Temps de l'Avent"
    # Note: Advent Embertide is a movable feast.
    # In CSV it is currently: Advent Embertide,Quatre-Temps de l'Avent
    name1 = "Advent Embertide"
    full_name1 = translator.format_feast_full_name(name1, 2)
    print(f"Full name for {name1}: {full_name1}")

    # Issue 2: "les saints Innocents" vs "la fête des saints Innocents"
    # In CSV it is currently: Childermas,Les saints Innocents
    name2 = "Childermas"
    full_name2 = translator.format_feast_full_name(name2, 2)
    print(f"Full name for {name2}: {full_name2}")

    # Issue 3: titles pluralization
    # Childermas has title "Martyr"
    full_name2_with_titles = translator.format_feast_full_name(name2, 2, titles=["Martyr"])
    print(f"Full name for {name2} with titles: {full_name2_with_titles}")

if __name__ == "__main__":
    test_repro()
