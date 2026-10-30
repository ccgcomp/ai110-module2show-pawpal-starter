# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

Run the demo with `python main.py`. It builds one owner with two pets and shows sorting, conflict warnings, recurring tasks and filtering (dates reflect the day it was run):

```

Today's Schedule for Cody (sorted by time)
----------------------------------------
[ ] 2026-10-30 07:30  Buddy (dog): Morning walk [daily]
[ ] 2026-10-30 07:30  Whiskers (cat): Play time [once]
[ ] 2026-10-30 08:00  Whiskers (cat): Breakfast [daily]
[ ] 2026-10-30 12:00  Buddy (dog): Flea medication [weekly]
[ ] 2026-10-30 15:00  Whiskers (cat): Vet appointment [once]
[ ] 2026-10-30 18:00  Buddy (dog): Evening feeding [daily]
[ ] 2026-10-30 18:00  Buddy (dog): Brush teeth [daily]
[ ] 2026-10-30 19:30  Whiskers (cat): Clean litter box [daily]

Conflict warnings
----------------------------------------
WARNING: Conflict on 2026-10-30 at 07:30: Buddy - Morning walk, Whiskers - Play time
WARNING: Conflict on 2026-10-30 at 18:00: Buddy - Evening feeding, Buddy - Brush teeth

Completed 'Morning walk'. Next one created for 2026-10-31.

Filter: Whiskers' tasks
----------------------------------------
[ ] 2026-10-30 07:30  Whiskers (cat): Play time [once]
[ ] 2026-10-30 08:00  Whiskers (cat): Breakfast [daily]
[ ] 2026-10-30 15:00  Whiskers (cat): Vet appointment [once]
[ ] 2026-10-30 19:30  Whiskers (cat): Clean litter box [daily]

Filter: completed tasks
----------------------------------------
[x] 2026-10-30 07:30  Buddy (dog): Morning walk [daily]

Filter: Buddy's unfinished tasks
----------------------------------------
[ ] 2026-10-30 12:00  Buddy (dog): Flea medication [weekly]
[ ] 2026-10-30 18:00  Buddy (dog): Evening feeding [daily]
[ ] 2026-10-30 18:00  Buddy (dog): Brush teeth [daily]
[ ] 2026-10-31 07:30  Buddy (dog): Morning walk [daily]
```

## 🧪 Testing PawPal+

```bash
# Run the full test suite:
pytest

# Run with coverage:
pytest --cov
```

Sample test output:

```
# Paste your pytest output here
```

## 📐 Smarter Scheduling

All of these live on the `Scheduler` class in `pawpal_system.py` and work across every pet the owner has.

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | `Scheduler.sort_by_time()`, `get_todays_schedule()` | `sorted()` with a lambda key on `(due_date, "HH:MM")`; the schedule only includes tasks due today |
| Filtering | `Scheduler.filter_tasks(completed, pet_name)` | Filter by completion status, pet name (case-insensitive), or both |
| Conflict handling | `Scheduler.find_conflicts()` | Returns warning messages for unfinished tasks sharing a date and exact time, same pet or different pets. It never raises |
| Recurring tasks | `Scheduler.complete_task()` | Completing a `daily` task adds a copy due tomorrow, `weekly` adds one `timedelta(days=7)` later, `once` adds nothing |

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
