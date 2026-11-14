import datetime as dt
from tridentine_calendar.i18n import Translator
from tridentine_calendar.tridentine_calendar import LiturgicalCalendar


def test_ja_translator_basic():
    translator = Translator(lang='ja')
    assert translator.translate('Monday') == '月曜日'
    assert translator.translate('Advent') == '待降節'
    assert translator.translate('White') == '白'
    assert translator.get_ordinal(1) == '第一'
    assert translator.get_ordinal(2) == '第二'


def test_ja_feast_full_name():
    translator = Translator(lang='ja')
    # Normal feast (Class III)
    assert translator.format_feast_full_name(
        'St. Hilary', 3) == '聖ヒラリオの祝日'
    # Commemoration (Class IV)
    assert translator.format_feast_full_name(
        'St. Hilary', 4) == '聖ヒラリオの記念'
    # Feast that already starts with 'Feast' or '祝日'
    assert '祝日' in translator.format_feast_full_name('The Circumcision', 1)


def test_ja_titles():
    translator = Translator(lang='ja')
    titles = ['Bishop', 'Confessor', 'Doctor of the Church']
    assert translator.format_titles(titles) == '司教、証聖者、教会博士'


def test_ja_class_feria():
    translator = Translator(lang='ja')
    assert translator.format_class_feria(
        '今日', 1, True) == '今日は一級の祝日です。'
    assert translator.format_class_feria(
        'この平休日', 3, False) == 'この平休日は三級の平休日です。'


def test_ja_liturgical_calendar_output():
    cal = LiturgicalCalendar(2024, lang='ja')
    # Jan 1st 2024 is The Circumcision
    date = dt.date(2024, 1, 1)
    events = cal[date]
    assert len(events) > 0
    assert events[0].name == 'The Circumcision'
    desc = events[0].generate_description()
    assert '典礼色は白です。' in desc


def test_ja_local_feasts():
    # Feb 5 has Twenty-six Martyrs of Japan
    cal = LiturgicalCalendar(2024, lang='ja')
    date = dt.date(2024, 2, 5)
    events = cal[date]
    event_names = [e.name for e in events]
    assert 'Twenty-six Martyrs of Japan' in event_names
    twenty_six = next(e for e in events if e.name == 'Twenty-six Martyrs of Japan')
    assert '日本二十六聖人殉教者' in twenty_six.full_name()

    # Leap year (2024) movable local feast is on Feb 26
    feb26_events = [e.name for e in cal[dt.date(2024, 2, 26)]]
    assert 'Bls. Diogo de Carvalho & Companions' in feb26_events

    # Non-leap year (2023) movable local feast is on Feb 25
    cal_2023 = LiturgicalCalendar(2023, lang='ja')
    feb25_events = [e.name for e in cal_2023[dt.date(2023, 2, 25)]]
    assert 'Bls. Diogo de Carvalho & Companions' in feb25_events
