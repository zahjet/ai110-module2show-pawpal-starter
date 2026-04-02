# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

add a pet, schedule a walk, see today's tasks

**UML Design:**

The system uses 6 main classes:

1. **Owner** - Stores owner info (name, availability) and manages pets. Responsible for setting time constraints that affect scheduling.

2. **Pet** - Represents a pet with attributes (name, species, age, health notes). Manages a list of care tasks and retrieves daily-due tasks.

3. **Task** - Represents an individual care activity (duration, priority level, frequency). Includes logic to determine if it's due today and compute priority scores for sorting.

4. **Scheduler** - The core orchestrator that takes an Owner and Pet, then generates optimized daily schedules. Sorts tasks by priority, detects time conflicts, and applies scheduling constraints.

5. **DailySchedule** - Represents the final output: a list of tasks scheduled for specific times with explanations of why each task was placed when it was.

6. **ScheduledTask** - Represents a Task placed at a specific time slot within the day, tracking start/end times.

**Key Relationships:**
- Owner has many Pets (1:many)
- Pet has many Tasks (1:many)  
- Scheduler considers both Owner and Pet to generate a DailySchedule
- DailySchedule contains ScheduledTask entries

**b. Design changes**

Yes, the design changed during implementation for practical reasons:

1. **Added `is_completed` status and `mark_complete()` to Task** - The initial design tracked `last_completed` but didn't have an explicit completion flag. During implementation, I added an `is_completed` boolean to track whether a task in the current day has been done, separate from the frequency-based logic. This was necessary for the "as_needed" frequency type.

2. **Added helper methods to Owner** - I added `get_all_tasks()` and `get_today_tasks()` methods that aggregate tasks across all pets. This wasn't in the initial skeleton but proved essential for the UI layer to easily access all pet tasks without manual iteration.

3. **Made `owner` a reference in DailySchedule** - The initial design showed DailySchedule as independent, but during implementation I made the `owner` field accessible in DailySchedule. This allows the schedule to check feasibility against the owner's availability constraint directly, rather than requiring the Scheduler to do it.

Why these changes? They emerged from actual usage in main.py and tests—the design evolved toward practical convenience without changing the core architecture. The system still follows the original 1:many Owner->Pet->Task hierarchy.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?

The scheduler considers: owner availability (total hours per day), task priority (high/medium/low), task duration, scheduled times, and frequency (daily/weekly/as_needed). It also checks for time conflicts and ensures schedules are feasible within the owner's time limits.

- How did you decide which constraints mattered most?

I prioritized owner availability first (hard constraint - schedules cannot exceed available time), then task priority (high-priority tasks scheduled first), then scheduled times (chronological ordering). Duration affects feasibility but is secondary to priority. Frequency determines which tasks are included but doesn't affect ordering within daily tasks.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.

The scheduler currently uses exact scheduled-time string matching for conflict detection (like two tasks both at "08:00") rather than detecting partially overlapping intervals (like 08:00-08:30 and 08:15-08:45). This is simpler and lightweight for initial MVP behavior, but it can miss real conflicts where tasks overlap without exact start-time equality.

- Why is that tradeoff reasonable for this scenario?

For a pet care assistant in early stages, precise interval math adds complexity and edge cases; using exact-time rules provides clear, predictable warnings with minimal code. As usage grows, the app can evolve into full interval overlap checking.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?

I used VS Code Copilot extensively throughout all phases: for initial UML diagram generation, class skeleton creation, implementing complex algorithms (sorting, filtering, recurrence), generating comprehensive test suites, debugging failing tests, and documenting features. I also used separate chat sessions for different phases to stay organized.

- What kinds of prompts or questions were most helpful?

The most helpful prompts were specific and contextual: "Based on my pawpal_system.py skeleton, how should the Scheduler retrieve all tasks from the Owner's pets?" and "Why is this test failing, and is the bug in my test code or my pawpal_system.py logic?" These targeted questions with file references (#file:) gave me precise, actionable suggestions rather than generic advice.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.

When implementing the `is_feasible()` method in DailySchedule, Copilot suggested checking for overlapping time intervals using complex datetime arithmetic. I rejected this in favor of a simpler approach that only checks if the total scheduled time exceeds owner availability, since the current system uses exact-time scheduling rather than interval overlaps. This kept the code cleaner and more aligned with the MVP scope.

- How did you evaluate or verify what the AI suggested?

I evaluated AI suggestions by: 1) Running the code to see if it works, 2) Checking if it aligns with the overall system design and constraints, 3) Considering code readability and maintainability, 4) Testing edge cases manually, and 5) Comparing with existing patterns in the codebase. For complex logic, I also asked follow-up questions like "Can you explain this approach in simpler terms?"

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?

I tested core functionality (task creation/completion, pet management), scheduling logic (priority sorting, time-based scheduling, feasibility), advanced features (time sorting, filtering, recurring tasks, conflict detection), and edge cases (empty pets, time conflicts, availability limits, due date overrides). All 30 tests cover happy paths and error conditions.

- Why were these tests important?

The tests ensure the system works reliably across different scenarios. Core functionality tests verify basic operations, scheduling tests validate the "smart" algorithms, advanced feature tests confirm the Phase 4 enhancements work correctly, and edge case tests prevent regressions. This comprehensive coverage gives confidence that the system handles real-world pet care scenarios without breaking.

**b. Confidence**

- How confident are you that your scheduler works correctly?

Very confident (5/5 stars) - all 30 automated tests pass, covering core functionality, advanced features, and edge cases. The system successfully handles task scheduling, recurrence, conflict detection, and multi-pet scenarios.

- What edge cases would you test next if you had more time?

I'd test: overlapping time intervals (not just exact matches), multi-day scheduling, task dependencies, weather-based scheduling adjustments, and integration with external calendars. I'd also add performance tests for larger pet/task datasets and user acceptance testing with real pet owners.

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

I'm most satisfied with how the system evolved from a simple skeleton to a fully functional, tested pet care assistant. The modular OOP design made it easy to add features incrementally, and the comprehensive test suite (30 tests) gives real confidence in the system's reliability. The AI collaboration was particularly effective - Copilot helped accelerate development while I maintained architectural control.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

I'd improve the conflict detection to handle overlapping intervals rather than exact time matches, add a more sophisticated scheduling algorithm that considers task dependencies and optimal time slots, and enhance the UI with drag-and-drop task reordering and calendar integration. I'd also add user authentication and data persistence to make it a real web app.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?

The most important lesson was learning to be the "lead architect" in AI-assisted development. While AI tools like Copilot excel at code generation and debugging, the human developer must maintain the big-picture vision, make judgment calls on suggestions, and ensure the system remains coherent and maintainable. AI accelerates development but doesn't replace the need for thoughtful system design and critical evaluation of automated suggestions.
