"""Translator class for internationalization support."""

import csv
import io
import calendar
from importlib import resources

from tridentine_calendar.utils import make_initial__the__lowercase


class Translator:
    """Handles translations and localized string formatting."""

    # Default formatting templates for English
    TEMPLATES = {
        'en': {
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
        },
        'ja': {
            'feast_full_name': '{name}の祝日',
            'commemoration_full_name': '{name}の記念',
            'basilica_full_name': '{name}の祝日',
            'basilica_commemoration_full_name': '{name}の記念',
            'vigil_full_name': '{name}の祝日の前夜祭',
            'vigil_generic_full_name': '{name}',
            'ordinal_sunday_full_name': '{season}{ordinal}主日',
            'ordinal_sunday_after_full_name': '{event}後{ordinal}主日',
            'last_sunday_full_name': '{event}後の最後の主日',
            'feria_in_lent': '四旬節{ordinal}週の{weekday}',
            'feria_after_ash_wednesday': '灰の水曜日後の{weekday}',
            'feria_in_passion_week': '受難週の{weekday}',
            'class_feria': '{name}は{rank}の{type}です。',
            'liturgical_color': '典礼色は{color}です。',
            'outranking': '{feast}は{outranking_feast}に優先されます。',
            'outranking_this_year': (
                '今年は{feast}は{outranking_feast}に優先されます。'),
            'holy_day': '{name}は守るべき祝日です。',
            'no_special_liturgy': '{name}には特別な典礼はありません。',
            'today_is_commemoration': '今日は記念日です。',
            'today': '今日',
            'this_feast': 'この祝日',
            'this_feria': 'この平休日',
            'lent_commemoration': (
                '{feast}は四旬節中のため、通常は{feria}のミサの中で記念としてのみ'
                '祝われます。'),
            'more_info': '{name}についての詳細情報：',
            'types': {'feast': '祝日', 'feria': '平休日'},
            'calendar_name': 'トリエント典礼暦',
            'calendar_desc': '1962年のローマ・カトリックの規定に基づく典礼暦。',
        },
        'fr': {
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
    }

    def __init__(self, lang='en'):
        self.lang = lang
        self.translations = {}
        self.templates = self.TEMPLATES.get(lang, self.TEMPLATES['en'])
        self._load_ordinals()
        self._load_weekdays()
        if lang == 'ja':
            self._load_ja()
        elif lang == 'fr':
            self._load_fr()

    def _load_ordinals(self):
        if self.lang == 'ja':
            self.ordinals = {
                1: '第一', 2: '第二', 3: '第三', 4: '第四', 5: '第五', 6: '第六',
                7: '第七', 8: '第八', 9: '第九', 10: '第十', 11: '第十一',
                12: '第十二', 13: '第十三', 14: '第十四', 15: '第十五',
                16: '第十六', 17: '第十七', 18: '第十八', 19: '第十九',
                20: '第二十', 21: '第二十一', 22: '第二十二', 23: '第二十三',
                24: '第二十四', 25: '第二十五', 26: '第二十六', 27: '第二十七',
            }
        elif self.lang == 'fr':
            self.ordinals = {
                1: 'premier', 2: 'deuxième', 3: 'troisième', 4: 'quatrième',
                5: 'cinquième', 6: 'sixième', 7: 'septième', 8: 'huitième',
                9: 'neuvième', 10: 'dixième', 11: 'onzième', 12: 'douzième',
                13: 'treizième', 14: 'quatorzième', 15: 'quinzième',
                16: 'seizième', 17: 'dix-septième', 18: 'dix-huitième',
                19: 'dix-neuvième', 20: 'vingtième', 21: 'vingt-et-unième',
                22: 'vingt-deuxième', 23: 'vingt-troisième', 24: 'vingt-quatrième',
                25: 'vingt-cinquième', 26: 'vingt-sixième', 27: 'vingt-septième',
            }
        else:
            self.ordinals = {
                1: 'First', 2: 'Second', 3: 'Third', 4: 'Fourth', 5: 'Fifth',
                6: 'Sixth', 7: 'Seventh', 8: 'Eighth', 9: 'Ninth', 10: 'Tenth',
                11: 'Eleventh', 12: 'Twelfth', 13: 'Thirteenth',
                14: 'Fourteenth', 15: 'Fifteenth', 16: 'Sixteenth',
                17: 'Seventeenth', 18: 'Eighteenth', 19: 'Nineteenth',
                20: 'Twentieth', 21: 'Twenty-first', 22: 'Twenty-second',
                23: 'Twenty-third', 24: 'Twenty-fourth', 25: 'Twenty-fifth',
                26: 'Twenty-sixth', 27: 'Twenty-seventh',
            }

    def _load_weekdays(self):
        if self.lang == 'ja':
            self.weekdays = {
                'Monday': '月曜日', 'Tuesday': '火曜日', 'Wednesday': '水曜日',
                'Thursday': '木曜日', 'Friday': '金曜日', 'Saturday': '土曜日',
                'Sunday': '日曜日'
            }
        elif self.lang == 'fr':
            self.weekdays = {
                'Monday': 'Lundi', 'Tuesday': 'Mardi', 'Wednesday': 'Mercredi',
                'Thursday': 'Jeudi', 'Friday': 'Vendredi', 'Saturday': 'Samedi',
                'Sunday': 'Dimanche'
            }
        else:
            self.weekdays = {day: day for day in calendar.day_name}

    def _load_ja(self):
        # Load main terms
        self._load_csv('i18n/ja/feasts_seasons.csv', 'en', 'ja')
        self._load_csv('i18n/ja/titles_lexicon.csv', 'en', 'ja')
        self._load_csv('i18n/ja/color_lexicon.csv', 'en', 'ja')
        self._load_csv('i18n/ja/class_lexicon.csv', 'en', 'ja')

        # Add or override core terms for better Sunday/Feria construction
        core_overrides = {
            'Epiphany': '公現',
            'Pentecost': '聖霊降臨',
            'Easter': '復活',
            'Advent': '待降節',
            'Lent': '四旬節',
            'Ascension': '昇天',
        }
        for en, ja in core_overrides.items():
            self.translations[en] = ja

    def _load_fr(self):
        # Load main terms
        self._load_csv('i18n/fr/feasts_seasons.csv', 'en', 'fr')
        self._load_csv('i18n/fr/titles_lexicon.csv', 'en', 'fr')
        self._load_csv('i18n/fr/color_lexicon.csv', 'en', 'fr')
        self._load_csv('i18n/fr/class_lexicon.csv', 'en', 'fr')

        # Add or override core terms for better Sunday/Feria construction
        core_overrides = {
            'Epiphany': "l'Épiphanie",
            'Pentecost': 'la Pentecôte',
            'Easter': 'Pâques',
            'Advent': "l'Avent",
            'Lent': 'le Carême',
            'Ascension': "l'Ascension",
        }
        for en, fr in core_overrides.items():
            self.translations[en] = fr

    def _load_csv(self, resource_path, en_col, lang_col):
        try:
            package_path = resource_path.split('/')
            filename = package_path[-1]
            directory = '.'.join(['tridentine_calendar'] + package_path[:-1])

            content = (resources.files(directory) / filename).read_bytes()
            if self.lang == 'ja':
                decoded_content = content.decode('shift_jis')
            else:
                decoded_content = content.decode('utf-8')
            reader = csv.DictReader(io.StringIO(decoded_content))
            for row in reader:
                en_val = row.get(en_col)
                lang_val = row.get(lang_col)
                if en_val and lang_val:
                    self.translations[en_val] = lang_val
        except FileNotFoundError:
            # Resource not found, skip
            pass
        except UnicodeDecodeError:
            # Encoding issue, skip
            pass
        except Exception as e:
            # Log other unexpected errors or ignore
            print(f"Error loading translation file {resource_path}: {e}")

    def translate(self, text):
        if self.lang == 'en':
            return text
        if text in self.weekdays:
            return self.weekdays[text]
        return self.translations.get(text, text)

    def _contract(self, text):
        """Apply French contractions and elisions."""
        if self.lang != 'fr':
            return text

        # Clean up any double articles that might have been introduced
        # (e.g., from translated names that already have articles)
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

    def _is_plural(self, name):
        if self.lang != 'fr':
            return False
        plural_prefixes = ('Les ', 'les ', 'Sts ', 'Stes ', 'sts ', 'stes ')
        return name.lstrip('» ').lstrip('› ').startswith(plural_prefixes)

    def get_ordinal(self, n):
        return self.ordinals.get(n, str(n))

    def format_feast_full_name(self, name, rank, titles=None):
        translated_name = self.translate(name)
        if titles:
            titles_str = self.format_titles(titles)
            if titles_str:
                translated_name = f"{translated_name} ({titles_str})"

        the_feast_of_prefixes = ['St.', 'SS.', 'Pope', 'Our Lady', 'The']
        other_the_feasts = ['Christ the King']

        # Check if it's a Sunday or a Feast starting with 'Feast'
        is_generic_sunday = (
            'Sunday' in name or '主日' in translated_name
            or 'dimanche' in translated_name.lower())
        is_already_feast = (name.startswith('Feast')
                            or translated_name.startswith('祝日'))

        if self.lang == 'ja':
            if is_generic_sunday or is_already_feast:
                return translated_name
            if rank == 4:
                return self.templates['commemoration_full_name'].format(
                    name=translated_name)
            return self.templates['feast_full_name'].format(
                name=translated_name)

        if self.lang == 'fr':
            if is_already_feast:
                return translated_name

            template_key = (
                'feast_full_name' if rank != 4 else 'commemoration_full_name')
            template = self.templates[template_key]

            return self._contract(template.format(name=translated_name))

        # English logic
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

    def format_class_feria(self, name, rank, is_feast):
        type_str = (self.templates['types']['feast'] if is_feast
                    else self.templates['types']['feria'])
        if self.lang == 'ja':
            rank_str = self.translate(str(rank))
        elif self.lang == 'fr':
            rank_str = self.translate(str(rank))
        else:
            rank_str = rank * 'I'

        template = self.templates['class_feria']
        if self._is_plural(name):
            template = template.replace(' est ', ' sont ')

        return template.format(
            name=name, rank=rank_str, type=type_str)

    def format_color(self, color):
        translated_color = self.translate(color.capitalize())
        if self.lang == 'en':
            translated_color = color.lower()
        elif self.lang == 'fr':
            translated_color = translated_color.lower()
        return self.templates['liturgical_color'].format(color=translated_color)

    def format_outranking(
            self, feast, outranking_feast, is_fixed_outranked_by_fixed):
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

    def format_holy_day(self, name):
        template = self.templates['holy_day']
        if self._is_plural(name):
            template = template.replace(' est ', ' sont ')
        return template.format(name=name)

    def format_no_special_liturgy(self, name):
        template = self.templates['no_special_liturgy']
        if self._is_plural(name):
            template = template.replace(' n\'a pas ', ' n\'ont pas ')
        return template.format(name=name)

    def format_commemoration(self):
        return self.templates['today_is_commemoration']

    def format_lent_commemoration(self, feast_name, feria_name):
        return self.templates['lent_commemoration'].format(
            feast=feast_name, feria=feria_name)

    def format_more_info(self, name):
        return self.templates['more_info'].format(name=name)

    def format_titles(self, titles):
        if not titles:
            return ""
        translated_titles = [self.translate(t) for t in titles]
        if self.lang == 'en':
            translated_titles = [
                t[0].upper() + t[1:] if t else t
                for t in translated_titles
            ]
        if self.lang == 'ja':
            return "、".join(translated_titles)
        return ", ".join(translated_titles)
