"""Pytest tests for PawPal+ system."""

import pytest
from datetime import datetime, time, timedelta, date
from pawpal_system import Owner, Pet, Task, Scheduler, DailySchedule, ScheduledTask


class TestTask:
    """Tests for Task class."""
    
    def test_task_creation(self):
        """Test that a task can be created with basic attributes."""
        task = Task(
            title="Walk",
            duration_minutes=30,
            priority="high",
            frequency="daily"
        )
        assert task.title == "Walk"
        assert task.duration_minutes == 30
        assert task.priority == "high"
        assert task.frequency == "daily"
    
    def test_mark_complete(self):
        """Verify that calling mark_complete() changes task's status."""
        task = Task(
            title="Walk",
            duration_minutes=30,
            priority="high",
            frequency="daily"
        )
        assert task.is_completed is False
        task.mark_complete()
        assert task.is_completed is True
        assert task.last_completed is not None
    
    def test_daily_task_is_due(self):
        """Test that daily tasks are always due."""
        task = Task(
            title="Feeding",
            duration_minutes=10,
            priority="high",
            frequency="daily"
        )
        assert task.is_due_today() is True
    
    def test_priority_score(self):
        """Test that priority scores map correctly."""
        low = Task(title="Low", duration_minutes=10, priority="low", frequency="daily")
        medium = Task(title="Med", duration_minutes=10, priority="medium", frequency="daily")
        high = Task(title="High", duration_minutes=10, priority="high", frequency="daily")
        
        assert low.get_priority_score() == 1
        assert medium.get_priority_score() == 2
        assert high.get_priority_score() == 3


class TestPet:
    """Tests for Pet class."""
    
    def test_pet_creation(self):
        """Test that a pet can be created."""
        pet = Pet(name="Mochi", species="dog", age=3.0)
        assert pet.name == "Mochi"
        assert pet.species == "dog"
        assert pet.age == 3.0
    
    def test_add_task_to_pet(self):
        """Verify that adding a task to a Pet increases task count."""
        pet = Pet(name="Mochi", species="dog", age=3.0)
        assert len(pet.get_tasks()) == 0
        
        task = Task(title="Walk", duration_minutes=30, priority="high", frequency="daily")
        pet.add_task(task)
        
        assert len(pet.get_tasks()) == 1
        assert pet.get_tasks()[0] == task
    
    def test_get_daily_tasks(self):
        """Test that get_daily_tasks returns only due tasks."""
        pet = Pet(name="Mochi", species="dog", age=3.0)
        
        daily_task = Task(title="Walk", duration_minutes=30, priority="high", frequency="daily")
        weekly_task = Task(title="Bath", duration_minutes=60, priority="medium", frequency="weekly")
        weekly_task.last_completed = datetime.now()  # Mark as recently completed
        
        pet.add_task(daily_task)
        pet.add_task(weekly_task)
        
        daily_tasks = pet.get_daily_tasks()
        assert len(daily_tasks) >= 1
        assert daily_task in daily_tasks


class TestOwner:
    """Tests for Owner class."""
    
    def test_owner_creation(self):
        """Test that an owner can be created."""
        owner = Owner(name="Jordan", available_hours=4.0)
        assert owner.name == "Jordan"
        assert owner.available_hours == 4.0
    
    def test_add_pet_to_owner(self):
        """Verify that adding a pet increases the owner's pet count."""
        owner = Owner(name="Jordan", available_hours=4.0)
        assert len(owner.get_pets()) == 0
        
        pet = Pet(name="Mochi", species="dog", age=3.0)
        owner.add_pet(pet)
        
        assert len(owner.get_pets()) == 1
        assert owner.get_pets()[0] == pet
    
    def test_set_availability(self):
        """Test that availability can be updated."""
        owner = Owner(name="Jordan", available_hours=4.0)
        owner.set_availability(6.0)
        assert owner.available_hours == 6.0


