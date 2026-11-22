from tridentine_calendar.i18n.strategies.french import FrenchStrategy


def test_french_female_martyr_title_agreement():
    """Female virgin-martyrs should render '(vierge, martyre)', not 'martyr'."""
    strategy = FrenchStrategy()

    for feast_key in (
        'St. Bibiana',
        'St. Lucy',
        'St. Agnes',
        'St. Agatha',
        'St. Cecilia',
    ):
        full = strategy.format_feast_full_name(
            feast_key, rank=3, titles=['Virgin', 'Martyr'], is_feast=True
        )
        assert 'martyre' in full, (
            f'Expected feminine martyre for {feast_key}: {full}'
        )
        assert ', martyr)' not in full, (
            f'Found masculine martyr for {feast_key}: {full}'
        )


def test_french_male_martyr_stays_masculine():
    """Male martyrs should still use masculine 'martyr'."""
    strategy = FrenchStrategy()

    full = strategy.format_feast_full_name(
        'St. Lawrence', rank=2, titles=['Martyr'], is_feast=True
    )
    assert '(martyr)' in full
