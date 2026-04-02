"""Pytest tests for PawPal+ system."""

import pytest
from datetime import datetime, time
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


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
