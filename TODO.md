* Fix Epiphany bug.
* Add bullet points to URL list.
* Fix Season URLs.
* Fix article when the name begins with "Feast".
* Fix article when name begins with "Pope".
* Fix capitalization with multiple saints. (See Pope Fabian.)
* Fix bug with "this year" calculation.
* The Conversion of St. Paul is listed twice.
* Try to format the URLs with HTML.
* Add class and title information to ICS description.
* Fix the ICS writing to file.
* Find a character that is after alphabetical characters for outranked feasts.
* See if holy day of obligation needs to be capitalized.
* Make a separate `utils.py` file.
* Write out superseding seasonal URLs as well.
* Insert events in order of precedence.
* Write a CLI interface.
* Add flags for the ICS conversion (exclude commemorations, etc.).
* Add documentation.
* Check to see whether we should use `append` vs `+=` for the list operations.
* Make code more efficient by running through the year only once.
* Add Holy Days of obligation for different regions.
* Add support for a one-event-per-day max.
* Support multiple years in a single `LiturgicalCalendar` object.