class TestScheduler:
    """Tests for Scheduler class."""
    
    def test_scheduler_creation(self):
        """Test that a scheduler can be created."""
        owner = Owner(name="Jordan", available_hours=4.0)
        pet = Pet(name="Mochi", species="dog", age=3.0)
        owner.add_pet(pet)
        
        scheduler = Scheduler(owner, pet)
        assert scheduler.owner == owner
        assert scheduler.pet == pet
    
    def test_sort_tasks_by_priority(self):
        """Test that tasks are sorted by priority correctly."""
        owner = Owner(name="Jordan", available_hours=4.0)
        pet = Pet(name="Mochi", species="dog", age=3.0)
        
        low = Task(title="Low", duration_minutes=10, priority="low", frequency="daily")
        high = Task(title="High", duration_minutes=10, priority="high", frequency="daily")
        med = Task(title="Med", duration_minutes=10, priority="medium", frequency="daily")
        
        pet.add_task(low)
        pet.add_task(high)
        pet.add_task(med)
        
        scheduler = Scheduler(owner, pet)
        sorted_tasks = scheduler.sort_tasks_by_priority()
        
        # Should be ordered: high, medium, low
        assert sorted_tasks[0].priority == "high"
        assert sorted_tasks[1].priority == "medium"
        assert sorted_tasks[2].priority == "low"
    
    def test_generate_schedule(self):
        """Test that a schedule can be generated."""
        owner = Owner(name="Jordan", available_hours=2.0)
        pet = Pet(name="Mochi", species="dog", age=3.0)
        
        task = Task(title="Walk", duration_minutes=30, priority="high", frequency="daily")
        pet.add_task(task)
        
        scheduler = Scheduler(owner, pet)
        schedule = scheduler.generate_schedule(datetime.now())
        
        assert isinstance(schedule, DailySchedule)
        assert len(schedule.scheduled_tasks) > 0
    
    def test_check_time_conflicts(self):
        """Test that time conflicts are detected."""
        owner = Owner(name="Jordan", available_hours=0.5)  # 30 minutes available
        pet = Pet(name="Mochi", species="dog", age=3.0)
        
        # Add tasks that exceed available time
        task1 = Task(title="Walk 1", duration_minutes=20, priority="high", frequency="daily")
        task2 = Task(title="Walk 2", duration_minutes=15, priority="high", frequency="daily")
        
        pet.add_task(task1)
        pet.add_task(task2)
        
        scheduler = Scheduler(owner, pet)
        conflicts = scheduler.check_time_conflicts()
        
        # Should detect conflicts
        assert len(conflicts) > 0


class TestDailySchedule:
    """Tests for DailySchedule class."""
    
    def test_schedule_total_duration(self):
        """Test that total duration is calculated correctly."""
        schedule = DailySchedule(date=datetime.now())
        task = Task(title="Walk", duration_minutes=30, priority="high", frequency="daily")
        
        schedule.add_scheduled_task(task, time(8, 0))
        
        assert schedule.total_duration == 30
    
    def test_schedule_multiple_tasks(self):
        """Test adding multiple tasks to a schedule."""
        schedule = DailySchedule(date=datetime.now())
        
        task1 = Task(title="Walk", duration_minutes=30, priority="high", frequency="daily")
        task2 = Task(title="Feeding", duration_minutes=10, priority="high", frequency="daily")
        
        schedule.add_scheduled_task(task1, time(8, 0))
        schedule.add_scheduled_task(task2, time(8, 30))
        
        assert len(schedule.scheduled_tasks) == 2
        assert schedule.total_duration == 40
    
    def test_schedule_explanation(self):
        """Test that schedule explanation is generated."""
        schedule = DailySchedule(date=datetime.now())
        task = Task(title="Walk", duration_minutes=30, priority="high", frequency="daily")
        schedule.add_scheduled_task(task, time(8, 0))
        
        explanation = schedule.get_explanation()
        assert "Walk" in explanation
        assert "08:00" in explanation
    
    def test_schedule_feasibility(self):
        """Test that feasibility is determined correctly."""
        owner = Owner(name="Jordan", available_hours=2.0)
        schedule = DailySchedule(date=datetime.now(), owner=owner)
        
        # Add task that fits
        task = Task(title="Walk", duration_minutes=60, priority="high", frequency="daily")
        schedule.add_scheduled_task(task, time(8, 0))
        
        assert schedule.is_feasible() is True


