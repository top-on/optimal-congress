# Optimal Congress

CLI to find an optimal, personal schedule for the [37c3 congress](https://events.ccc.de/congress/2023/infos/).

## Optimization logic

The optimization relies on a simple 2-fold logic:

1. Find a personal schedule that maximizes the sum of 'rating scores' assigned to scheduled events.
2. The schedule must be feasible, i.e. the times of scheduled events must not overlap.

## Installation

```bash
pip install optimal-congress
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

- new command 'next', for next N events. with 'minimum rating' as filter argument
- test export of schedule to iOS app via QR code
