"""Schedule optimization."""

# %%
from pulp import PULP_CBC_CMD, LpMaximize, LpProblem, LpStatus, LpVariable

from congress_optimizer.models import Event, Rating, events_overlap


def optimize_schedule(
    events_ratings: list[tuple[Event, Rating]],
) -> list[Event]:
    """
    Optimize the schedule of events based on ratings.

    Args:
        events_ratings: Tuples of events and matching ratings.
    Returns:
        Scheduled events.
    Raises:
        ValueError: If no optimal solution is found.
    """
    # unpack events and ratings
    events, ratings = zip(*events_ratings)

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
                constraint_name = (
                    f"overlap_{str(event_i.id).replace("-", "_")}"
                    f"_{str(event_j.id).replace("-", "_")}"
                )
                print(f"Adding constraint: {constraint_name}")
                prob += (lp_vars[i] + lp_vars[j] <= 1, constraint_name)

    print("\nProblem:")
    print(prob)

    # solve problem
    prob.solve(PULP_CBC_CMD(msg=False))

    # check if optimal solution was found
    optimal = LpStatus[prob.status] == "Optimal"
    if not optimal:
        raise ValueError("No optimal solution found.")

    print("solution:")
    for var in prob.variables():
        print(f"{var.name}: {var.varValue}")

    # extract scheduled events
    scheduled_event_names: list[str] = [
        var.name for var in prob.variables() if var.varValue == 1
    ]
    print(scheduled_event_names)
    scheduled_events: list[Event] = [
        event
        for event in events
        if event.slug.replace("-", "_") in scheduled_event_names
    ]
    print(scheduled_events)
    return scheduled_events
