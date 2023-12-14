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

1. Fetch events and room from congress API:

```bash
$ optimal-congress fetch

Fetching events and rooms from API...

Found 47 events and 57 rooms at API.
Saving events and rooms to cache...
```

2. Interactively rate events, if not already rated:

```bash
$ optimal-congress rate

loading events and ratings from cache...

Found 47 events and 47 ratings.
No new events to rate. Exiting.
```

3. Optimize schedule.

```bash
$ optimal-congress optimize

loading events and ratings from cache...

Scheduled events:
- Wed 27 10:30-11:00: 37C3: Feierliche Eröffnung...........................https://events.ccc.de/congress/2023/hub/en/event/37c3_feierliche_eroffnung
- Wed 27 13:00-15:30: POTA – Parks on the Air [Day 1]......................https://events.ccc.de/congress/2023/hub/en/event/pota-parks-on-the-air
...
```

## Roadmap

- when fetching new events and rooms, report on what's new and what's deleted

- dump all latest ratings to CSV
- load ratings from CSV
