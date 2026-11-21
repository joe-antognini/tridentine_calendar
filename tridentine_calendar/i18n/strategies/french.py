"""French language strategy."""

from typing import List, Optional

from tridentine_calendar.i18n.base import BaseLanguageStrategy
from tridentine_calendar.utils import make_initial__the__lowercase


class FrenchStrategy(BaseLanguageStrategy):
    """Localization strategy for French."""

    lang_code = 'fr'

    TEMPLATES = {
        'feast_full_name': 'la fête de {name}',
        'commemoration_full_name': 'la commémoraison de {name}',
        'basilica_full_name': 'la fête de {name}',
        'basilica_commemoration_full_name': (
            'la commémoraison de {name}'),
        'vigil_full_name': 'la vigile de la fête de {name}',
        'vigil_generic_full_name': '{name}',
        'ordinal_sunday_full_name': '{ordinal} dimanche de {season}',
        'ordinal_sunday_after_full_name': '{ordinal} dimanche après {event}',
        'last_sunday_full_name': 'Dernier dimanche après {event}',
        'feria_in_lent': '{weekday} de la {ordinal} semaine de Carême',
        'feria_after_ash_wednesday': '{weekday} après le Mercredi des Cendres',
        'feria_in_passion_week': '{weekday} de la semaine de la Passion',
        'class_feria': '{name} est une {type} de {rank}.',
        'liturgical_color': 'La couleur liturgique est le {color}.',
        'outranking': '{feast} est omise.',
        'outranking_this_year': 'Cette année, {feast} est omise.',
        'holy_day': '{name} est un jour d\'obligation.',
        'no_special_liturgy': '{name} n\'a pas de liturgie spéciale.',
        'today_is_commemoration': 'Aujourd\'hui, c\'est une commémoraison.',
        'lent_commemoration': (
            'Puisque {feast} tombe pendant le Carême, il sera ordinairement '
            'célébré seulement comme une commémoraison pendant la messe de '
            '{feria}.'),
        'more_info': 'Plus d\'informations sur {name} :',
        'types': {'feast': 'fête', 'feria': 'férie'},
        'today': 'Aujourd\'hui',
        'this_feast': 'Cette fête',
        'this_feria': 'Cette férie',
        'calendar_name': 'Calendrier Tridentin',
        'calendar_desc': (
            'Calendrier liturgique utilisant les rubriques de 1962 de '
            'l\'Église catholique romaine.'),
    }

    ORDINALS = {
        1: 'premier', 2: 'deuxième', 3: 'troisième', 4: 'quatrième',
        5: 'cinquième', 6: 'sixième', 7: 'septième', 8: 'huitième',
        9: 'neuvième', 10: 'dixième', 11: 'onzième', 12: 'douzième',
        13: 'treizième', 14: 'quatorzième', 15: 'quinzième',
        16: 'seizième', 17: 'dix-septième', 18: 'dix-huitième',
        19: 'dix-neuvième', 20: 'vingtième', 21: 'vingt-et-unième',
        22: 'vingt-deuxième', 23: 'vingt-troisième', 24: 'vingt-quatrième',
        25: 'vingt-cinquième', 26: 'vingt-sixième', 27: 'vingt-septième',
    }

    WEEKDAYS = {
        'Monday': 'Lundi', 'Tuesday': 'Mardi', 'Wednesday': 'Mercredi',
        'Thursday': 'Jeudi', 'Friday': 'Vendredi', 'Saturday': 'Samedi',
        'Sunday': 'Dimanche'
    }

    CORE_OVERRIDES = {
        'Epiphany': "l'Épiphanie",
        'Pentecost': 'la Pentecôte',
        'Easter': 'Pâques',
        'Advent': "l'Avent",
        'Lent': 'le Carême',
        'Ascension': "l'Ascension",
    }

    def _load_data(self) -> None:
        self.templates = dict(self.TEMPLATES)
        self.ordinals = dict(self.ORDINALS)
        self.weekdays = dict(self.WEEKDAYS)

        self._load_csv('i18n/fr/feasts_seasons.csv', 'en', 'fr')
        self._load_csv('i18n/fr/titles_lexicon.csv', 'en', 'fr')
        self._load_csv('i18n/fr/color_lexicon.csv', 'en', 'fr')
        self._load_csv('i18n/fr/class_lexicon.csv', 'en', 'fr')

        for en, fr in self.CORE_OVERRIDES.items():
            self.translations[en] = fr

    def _contract(self, text: str) -> str:
        """Apply French contractions and elisions."""
        # Clean up any double articles that might have been introduced
        text = text.replace('le le ', 'le ')
        text = text.replace('la la ', 'la ')
        text = text.replace('le la ', 'la ')
        text = text.replace('la le ', 'le ')
        text = text.replace("l'l'", "l'")
        text = text.replace("le l'", "l'")
        text = text.replace("la l'", "l'")

        # Contractions
        text = text.replace('de le ', 'du ')
        text = text.replace('de les ', 'des ')
        text = text.replace('de la Dimanche', 'du Dimanche')

        # Elisions
        vowels = 'aeiouyàâéèêëîïôûùh'
        for v in vowels:
            text = text.replace(f'de {v}', f"de l'{v}")
            text = text.replace(f'de {v.upper()}', f"de l'{v.upper()}")

        # Special cases for le/la
        for v in vowels:
            text = text.replace(f'le {v}', f"l'{v}")
            text = text.replace(f'le {v.upper()}', f"l'{v.upper()}")
            text = text.replace(f'la {v}', f"l'{v}")
            text = text.replace(f'la {v.upper()}', f"l'{v.upper()}")

        # Final cleanup
        text = text.replace('de du ', 'du ')
        text = text.replace('de des ', 'des ')
        text = text.replace("de l'l'", "de l'")
        text = text.replace('de le ', 'du ')
        text = text.replace('de les ', 'des ')

        return text

    def _is_plural(self, name: str) -> bool:
        plural_prefixes = ('Les ', 'les ', 'Sts ', 'Stes ', 'sts ', 'stes ')
        return name.lstrip('» ').lstrip('› ').startswith(plural_prefixes)

    def format_season_name(self, name: str) -> str:
        return self._contract(self.translate(name))

    def format_fifth_sunday_of_easter(self, ordinal: str, event_name: str) -> str:
        return self.templates['ordinal_sunday_full_name'].format(
            ordinal=ordinal, season=event_name
        )

    def format_ics_summary(self, name: str) -> str:
        ics_name = self.translate(name)
        if ics_name:
            ics_name = self._contract(ics_name)
            ics_name = ics_name[0].upper() + ics_name[1:]
        return ics_name

    def format_more_info(self, name: str) -> str:
        return self._contract(self.templates['more_info'].format(name=name))

    def _pluralize_fr_title(self, title: str) -> str:
        """Pluralize a French title."""
        if not title:
            return title

        parts = title.split(' et ')
        plural_parts = []
        for part in parts:
            subparts = part.split(' de ')
            if len(subparts) > 1:
                plural_parts.append(
                    subparts[0] + 's de ' + ' de '.join(subparts[1:]))
            else:
                plural_parts.append(part + 's')

        return ' et '.join(plural_parts)

    def format_titles(self, titles: List[str], plural: bool = False) -> str:
        if not titles:
            return ""
        translated_titles = [self.translate(t) for t in titles]
        if plural:
            translated_titles = [
                self._pluralize_fr_title(t) for t in translated_titles
            ]
        return ", ".join(translated_titles)

    def format_feast_full_name(
        self,
        name: str,
        rank: int,
        titles: Optional[List[str]] = None,
        is_feast: bool = True
    ) -> str:
        translated_name = self.translate(name)
        is_plural = self._is_plural(translated_name)

        if titles:
            titles_str = self.format_titles(titles, plural=is_plural)
            if titles_str:
                titles_str_sing = self.format_titles(titles, plural=False)
                if (translated_name.endswith(f", {titles_str}")
                        or translated_name.endswith(f", {titles_str_sing}")):
                    pass
                else:
                    translated_name = f"{translated_name} ({titles_str})"

        is_generic_sunday = (
            'Sunday' in name or 'dimanche' in translated_name.lower())
        is_already_feast = (name.startswith('Feast')
                            or 'fête' in translated_name.lower())

        if is_already_feast or not is_feast:
            return translated_name

        if is_generic_sunday:
            if translated_name.lower().startswith(('le ', "l'", 'la ', 'les ')):
                return translated_name
            return self._contract("le " + translated_name)

        template_key = (
            'feast_full_name' if rank != 4 else 'commemoration_full_name')
        template = self.templates[template_key]

        return self._contract(template.format(name=translated_name))

    def format_class_feria(self, name: str, rank: int, is_feast: bool) -> str:
        type_str = (self.templates['types']['feast'] if is_feast
                    else self.templates['types']['feria'])
        rank_str = self.translate(str(rank))
        template = self.templates['class_feria']
        if self._is_plural(name):
            template = template.replace(' est ', ' sont ')
        return template.format(name=name, rank=rank_str, type=type_str)

    def format_color(self, color: str) -> str:
        translated_color = self.translate(color.capitalize()).lower()
        return self.templates['liturgical_color'].format(color=translated_color)

    def format_outranking(
        self,
        feast: str,
        outranking_feast: str,
        is_fixed_outranked_by_fixed: bool
    ) -> str:
        template_key = (
            'outranking' if is_fixed_outranked_by_fixed
            else 'outranking_this_year')
        template = self.templates[template_key]
        if self._is_plural(feast):
            template = template.replace(' est ', ' sont ')
            template = template.replace(' omise.', ' omises.')
        return template.format(
            feast=make_initial__the__lowercase(feast),
            outranking_feast=outranking_feast,
        )

    def format_holy_day(self, name: str) -> str:
        template = self.templates['holy_day']
        if self._is_plural(name):
            template = template.replace(' est ', ' sont ')
        return template.format(name=name)

    def format_no_special_liturgy(self, name: str) -> str:
        template = self.templates['no_special_liturgy']
        if self._is_plural(name):
            template = template.replace(" n'a pas ", " n'ont pas ")
        return template.format(name=name)