class TestSchedulerAdvanced:
    """Tests for advanced Scheduler features: sorting, filtering, recurrence."""
    
    def test_sort_tasks_by_time(self):
        """Test that tasks are sorted by scheduled time."""
        owner = Owner(name="Jordan", available_hours=4.0)
        pet = Pet(name="Mochi", species="dog", age=3.0)
        
        # Add tasks out of chronological order
        task1 = Task(title="Morning", duration_minutes=10, priority="high", frequency="daily", scheduled_time="09:00")
        task2 = Task(title="Afternoon", duration_minutes=10, priority="high", frequency="daily", scheduled_time="15:00")
        task3 = Task(title="Evening", duration_minutes=10, priority="high", frequency="daily", scheduled_time="18:00")
        
        pet.add_task(task2)  # Add out of order
        pet.add_task(task1)
        pet.add_task(task3)
        
        scheduler = Scheduler(owner, pet)
        sorted_tasks = scheduler.sort_tasks_by_time()
        
        # Should be sorted: 09:00, 15:00, 18:00
        assert sorted_tasks[0].scheduled_time == "09:00"
        assert sorted_tasks[1].scheduled_time == "15:00"
        assert sorted_tasks[2].scheduled_time == "18:00"
    
    def test_filter_tasks_by_completion(self):
        """Test filtering tasks by completion status."""
        owner = Owner(name="Jordan", available_hours=4.0)
        pet = Pet(name="Mochi", species="dog", age=3.0)
        
        task1 = Task(title="Task1", duration_minutes=10, priority="high", frequency="daily")
        task2 = Task(title="Task2", duration_minutes=10, priority="high", frequency="daily")
        
        pet.add_task(task1)
        pet.add_task(task2)
        
        task1.mark_complete()  # Mark one complete
        
        scheduler = Scheduler(owner, pet)
        
        completed = scheduler.filter_tasks(completed=True)
        pending = scheduler.filter_tasks(completed=False)
        all_tasks = scheduler.filter_tasks()
        
        assert len(completed) == 1
        assert len(pending) == 1
        assert len(all_tasks) == 2
    
    def test_recurring_task_creation(self):
        """Test that marking a daily task complete creates next occurrence."""
        owner = Owner(name="Jordan", available_hours=4.0)
        pet = Pet(name="Mochi", species="dog", age=3.0)
        
        task = Task(title="Daily Walk", duration_minutes=30, priority="high", frequency="daily")
        pet.add_task(task)
        
        scheduler = Scheduler(owner, pet)
        
        # Initially 1 task
        assert len(pet.get_tasks()) == 1
        
        # Mark complete, should create next task
        next_task = scheduler.mark_task_complete(task)
        
        assert task.is_completed is True
        assert next_task is not None
        assert next_task.title == "Daily Walk"
        assert next_task.due_date == datetime.now().date() + timedelta(days=1)
        assert len(pet.get_tasks()) == 2  # Original + new
    
    def test_weekly_recurring_task(self):
        """Test weekly task recurrence."""
        owner = Owner(name="Jordan", available_hours=4.0)
        pet = Pet(name="Mochi", species="dog", age=3.0)
        
        task = Task(title="Weekly Bath", duration_minutes=60, priority="medium", frequency="weekly")
        pet.add_task(task)
        
        scheduler = Scheduler(owner, pet)
        
        next_task = scheduler.mark_task_complete(task)
        
        assert next_task.due_date == datetime.now().date() + timedelta(days=7)
    
    def test_no_recurrence_for_as_needed(self):
        """Test that as_needed tasks don't create recurrence."""
        owner = Owner(name="Jordan", available_hours=4.0)
        pet = Pet(name="Mochi", species="dog", age=3.0)
        
        task = Task(title="Vet Visit", duration_minutes=60, priority="high", frequency="as_needed")
        pet.add_task(task)
        
        scheduler = Scheduler(owner, pet)
        
        next_task = scheduler.mark_task_complete(task)
        
        assert next_task is None
        assert len(pet.get_tasks()) == 1  # No new task added


