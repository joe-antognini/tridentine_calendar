* Add a check on the output from an end-to-end test.
* Use `feria_name` for ferias of Holy Week, feasts of Easter Week, and Pentecost Week.
* Monkey patch the JSON files to a test object during tests.
* Improve the tests.
    - Use mocks.
    - Add better CLI tests.
    - Add doctests.
* Add flags for the ICS conversion (exclude commemorations, etc.).
* Make code more efficient by running through the year only once.
* Add Holy Days of obligation for different regions.
* Add support for a one-event-per-day max.
