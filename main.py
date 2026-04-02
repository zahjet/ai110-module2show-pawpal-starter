"""PawPal+ Demo Script - Test the backend system in the terminal."""

from datetime import datetime, time
from pawpal_system import Owner, Pet, Task, Scheduler


def print_separator(title: str = ""):
    """Print a formatted separator."""
    if title:
        print(f"\n{'=' * 60}")
        print(f"  {title}")
        print(f"{'=' * 60}\n")
    else:
        print(f"\n{'-' * 60}\n")


def main():
    """Run the demo."""
    
    # Step 1: Create an owner
    print_separator("CREATING OWNER AND PETS")
    owner = Owner(name="Jordan", available_hours=4)
    print(f"✓ Created owner: {owner.name}")
    print(f"  Available time: {owner.available_hours} hours/day")
    
    # Step 2: Create pets
    mochi = Pet(name="Mochi", species="dog", age=3.5, health_notes="Energetic, loves walks")
    luna = Pet(name="Luna", species="cat", age=2.0, health_notes="Indoor, calm")
    
    owner.add_pet(mochi)
    owner.add_pet(luna)
    
    print(f"\n✓ Created pet: {mochi.name} ({mochi.species})")
    print(f"✓ Created pet: {luna.name} ({luna.species})")
    
    # Step 3: Add tasks for Mochi
    print_separator("ADDING TASKS")
    
    task1 = Task(
        title="Morning walk",
        duration_minutes=30,
        priority="high",
        frequency="daily",
        scheduled_time="09:00"
    )
    task2 = Task(
        title="Afternoon walk",
        duration_minutes=20,
        priority="high",
        frequency="daily",
        scheduled_time="15:00"
    )
    task3 = Task(
        title="Feeding",
        duration_minutes=10,
        priority="high",
        frequency="daily",
        scheduled_time="08:00"
    )
    task4 = Task(
        title="Playtime",
        duration_minutes=15,
        priority="medium",
        frequency="daily",
        scheduled_time="12:00"
    )

    # Add tasks out-of-order to test sort_by_time
    mochi.add_task(task2)  # afternoon first (out of chronological order)
    mochi.add_task(task4)
    mochi.add_task(task1)
    mochi.add_task(task3)
    task5 = Task(
        title="Feeding (Luna)",
        duration_minutes=5,
        priority="high",
        frequency="daily"
    )
    task6 = Task(
        title="Litter box refresh",
        duration_minutes=5,
        priority="medium",
        frequency="daily"
    )
    
    luna.add_task(task5)
    luna.add_task(task6)
    
    print(f"✓ Added {len(luna.get_tasks())} tasks to {luna.name}")
    
    # Step 4: Generate Mochi's schedule
    print_separator("SCHEDULING MOCHI'S DAY")
    
    scheduler_mochi = Scheduler(owner, mochi)
    
    print(f"Daily tasks for {mochi.name}:")
    for task in scheduler_mochi.sort_tasks_by_priority():
        print(f"  • {task.title} ({task.duration_minutes} min, priority: {task.priority})")
    
    schedule = scheduler_mochi.generate_schedule(datetime.now())
    print()
    print(schedule.get_explanation())
    print(f"\nSchedule feasible: {schedule.is_feasible()}")
    
    # Check for conflicts
    conflicts = scheduler_mochi.check_time_conflicts()
    if conflicts:
        print("\n⚠️  Time Conflicts Detected:")
        for conflict in conflicts:
            print(f"  {conflict}")
    else:
        print("\n✓ No time conflicts")
    
    # Step 4.5: Task sorting + filtering + recurrence demo
    print_separator("TASK SORT/FILTER/RECURRING DEMO")

    print("Current Mochi tasks in insertion order:")
    for t in mochi.get_tasks():
        print(f"  • {t.scheduled_time or 'N/A'}  {t.title} (completed={t.is_completed})")

    sorted_by_time = scheduler_mochi.sort_tasks_by_time()
    print("\nMochi tasks sorted by scheduled time:")
    for t in sorted_by_time:
        print(f"  • {t.scheduled_time or 'N/A'}  {t.title}")

    print("\nUnfinished tasks only:")
    unfinished = scheduler_mochi.filter_tasks(completed=False)
    for t in unfinished:
        print(f"  • {t.title} (is_completed={t.is_completed})")

    print("\nMarking 'Morning walk' complete...")
    new_task = scheduler_mochi.mark_task_complete(task1)
    print(f"  - Morning walk completed? {task1.is_completed}")
    if new_task:
        print(f"  - Recurring task added with due_date {new_task.due_date}")

    print("\nNow tasks after recurrence:")
    for t in mochi.get_tasks():
        print(f"  • {t.title} due {t.due_date or datetime.now().date()} completed={t.is_completed}")

    # Conflict test: add another task at same scheduled time
    conflict_task = Task(
        title="Vet call",
        duration_minutes=15,
        priority="medium",
        frequency="as_needed",
        scheduled_time="08:00"
    )
    mochi.add_task(conflict_task)
    owner_conflicts = owner.detect_all_time_conflicts()
    if owner_conflicts:
        print("\nDetected conflicts across pets/tasks:")
        for c in owner_conflicts:
            print(f"  ⚠️ {c}")
    else:
        print("\nNo conflicts detected.")

    # Step 5: Generate Luna's schedule
    print_separator("SCHEDULING LUNA'S DAY")
    
    scheduler_luna = Scheduler(owner, luna)
    
    print(f"Daily tasks for {luna.name}:")
    for task in scheduler_luna.sort_tasks_by_priority():
        print(f"  • {task.title} ({task.duration_minutes} min, priority: {task.priority})")
    
    schedule_luna = scheduler_luna.generate_schedule(datetime.now())
    print()
    print(schedule_luna.get_explanation())
    print(f"\nSchedule feasible: {schedule_luna.is_feasible()}")
    
    # Step 6: Show owner's overview
    print_separator("OWNER'S OVERVIEW")
    
    print(f"Owner: {owner.name}")
    print(f"Pets: {', '.join([p.name for p in owner.get_pets()])}")
    print(f"Total tasks today: {len(owner.get_today_tasks())}")
    print(f"Available time: {owner.available_hours} hours")
    
    print_separator("DEMO COMPLETE")
    print("✓ All classes working correctly!")


if __name__ == "__main__":
    main()