class TestOwnerAdvanced:
    """Tests for advanced Owner features."""
    
    def test_detect_time_conflicts(self):
        """Test conflict detection across pets."""
        owner = Owner(name="Jordan", available_hours=4.0)
        
        pet1 = Pet(name="Mochi", species="dog", age=3.0)
        pet2 = Pet(name="Luna", species="cat", age=2.0)
        
        task1 = Task(title="Walk", duration_minutes=30, priority="high", frequency="daily", scheduled_time="09:00")
        task2 = Task(title="Feeding", duration_minutes=10, priority="high", frequency="daily", scheduled_time="09:00")
        
        pet1.add_task(task1)
        pet2.add_task(task2)
        
        owner.add_pet(pet1)
        owner.add_pet(pet2)
        
        conflicts = owner.detect_all_time_conflicts()
        
        assert len(conflicts) == 1
        assert "Conflict at 09:00" in conflicts[0]
        assert "Walk" in conflicts[0] and "Feeding" in conflicts[0]
    
    def test_no_conflicts_when_times_differ(self):
        """Test no conflicts when scheduled times are different."""
        owner = Owner(name="Jordan", available_hours=4.0)
        
        pet = Pet(name="Mochi", species="dog", age=3.0)
        
        task1 = Task(title="Walk", duration_minutes=30, priority="high", frequency="daily", scheduled_time="09:00")
        task2 = Task(title="Feeding", duration_minutes=10, priority="high", frequency="daily", scheduled_time="10:00")
        
        pet.add_task(task1)
        pet.add_task(task2)
        
        owner.add_pet(pet)
        
        conflicts = owner.detect_all_time_conflicts()
        
        assert len(conflicts) == 0
    
    def test_filter_tasks_by_status(self):
        """Test filtering all tasks by completion status."""
        owner = Owner(name="Jordan", available_hours=4.0)
        
        pet = Pet(name="Mochi", species="dog", age=3.0)
        
        task1 = Task(title="Walk", duration_minutes=30, priority="high", frequency="daily")
        task2 = Task(title="Feeding", duration_minutes=10, priority="high", frequency="daily")
        
        pet.add_task(task1)
        pet.add_task(task2)
        owner.add_pet(pet)
        
        task1.mark_complete()
        
        completed = owner.get_tasks_by_status(completed=True)
        pending = owner.get_tasks_by_status(completed=False)
        
        assert len(completed) == 1
        assert len(pending) == 1


class TestEdgeCases:
    """Tests for edge cases and error conditions."""
    
    def test_pet_with_no_tasks(self):
        """Test scheduler with pet that has no tasks."""
        owner = Owner(name="Jordan", available_hours=4.0)
        pet = Pet(name="Mochi", species="dog", age=3.0)
        owner.add_pet(pet)
        
        scheduler = Scheduler(owner, pet)
        
        schedule = scheduler.generate_schedule(datetime.now())
        
        assert len(schedule.scheduled_tasks) == 0
        assert schedule.get_explanation() == "No tasks scheduled for today."
    
    def test_task_with_no_scheduled_time(self):
        """Test sorting when some tasks have no scheduled time."""
        owner = Owner(name="Jordan", available_hours=4.0)
        pet = Pet(name="Mochi", species="dog", age=3.0)
        
        task1 = Task(title="With Time", duration_minutes=10, priority="high", frequency="daily", scheduled_time="09:00")
        task2 = Task(title="No Time", duration_minutes=10, priority="high", frequency="daily")
        
        pet.add_task(task1)
        pet.add_task(task2)
        
        scheduler = Scheduler(owner, pet)
        sorted_tasks = scheduler.sort_tasks_by_time()
        
        # Task with time should come first
        assert sorted_tasks[0].scheduled_time == "09:00"
        assert sorted_tasks[1].scheduled_time is None
    
    def test_schedule_exceeds_available_time(self):
        """Test when total task time exceeds owner's availability."""
        owner = Owner(name="Jordan", available_hours=0.5)  # 30 minutes
        pet = Pet(name="Mochi", species="dog", age=3.0)
        
        task1 = Task(title="Long Walk", duration_minutes=20, priority="high", frequency="daily")
        task2 = Task(title="Another Task", duration_minutes=20, priority="high", frequency="daily")
        
        pet.add_task(task1)
        pet.add_task(task2)
        owner.add_pet(pet)
        
        scheduler = Scheduler(owner, pet)
        schedule = scheduler.generate_schedule(datetime.now())
        
        # Should only schedule what fits (20 min task fits in 30 min availability)
        assert len(schedule.scheduled_tasks) == 1  # Only first task fits
        assert schedule.total_duration == 20  # 20 minutes scheduled
        assert schedule.is_feasible()  # The scheduled tasks fit
        
        # But check that there are more tasks that couldn't be scheduled
        all_tasks = pet.get_daily_tasks()
        assert len(all_tasks) == 2  # Two tasks total
        assert len(schedule.scheduled_tasks) < len(all_tasks)  # Not all tasks scheduled
    
    def test_due_date_override(self):
        """Test that explicit due_date overrides frequency logic."""
        from datetime import date
        
        task = Task(
            title="Specific Date Task", 
            duration_minutes=10, 
            priority="high", 
            frequency="daily",
            due_date=date.today()
        )
        
        assert task.is_due_today() is True
        
        # Set due date to tomorrow
        tomorrow = date.today() + timedelta(days=1)
        task.due_date = tomorrow
        
        assert task.is_due_today() is False
