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

## Smarter Scheduling

The current PawPal+ implementation now includes:

- Task sorting by priority and scheduled time (HH:MM).  
- Task filtering by completion status (completed / pending).  
- Recurring tasks: completing a daily or weekly task generates next occurrence automatically.  
- Basic conflict detection by exact scheduled-time matches across pets/tasks.

## Features

PawPal+ includes these smart scheduling algorithms:

- **Priority-Based Scheduling**: Tasks sorted by high → medium → low priority
- **Time-Based Sorting**: Tasks organized chronologically by scheduled time (HH:MM)
- **Completion Filtering**: Separate views for completed vs pending tasks
- **Recurring Tasks**: Daily/weekly tasks auto-generate next occurrence when completed
- **Conflict Detection**: Identifies exact-time conflicts across all pets/tasks
- **Feasibility Checking**: Ensures schedules fit within owner availability
- **Multi-Pet Support**: Manages care schedules for multiple pets simultaneously

## Testing PawPal+

Run the automated test suite to verify system behavior:

```bash
python -m pytest test_pawpal.py -v
```

The test suite covers:
- **Core functionality**: Task creation, completion, priority scoring
- **Pet and Owner management**: Adding pets/tasks, availability settings
- **Scheduling logic**: Priority sorting, time-based scheduling, feasibility checks
- **Advanced features**: Time sorting, completion filtering, recurring tasks, conflict detection
- **Edge cases**: Empty pets, time conflicts, availability limits, due date overrides

**Confidence Level**: ⭐⭐⭐⭐⭐ (5/5 stars) - All 30 tests pass, covering happy paths and edge cases. The system reliably handles task scheduling, recurrence, and conflict detection.

## 📸 Demo

<a href="/course_images/ai110/pawpal_demo.png" target="_blank"><img src='/course_images/ai110/pawpal_demo.png' title='PawPal+ App Demo' width='' alt='PawPal+ App Demo' class='center-block' /></a>

