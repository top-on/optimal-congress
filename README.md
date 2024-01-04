# Optimal Congress

Command Line Interface to find an optimal, personal schedule for the [37c3 congress](https://events.ccc.de/congress/2023/infos/).

## Project status

⚠️ Development for this project is currently on hold. It can quickly be adapted for [future CCC events](https://events.ccc.de/). ⚠️

## Optimization logic

The optimization relies on a simple 2-fold logic:

1. Find a personal schedule that maximizes the sum of 'rating scores' assigned to scheduled events.
2. The schedule must be feasible, i.e. the times of scheduled events must not overlap.

## Installation

```bash
pip install optimal-congress
```

## Available commands

`optimal-congress` provides the following commands:

```
$ optimal-congress -h

 Usage: optimal-congress [OPTIONS] COMMAND [ARGS]...

 Optimize your personal schedule for the 37c3.

╭─ Options ────────────────────────────────────────────────────────────────────────────╮
│ --verbose  -v        Include debug messages in output.                               │
│ --help     -h        Show this message and exit.                                     │
╰──────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ───────────────────────────────────────────────────────────────────────────╮
│ dump                   Export all latest ratings to CSV, for bulk editing.           │
│ fetch                  Fetch events and rooms from API, and update local cache.      │
│ load                   Bulk import ratings from CSV.                                 │
│ next                   List next upcoming events, filtered by minimum rating.        │
│ optimize               Optimize the schedule based on ratings.                       │
│ rate                   Interactively rate those events that have not been rated yet. │
│ ratings                List all latest ratings.                                      │
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

Software testing uses `pytest`, relying upon `poetry` and `tox`.<br>
To run all tests, across multiple python versions:

```bash
poetry run tox
```

## Roadmap

- output more/all information with associated events (see [feature request](https://github.com/top-on/optimal-congress/issues/3) and [example](https://www.willmcgugan.com/blog/tech/post/real-working-hyperlinks-in-the-terminal-with-rich/) for more compact hyperlinks with `rich`)
- change rating scheme, to minimize effort and maximize flexibility (see [feature request](https://github.com/top-on/optimal-congress/issues/4)),<br>
e.g. by first marking favorites, and only requiring relative ratings for conflicting favorites
- test export of schedule to iOS app via QR code (same format as halfnarp)
