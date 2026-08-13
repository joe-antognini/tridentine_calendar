import datetime as dt
from unittest import mock

from tridentine_calendar.tridentine_calendar import FIXED_FEASTS_DATA
from tridentine_calendar.tridentine_calendar import LiturgicalCalendarEvent


def test_st_george_commemoration_is_red_in_all_locales():
    st_george = next(
        event
        for event in FIXED_FEASTS_DATA['April 23']
        if event['name'] == 'St. George'
    )

    assert st_george['class'] == 4
    assert st_george['titles'] == ['Martyr']
    assert st_george['liturgical_event'] is True
    assert st_george['color'] == 'Red'

    expected_colors = (
        ('en', 'Red'),
        ('fr', 'Rouge'),
        ('ja', '赤'),
    )
    with mock.patch.object(LiturgicalCalendarEvent, 'is_fixed', return_value=True):
        for lang, expected_color in expected_colors:
            event = LiturgicalCalendarEvent.from_json(
                dt.date(2027, 4, 23), st_george, lang=lang
            )

            assert event.date == dt.date(2027, 4, 23)
            assert event.name == 'St. George'
            assert event.rank == 4
            assert event.titles == ['Martyr']
            assert event.liturgical_event is True
            assert event.feast is True
            assert event.color == 'Red'
            assert event.translator.translate(event.color) == expected_color
