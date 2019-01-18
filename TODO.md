* Add a `LiturgicalCalendarEvent` class.
    - Date
    - Name
    - Url
    - Class
    - Color
    - Titles
    - Whether it is a liturgical event
    - Whether it is a holy day of obligation
* Move `_name_with_article` to `utils.py`.
* Precedence with the Major Rogation and Easter.
* Switch to iCalendar from ics.
* Package the code.
* The function-name pairs are a mess.
* Remove `date` from date function names.
* Add class and title information to ICS description.
* Add color information.
* Fix the ICS writing to file.
* Add flags for the ICS conversion (exclude commemorations, etc.).
* Check to see whether we should use `append` vs `+=` for the list operations.
* Make code more efficient by running through the year only once.
* Add Holy Days of obligation for different regions.
* Add support for a one-event-per-day max.
* Support multiple years in a single `LiturgicalCalendar` object.
* Clean up the HTML vs. Markdown formatting.
