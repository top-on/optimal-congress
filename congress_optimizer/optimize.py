"""Schedule optimization."""

# %%
from pulp import PULP_CBC_CMD, LpMaximize, LpProblem, LpStatus, LpVariable

from congress_optimizer.models import Event, Rating, events_overlap


def optimize_schedule(events: list[Event], ratings: list[Rating]) -> list[Event]:
    assert len(events) == len(ratings)

    prob = LpProblem(name="Optimal Congress", sense=LpMaximize)

    # define problem variables
    lp_vars = [
        LpVariable(
            name=event.slug,
            cat="Binary",
        )
        for event in events
    ]

    # define objective function
    prob += sum(lp_var * rating.score for lp_var, rating in zip(lp_vars, ratings))

    # add constraint that checks for overlapping events
    for i, event_i in enumerate(events):
        for j, event_j in enumerate(events):
            if i >= j:
                # skip elements below diagonal
                continue
            if events_overlap(event_i, event_j):
                prob += (
                    lp_vars[i] + lp_vars[j] <= 1,
                    f"overlap_{event_i.name}_{event_j.name}",
                )

    # solve problem
    prob.solve(PULP_CBC_CMD(msg=False))
    optimal = LpStatus[prob.status] == "Optimal"
    if not optimal:
        raise ValueError("No optimal solution found.")

    scheduled_event_names: list[str] = [
        var.name for var in prob.variables() if var.varValue == 1
    ]

    scheduled_events: list[Event] = [
        event for event in events if event.slug in scheduled_event_names
    ]
    return scheduled_events
