"""English language strategy."""

import calendar
from typing import List, Optional

from tridentine_calendar.i18n.base import BaseLanguageStrategy


class EnglishStrategy(BaseLanguageStrategy):
    """Localization strategy for English."""

    lang_code = 'en'

    TEMPLATES = {
        'feast_full_name': 'the Feast of {name}',
        'commemoration_full_name': 'the Commemoration of {name}',
        'basilica_full_name': 'the Feast of the {name}',
        'basilica_commemoration_full_name': (
            'the Commemoration of the {name}'),
        'vigil_full_name': 'the Vigil of the Feast of {name}',
        'vigil_generic_full_name': 'the {name}',
        'ordinal_sunday_full_name': '{ordinal} Sunday of {season}',
        'ordinal_sunday_after_full_name': '{ordinal} Sunday after {event}',
        'last_sunday_full_name': 'Last Sunday after {event}',
        'feria_in_lent': '{weekday} in the {ordinal} week of Lent',
        'feria_after_ash_wednesday': '{weekday} after Ash Wednesday',
        'feria_in_passion_week': '{weekday} in Passion week',
        'class_feria': '{name} is a Class {rank} {type}.',
        'liturgical_color': 'The liturgical color is {color}.',
        'outranking': '{feast} is outranked by {outranking_feast}.',
        'outranking_this_year': (
            'This year {feast} is outranked by {outranking_feast}.'),
        'holy_day': '{name} is a Holy Day of Obligation.',
        'no_special_liturgy': '{name} has no special liturgy.',
        'today_is_commemoration': 'Today is a commemoration.',
        'lent_commemoration': (
            'Since {feast} falls during Lent it will ordinarily be '
            'celebrated only as a commemoration during the mass of '
            '{feria}.'),
        'more_info': 'More information about {name}:',
        'types': {'feast': 'feast', 'feria': 'feria'},
        'today': 'Today',
        'this_feast': 'This feast',
        'this_feria': 'This feria',
        'calendar_name': 'Tridentine calendar',
        'calendar_desc': (
            'Liturgical calendar using the 1962 Roman Catholic rubrics.'),
    }

    ORDINALS = {
        1: 'First', 2: 'Second', 3: 'Third', 4: 'Fourth', 5: 'Fifth',
        6: 'Sixth', 7: 'Seventh', 8: 'Eighth', 9: 'Ninth', 10: 'Tenth',
        11: 'Eleventh', 12: 'Twelfth', 13: 'Thirteenth',
        14: 'Fourteenth', 15: 'Fifteenth', 16: 'Sixteenth',
        17: 'Seventeenth', 18: 'Eighteenth', 19: 'Nineteenth',
        20: 'Twentieth', 21: 'Twenty-first', 22: 'Twenty-second',
        23: 'Twenty-third', 24: 'Twenty-fourth', 25: 'Twenty-fifth',
        26: 'Twenty-sixth', 27: 'Twenty-seventh',
    }

    def _load_data(self) -> None:
        self.templates = dict(self.TEMPLATES)
        self.ordinals = dict(self.ORDINALS)
        self.weekdays = {day: day for day in calendar.day_name}

    def format_season_name(self, name: str) -> str:
        translated_name = self.translate(name)
        if name.startswith('Time after'):
            return 'the ' + translated_name
        return translated_name

    def format_feria_in_lent(self, lent_week: int, weekday: str) -> str:
        ordinal = self.get_ordinal(lent_week).lower()
        return self.templates['feria_in_lent'].format(
            ordinal=ordinal, weekday=weekday
        )

    def format_feast_full_name(
        self,
        name: str,
        rank: int,
        titles: Optional[List[str]] = None,
        is_feast: bool = True
    ) -> str:
        translated_name = self.translate(name)
        if titles:
            titles_str = self.format_titles(titles)
            if titles_str:
                translated_name = f"{translated_name} ({titles_str})"

        the_feast_of_prefixes = ['St.', 'SS.', 'Pope', 'Our Lady', 'The']
        other_the_feasts = ['Christ the King']

        if any([name.split()[0] in the_feast_of_prefixes,
               name in other_the_feasts]):
            name_to_use = (translated_name[0].lower() + translated_name[1:]
                           if name.startswith('The') else translated_name)
            template = (
                'feast_full_name' if rank != 4 else 'commemoration_full_name')
            return self.templates[template].format(name=name_to_use)
        elif name.split()[0] in ['Basilica', 'Baptism', 'Church']:
            template = (
                'basilica_full_name' if rank != 4
                else 'basilica_commemoration_full_name')
            return self.templates[template].format(name=translated_name)
        elif name.split()[0] == 'Vigil':
            if name.split()[2] in the_feast_of_prefixes:
                name_val = ' '.join(name.split()[2:])
                if titles:
                    titles_str = self.format_titles(titles)
                    if titles_str:
                        name_val = f"{name_val} ({titles_str})"
                return self.templates['vigil_full_name'].format(
                    name=name_val)
            return self.templates['vigil_generic_full_name'].format(
                name=translated_name
            )
        elif any([(name.split()[0] in self.ordinals.values()
                   and name.split()[1] == 'Sunday'),
                  name.startswith('Last Sunday'),
                  name.startswith('Feast')]):
            return self.templates['vigil_generic_full_name'].format(
                name=translated_name
            )
        else:
            return translated_name

    def format_class_feria(self, name: str, rank: int, is_feast: bool) -> str:
        type_str = (self.templates['types']['feast'] if is_feast
                    else self.templates['types']['feria'])
        rank_str = rank * 'I'
        return self.templates['class_feria'].format(
            name=name, rank=rank_str, type=type_str)

    def format_color(self, color: str) -> str:
        return self.templates['liturgical_color'].format(color=color.lower())

    def format_titles(self, titles: List[str], plural: bool = False) -> str:
        if not titles:
            return ""
        translated_titles = [self.translate(t) for t in titles]
        translated_titles = [
            t[0].upper() + t[1:] if t else t
            for t in translated_titles
        ]
        return ", ".join(translated_titles)
