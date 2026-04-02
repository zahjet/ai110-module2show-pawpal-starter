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
        frequency="daily"
    )
    task2 = Task(
        title="Afternoon walk",
        duration_minutes=20,
        priority="high",
        frequency="daily"
    )
    task3 = Task(
        title="Feeding",
        duration_minutes=10,
        priority="high",
        frequency="daily"
    )
    task4 = Task(
        title="Playtime",
        duration_minutes=15,
        priority="medium",
        frequency="daily"
    )
    
    mochi.add_task(task1)
    mochi.add_task(task2)
    mochi.add_task(task3)
    mochi.add_task(task4)
    
    print(f"✓ Added {len(mochi.get_tasks())} tasks to {mochi.name}")
    
    # Tasks for Luna
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
