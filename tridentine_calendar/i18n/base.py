"""Base class for language strategies."""

from abc import ABC, abstractmethod
import csv
import enum
import io
from importlib import resources
from typing import Any, Dict, List, Optional

from tridentine_calendar.utils import make_initial__the__lowercase


class Gender(enum.StrEnum):
    MASCULINE = 'masculine'
    FEMININE = 'feminine'
    NEUTER = 'neuter'


class BaseLanguageStrategy(ABC):
    """Abstract base strategy for language-specific translation and formatting."""

    lang_code: str
    templates: Dict[str, str] = {}
    ordinals: Dict[int, str] = {}
    weekdays: Dict[str, str] = {}

    def __init__(self):
        self.translations: Dict[str, str] = {}
        self.templates = dict(self.templates)
        self.ordinals = dict(self.ordinals)
        self.weekdays = dict(self.weekdays)
        self._load_data()

    @property
    def lang(self) -> str:
        """Alias for lang_code to maintain backward compatibility."""
        return self.lang_code

    def _load_data(self) -> None:
        """Hook for subclasses to load lexicons, ordinals, and weekdays."""
        pass

    def _load_csv(
        self,
        resource_path: str,
        en_col: str = 'en',
        lang_col: Optional[str] = None
    ) -> None:
        """Load translation terms from a CSV resource."""
        if lang_col is None:
            lang_col = self.lang_code
        try:
            package_path = resource_path.split('/')
            filename = package_path[-1]
            directory = '.'.join(['tridentine_calendar'] + package_path[:-1])

            content = (resources.files(directory) / filename).read_bytes()
            decoded_content = content.decode('utf-8')
            reader = csv.DictReader(io.StringIO(decoded_content))
            for row in reader:
                en_val = row.get(en_col) or row.get('en')
                lang_val = (
                    row.get(lang_col)
                    or row.get('translated')
                    or row.get(self.lang_code)
                )
                if en_val and lang_val:
                    self.translations[en_val] = lang_val
        except FileNotFoundError:
            pass
        except UnicodeDecodeError:
            pass
        except Exception as e:
            print(f"Error loading translation file {resource_path}: {e}")

    def translate(self, text: str) -> str:
        """Translate a single term or return the original text."""
        if text in self.weekdays:
            return self.weekdays[text]
        if text in ('Tridentine calendar', 'Tridentine Calendar'):
            return self.get_calendar_name()
        return self.translations.get(text, text)

    def get_calendar_name(self) -> str:
        """Get the localized calendar name."""
        return self.templates.get('calendar_name', 'TLM Calendar')

    def get_calendar_description(self) -> str:
        """Get the localized calendar description."""
        return self.templates.get(
            'calendar_desc',
            'Liturgical calendar using the 1962 Roman Catholic rubrics.',
        )

    def get_ordinal(self, n: int, gender: Optional[Gender] = None) -> str:
        """Return the localized ordinal for an integer."""
        return self.ordinals.get(n, str(n))

    def _contract(self, text: str) -> str:
        """Hook for grammatical contractions/elisions (default no-op)."""
        return text

    def _is_plural(self, name: str) -> bool:
        """Hook to determine if a name is plural (default False)."""
        return False

    @abstractmethod
    def format_feast_full_name(
        self,
        name: str,
        rank: int,
        titles: Optional[List[str]] = None,
        is_feast: bool = True
    ) -> str:
        """Format the full display name of a feast or liturgical day."""
        pass

    @abstractmethod
    def format_class_feria(self, name: str, rank: int, is_feast: bool) -> str:
        """Format class description (e.g. 'Class I feast')."""
        pass

    @abstractmethod
    def format_color(self, color: str) -> str:
        """Format liturgical color announcement."""
        pass

    @abstractmethod
    def format_titles(self, titles: List[str], plural: bool = False) -> str:
        """Format and join saintly titles."""
        pass

    def format_outranking(
        self,
        feast: str,
        outranking_feast: str,
        is_fixed_outranked_by_fixed: bool
    ) -> str:
        """Format announcement that a feast is outranked."""
        template_key = (
            'outranking' if is_fixed_outranked_by_fixed
            else 'outranking_this_year'
        )
        template = self.templates[template_key]
        if is_fixed_outranked_by_fixed:
            formatted_feast = feast[0].upper() + feast[1:] if feast else feast
        else:
            formatted_feast = make_initial__the__lowercase(feast)
        return template.format(
            feast=formatted_feast,
            outranking_feast=outranking_feast,
        )

    def format_holy_day(self, name: str) -> str:
        """Format Holy Day of Obligation announcement."""
        return self.templates['holy_day'].format(name=name)

    def format_no_special_liturgy(self, name: str) -> str:
        """Format no special liturgy announcement."""
        return self.templates['no_special_liturgy'].format(name=name)

    def format_commemoration(self) -> str:
        """Format commemoration announcement."""
        return self.templates['today_is_commemoration']

    def format_lent_commemoration(self, feast_name: str, feria_name: str) -> str:
        """Format Lent commemoration explanation."""
        return self.templates['lent_commemoration'].format(
            feast=feast_name, feria=feria_name
        )

    def format_more_info(self, name: str) -> str:
        """Format more information header."""
        return self.templates['more_info'].format(name=name)

    def format_season_name(self, name: str) -> str:
        """Format the name of a liturgical season."""
        return self.translate(name)

    def get_today(self) -> str:
        """Get the localized word for 'Today'."""
        return self.templates.get('today', 'Today')

    def get_this_day(self, is_feast: bool) -> str:
        """Get the localized demonstrative noun ('This feast' / 'This feria')."""
        key = 'this_feast' if is_feast else 'this_feria'
        return self.templates.get(key, 'This feast' if is_feast else 'This feria')

    def format_fifth_sunday_of_easter(self, ordinal: str, event_name: str) -> str:
        """Format the 5th Sunday after Easter (Rogate Sunday)."""
        return self.templates['ordinal_sunday_after_full_name'].format(
            ordinal=ordinal, event=event_name
        )

    def format_ics_summary(self, name: str) -> str:
        """Format event summary for ICS calendar exports."""
        return self.translate(name)

    def format_feria_in_lent(self, lent_week: int, weekday: str) -> str:
        """Format the name of a feria during Lent."""
        ordinal = self.get_ordinal(lent_week)
        return self.templates['feria_in_lent'].format(
            ordinal=ordinal, weekday=weekday
        )

    def format_feria_after_ash_wednesday(self, weekday: str) -> str:
        """Format the name of a feria after Ash Wednesday."""
        return self.templates['feria_after_ash_wednesday'].format(weekday=weekday)

    def format_feria_in_passion_week(self, weekday: str) -> str:
        """Format the name of a feria during Passion week."""
        return self.templates['feria_in_passion_week'].format(weekday=weekday)

    def load_local_calendar_feasts(
        self,
        calendar_dict: Dict,
        year: int,
        event_cls: Any,
        translator: Any = None
    ) -> None:
        """Optional hook for region/language-specific local feasts (e.g. Japan)."""
        pass
