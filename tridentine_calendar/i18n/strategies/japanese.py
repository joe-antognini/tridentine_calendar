"""Japanese language strategy."""

from typing import List, Optional

from tridentine_calendar.i18n.base import BaseLanguageStrategy


class JapaneseStrategy(BaseLanguageStrategy):
    """Localization strategy for Japanese."""

    lang_code = 'ja'

    TEMPLATES = {
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
    }

    ORDINALS = {
        1: '第一', 2: '第二', 3: '第三', 4: '第四', 5: '第五', 6: '第六',
        7: '第七', 8: '第八', 9: '第九', 10: '第十', 11: '第十一',
        12: '第十二', 13: '第十三', 14: '第十四', 15: '第十五',
        16: '第十六', 17: '第十七', 18: '第十八', 19: '第十九',
        20: '第二十', 21: '第二十一', 22: '第二十二', 23: '第二十三',
        24: '第二十四', 25: '第二十五', 26: '第二十六', 27: '第二十七',
    }

    WEEKDAYS = {
        'Monday': '月曜日', 'Tuesday': '火曜日', 'Wednesday': '水曜日',
        'Thursday': '木曜日', 'Friday': '金曜日', 'Saturday': '土曜日',
        'Sunday': '日曜日'
    }

    CORE_OVERRIDES = {
        'Epiphany': '公現',
        'Pentecost': '聖霊降臨',
        'Easter': '復活',
        'Advent': '待降節',
        'Lent': '四旬節',
        'Ascension': '昇天',
    }

    def _load_data(self) -> None:
        self.templates = dict(self.TEMPLATES)
        self.ordinals = dict(self.ORDINALS)
        self.weekdays = dict(self.WEEKDAYS)

        self._load_csv('i18n/ja/feasts_seasons.csv', 'en', 'ja')
        self._load_csv('i18n/ja/titles_lexicon.csv', 'en', 'ja')
        self._load_csv('i18n/ja/color_lexicon.csv', 'en', 'ja')
        self._load_csv('i18n/ja/class_lexicon.csv', 'en', 'ja')

        for en, ja in self.CORE_OVERRIDES.items():
            self.translations[en] = ja

    def format_titles(self, titles: List[str], plural: bool = False) -> str:
        if not titles:
            return ""
        translated_titles = [self.translate(t) for t in titles]
        return "、".join(translated_titles)

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

        is_generic_sunday = ('Sunday' in name or '主日' in translated_name)
        is_already_feast = (name.startswith('Feast')
                            or translated_name.startswith('祝日')
                            or '祝日' in translated_name)

        if is_generic_sunday or is_already_feast:
            return translated_name
        if rank == 4:
            return self.templates['commemoration_full_name'].format(
                name=translated_name)
        return self.templates['feast_full_name'].format(
            name=translated_name)

    def format_class_feria(self, name: str, rank: int, is_feast: bool) -> str:
        type_str = (self.templates['types']['feast'] if is_feast
                    else self.templates['types']['feria'])
        rank_str = self.translate(str(rank))
        return self.templates['class_feria'].format(
            name=name, rank=rank_str, type=type_str)

    def format_color(self, color: str) -> str:
        translated_color = self.translate(color.capitalize())
        return self.templates['liturgical_color'].format(color=translated_color)
