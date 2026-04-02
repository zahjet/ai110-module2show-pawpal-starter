"""PawPal+ System - Core logic for pet care scheduling."""

from dataclasses import dataclass, field
from datetime import datetime, date, time, timedelta
from typing import Optional


@dataclass
class Task:
    """Represents a pet care task (walk, feeding, medication, etc.)."""
    
    title: str
    duration_minutes: int
    priority: str  # "low", "medium", "high"
    frequency: str  # "daily", "weekly", "as_needed"
    last_completed: Optional[datetime] = None
    is_completed: bool = False
    scheduled_time: Optional[str] = None  # HH:MM
    due_date: Optional[date] = None
    
    def is_due_today(self) -> bool:
        """Check whether the task is due today."""
        today = datetime.now().date()
        if self.due_date is not None:
            return self.due_date == today
        if self.frequency == "daily":
            return True
        elif self.frequency == "weekly":
            if self.last_completed is None:
                return True
            days_since = (datetime.now() - self.last_completed).days
            return days_since >= 7
        elif self.frequency == "as_needed":
            return not self.is_completed
        return False
    
    def get_priority_score(self) -> int:
        """Return numeric priority score for sorting (higher = more important)."""
        priority_map = {"low": 1, "medium": 2, "high": 3}
        return priority_map.get(self.priority, 1)
    
    def mark_complete(self) -> Optional["Task"]:
        """Mark this task complete and return a new recurring task if needed."""
        self.is_completed = True
        self.last_completed = datetime.now()

        if self.frequency in ("daily", "weekly"):
            if self.due_date is not None:
                current_due = self.due_date
            else:
                current_due = datetime.now().date()

            delta = timedelta(days=1 if self.frequency == "daily" else 7)
            next_due = current_due + delta

            # Keep same scheduled_time and most attributes, new task created for next recurrence.
            return Task(
                title=self.title,
                duration_minutes=self.duration_minutes,
                priority=self.priority,
                frequency=self.frequency,
                scheduled_time=self.scheduled_time,
                due_date=next_due,
            )

        return None


@dataclass
class Pet:
    """Represents a pet in the owner's care."""
    
    name: str
    species: str  # "dog", "cat", "other"
    age: float
    health_notes: str = ""
    tasks: list[Task] = field(default_factory=list)
    
    def add_task(self, task: Task) -> None:
        """Add a care task for this pet."""
        self.tasks.append(task)
    
    def get_tasks(self) -> list[Task]:
        """Get all tasks for this pet."""
        return self.tasks
    
    def get_daily_tasks(self) -> list[Task]:
        """Get only tasks that are due today."""
        return [task for task in self.tasks if task.is_due_today()]


@dataclass
class Owner:
    """Represents the pet owner and their preferences."""
    
    name: str
    available_hours: float = 8.0
    preferences: list[str] = field(default_factory=list)
    pets: list[Pet] = field(default_factory=list)
    
    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner's collection."""
        self.pets.append(pet)
    
    def get_pets(self) -> list[Pet]:
        """Get all pets owned by this owner."""
        return self.pets
    
    def set_availability(self, hours: float) -> None:
        """Set the owner's available time for pet care (in hours)."""
        self.available_hours = hours
    
    def get_all_tasks(self) -> list[Task]:
        """Get all tasks from all pets."""
        all_tasks = []
        for pet in self.pets:
            all_tasks.extend(pet.get_tasks())
        return all_tasks

    def get_tasks_by_status(self, completed: bool) -> list[Task]:
        """Filter all tasks by completion status."""
        return [task for task in self.get_all_tasks() if task.is_completed == completed]
    
    def get_today_tasks(self) -> list[Task]:
        """Get all tasks due today from all pets."""
        all_tasks = []
        for pet in self.pets:
            all_tasks.extend(pet.get_daily_tasks())
        return all_tasks

    def detect_all_time_conflicts(self) -> list[str]:
        """Detect scheduling conflicts across all pets (same due time)."""
        conflicts = []
        tasks_with_time = [t for t in self.get_all_tasks() if t.scheduled_time]
        time_map = {}

        for task in tasks_with_time:
            time_map.setdefault(task.scheduled_time, []).append(task)

        for scheduled_time, grouped in time_map.items():
            if len(grouped) > 1:
                titles = ", ".join([t.title for t in grouped])
                conflicts.append(f"Conflict at {scheduled_time}: {titles}")

        return conflicts


@dataclass
class ScheduledTask:
    """Represents a task scheduled for a specific time in the day."""
    
    task: Task
    start_time: time
    end_time: time
    
    def get_duration(self) -> int:
        """Get duration of this scheduled task in minutes."""
        start_dt = datetime.combine(datetime.now().date(), self.start_time)
        end_dt = datetime.combine(datetime.now().date(), self.end_time)
        duration = (end_dt - start_dt).total_seconds() / 60
        return int(duration)


