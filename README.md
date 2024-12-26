# Optimal Congress

[![Python](https://img.shields.io/pypi/pyversions/optimal-congress.svg)](https://badge.fury.io/py/optimal-congress)
[![PyPI](https://badge.fury.io/py/optimal-congress.svg)](https://badge.fury.io/py/optimal-congress)
[![Pytest](https://github.com/top-on/optimal-congress/actions/workflows/pytest.yml/badge.svg)](https://github.com/top-on/optimal-congress/actions/workflows/pytest.yml)
[![pre-commit](https://github.com/top-on/optimal-congress/actions/workflows/pre-commit.yml/badge.svg)](https://github.com/top-on/optimal-congress/actions/workflows/pre-commit.yml)

Command Line Interface to find an optimal, personal schedule for the [38c3 congress](https://events.ccc.de/congress/2024/infos/).

## Optimization logic

The optimization relies on a simple 2-fold logic:

1. Find a personal schedule that maximizes the sum of 'rating scores' assigned to scheduled events.
2. The schedule must be feasible, i.e. the times of scheduled events must not overlap.

## Installation

```bash
pip install optimal-congress
```

With nix, you can run this application directly (contact [kaesaecracker](https://github.com/kaesaecracker) if this does not work):
```bash
nix run github:top-on/optimal-congress
```

## Available commands

`optimal-congress` provides the following commands:

```
$ optimal-congress -h

 Usage: optimal-congress [OPTIONS] COMMAND [ARGS]...

 Optimize your personal schedule for the 38c3.

╭─ Options ────────────────────────────────────────────────────────────────────────────╮
│ --verbose  -v        Include debug messages in output.                               │
│ --help     -h        Show this message and exit.                                     │
╰──────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ───────────────────────────────────────────────────────────────────────────╮
│ fetch                  Fetch events and rooms from API, and update local cache.      │
│ rate                   Interactively rate those events that have not been rated yet. │
│ ratings                List all latest ratings.                                      │
│ optimize               Optimize the schedule based on ratings.                       │
│ next                   List next upcoming events, filtered by minimum rating.        │
│ dump                   Export all latest ratings to CSV, for bulk editing.           │
│ load                   Bulk import ratings from CSV.                                 │
│ version                Print version and exit.                                       │
╰──────────────────────────────────────────────────────────────────────────────────────╯
```

## Example Workflow

1. Fetch events and rooms from congress API:

```
$ optimal-congress fetch

Fetching events and rooms from API...
Fetched 49 events and 58 rooms from API.

Comparing API with cache...
Found 0 new events, and 0 removed events.

Updating cache...
Done.
```

2. Interactively rate events, if not already rated:

```
$ optimal-congress rate

Unrated event (1/65):

2023-12-28 20:15 - 20:55

Lützerath Lebt! Einblicke in den Widerstand

You can't evict a movement! Der Energiekonzern RWE wird noch Jahre brauchen, die Kohle unter Lützi abzubaggern: Der Kampf gegen die Kohle und für Klimagerechtigkeit geht weiter!

https://events.ccc.de/congress/2023/hub/en/event/lutzerath_lebt_einblicke_in_den_widerstand

Rate from 0 to 10 (Enter to exit):
```

3. Review you current ratings:

```
$ optimal-congress ratings

loading events and ratings from cache...

Latest ratings:
- Rating: 8.0 - Amateurfunk als Hilfe in Not- und Katastrophenfäll..https://events.ccc.de/congress/2023/hub/en/event/amateurfunk-als-hilfe-in-not-und-katastrophenfalle
- Rating: 8.0 - InfraNodus: Reveal Non-Obvious and Find the Gaps w..https://events.ccc.de/congress/2023/hub/en/event/infranodus-reveal-non-obvious-and-find-the-gaps-wi
```

4. Optimize your personal schedule:

```
$ optimal-congress optimize

loading events, ratings, and rooms from cache...

Scheduled events:
- Wed 27 10:30-11:00 Saal 1..........37C3: Feierliche Eröffnung................https://events.ccc.de/congress/2023/hub/en/event/37c3_feierliche_eroffnung
- Wed 27 11:00-11:40 Saal Granville..The Trouble with Green Electricity Certi..https://events.ccc.de/congress/2023/hub/en/event/the_trouble_with_green_electricity_certificates
...
```

## Testing

Testing of this library relies on `pytest`.
Tests are split into unit tests (`tests/unit`) and integration tests (`tests/integration`).

To run all tests, use: `poetry run pytest`

Note that the unit tests are executed automatically in the CI pipeline (see `.github/workflows/pytest.yml`).

## Long-term Roadmap

- add latest UI examples to README
- use rich table for `next` view
- output more/all information with associated events (see [feature request](https://github.com/top-on/optimal-congress/issues/3) and [example](https://www.willmcgugan.com/blog/tech/post/real-working-hyperlinks-in-the-terminal-with-rich/) for more compact hyperlinks with `rich`)
- change rating scheme, to minimize effort and maximize flexibility (see [feature request](https://github.com/top-on/optimal-congress/issues/4)),<br>
e.g. by first marking favorites, and only requiring relative ratings for conflicting favorites
- test export of schedule to iOS app via QR code (same format as halfnarp)
