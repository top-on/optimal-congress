"""Schedule optimization."""

# %%
from pulp import PULP_CBC_CMD, LpMaximize, LpProblem, LpStatus, LpVariable

from congress_optimizer.models import Event, Rating, events_overlap


def optimize_schedule(
    events: list[Event],
    ratings: list[Rating],
) -> list[Event]:
    """
    Optimize the schedule of events based on ratings.

    Args:
        events: Events to be scheduled.
        ratings: Ratings for each event. Order and length must match provided events.
    Returns:
        Scheduled events.
    Raises:
        ValueError: If no optimal solution is found.
    """
    # sanity check
    assert len(events) == len(ratings)

    # define problem
    prob = LpProblem(name="Optimal Congress", sense=LpMaximize)

    # define decision variables (binary vector of same length as events)
    lp_vars = [
        LpVariable(
            name=event.slug,
            cat="Binary",
        )
        for event in events
    ]

    # objective function: maximize sum of ratings for scheduled events
    prob += sum(lp_var * rating.score for lp_var, rating in zip(lp_vars, ratings))

    # constraints: no overlapping events can be scheduled
    for i, event_i in enumerate(events):
        for j, event_j in enumerate(events):
            if i >= j:
                # avoid double counting, and comparing event to itself
                continue
            if events_overlap(event_i, event_j):
                prob += (
                    lp_vars[i] + lp_vars[j] <= 1,
                    f"overlap_{event_i.name}_{event_j.name}",
                )

    # solve problem
    prob.solve(PULP_CBC_CMD(msg=False))

    # check if optimal solution was found
    optimal = LpStatus[prob.status] == "Optimal"
    if not optimal:
        raise ValueError("No optimal solution found.")

    # extract scheduled events
    scheduled_event_names: list[str] = [
        var.name for var in prob.variables() if var.varValue == 1
    ]
    scheduled_events: list[Event] = [
        event for event in events if event.slug in scheduled_event_names
    ]
    return scheduled_events