@dataclass
class DailySchedule:
    """Represents the optimized schedule for one day."""
    
    date: datetime
    scheduled_tasks: list[ScheduledTask] = field(default_factory=list)
    owner: Optional['Owner'] = None
    
    @property
    def total_duration(self) -> int:
        """Get total time allocated for all scheduled tasks (in minutes)."""
        return sum(st.get_duration() for st in self.scheduled_tasks)
    
    def add_scheduled_task(self, task: Task, start_time: time) -> None:
        """Add a task to the schedule at a specific start time."""
        end_minutes = start_time.hour * 60 + start_time.minute + task.duration_minutes
        end_hour = end_minutes // 60
        end_minute = end_minutes % 60
        end_time = time(hour=end_hour, minute=end_minute)
        scheduled = ScheduledTask(task=task, start_time=start_time, end_time=end_time)
        self.scheduled_tasks.append(scheduled)
    
    def get_explanation(self) -> str:
        """Return a human-readable explanation of why tasks were scheduled this way."""
        if not self.scheduled_tasks:
            return "No tasks scheduled for today."
        
        explanation = f"Daily Schedule for {self.date.strftime('%A, %B %d')}:\n\n"
        for st in self.scheduled_tasks:
            explanation += f"• {st.start_time.strftime('%I:%M %p')} - {st.task.title} ({st.task.duration_minutes} min, Priority: {st.task.priority})\n"
        
        total_mins = self.total_duration
        hours = total_mins // 60
        mins = total_mins % 60
        explanation += f"\nTotal time: {hours}h {mins}m"
        
        if self.owner and self.owner.available_hours * 60 < total_mins:
            explanation += f" ⚠️ (Exceeds available time of {self.owner.available_hours}h)"
        
        return explanation
    
    def is_feasible(self) -> bool:
        """Check if schedule fits within owner's available time and has no conflicts."""
        if not self.owner:
            return True
        
        available_minutes = self.owner.available_hours * 60
        
        # Check if total time exceeds availability
        if self.total_duration > available_minutes:
            return False
        
        # Check for time conflicts (overlapping tasks)
        for i, st1 in enumerate(self.scheduled_tasks):
            for st2 in self.scheduled_tasks[i + 1:]:
                # Check if st1 overlaps with st2
                if st1.start_time < st2.end_time and st2.start_time < st1.end_time:
                    return False
        
        return True


class Scheduler:
    """Orchestrates the scheduling logic for a pet's daily tasks."""
    
    def __init__(self, owner: Owner, pet: Pet):
        """Initialize scheduler with an owner and a pet."""
        self.owner = owner
        self.pet = pet
        self.tasks = pet.tasks
    
    def generate_schedule(self, date: datetime) -> DailySchedule:
        """Generate an optimized daily schedule based on constraints."""
        schedule = DailySchedule(date=date, owner=self.owner)
        
        # Get tasks due today and sort by priority
        due_tasks = self.pet.get_daily_tasks()
        sorted_tasks = self.sort_tasks_by_priority()
        sorted_tasks = [t for t in sorted_tasks if t in due_tasks]
        
        # Schedule tasks starting at 8:00 AM
        current_time = time(8, 0)
        available_minutes = self.owner.available_hours * 60
        
        for task in sorted_tasks:
            # Calculate current time in minutes since midnight
            current_minutes = current_time.hour * 60 + current_time.minute
            
            # Check if task fits in available time (starting at 8 AM)
            if schedule.total_duration + task.duration_minutes <= available_minutes:
                schedule.add_scheduled_task(task, current_time)
                # Update current time
                new_minutes = current_minutes + task.duration_minutes
                current_time = time(hour=new_minutes // 60, minute=new_minutes % 60)
        
        return schedule
    
    def sort_tasks_by_priority(self) -> list[Task]:
        """Sort tasks by priority (highest first)."""
        return sorted(self.pet.get_daily_tasks(), key=lambda t: -t.get_priority_score())

    def sort_tasks_by_time(self) -> list[Task]:
        """Sort tasks by scheduled time if set, otherwise send to end."""
        return sorted(
            self.pet.get_tasks(),
            key=lambda t: t.scheduled_time or "23:59"
        )

    def filter_tasks(self, completed: Optional[bool] = None) -> list[Task]:
        """Filter tasks by completion status."""
        tasks = self.pet.get_tasks()
        if completed is None:
            return tasks
        return [task for task in tasks if task.is_completed == completed]
    
    def mark_task_complete(self, task: Task) -> Optional[Task]:
        """Mark a task complete and register next recurrence if needed."""
        next_task = task.mark_complete()
        if next_task:
            self.pet.add_task(next_task)
        return next_task

    def check_time_conflicts(self) -> list[str]:
        """Identify tasks that cannot fit within available time."""
        conflicts = []
        total_time_needed = sum(t.duration_minutes for t in self.pet.get_daily_tasks())
        available_minutes = self.owner.available_hours * 60
        
        if total_time_needed > available_minutes:
            excess = total_time_needed - available_minutes
            conflicts.append(f"Total tasks require {total_time_needed} minutes but only {available_minutes} available. Missing {excess} minutes.")
            
            # Identify lower-priority tasks that don't fit
            sorted_tasks = self.sort_tasks_by_priority()
            accumulated = 0
            for task in sorted_tasks:
                accumulated += task.duration_minutes
                if accumulated > available_minutes:
                    conflicts.append(f"  - '{task.title}' (priority: {task.priority}) cannot fit in schedule")
        
        return conflicts
