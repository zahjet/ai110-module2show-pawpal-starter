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
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.

The scheduler currently uses exact scheduled-time string matching for conflict detection (like two tasks both at "08:00") rather than detecting partially overlapping intervals (like 08:00-08:30 and 08:15-08:45). This is simpler and lightweight for initial MVP behavior, but it can miss real conflicts where tasks overlap without exact start-time equality.

- Why is that tradeoff reasonable for this scenario?

For a pet care assistant in early stages, precise interval math adds complexity and edge cases; using exact-time rules provides clear, predictable warnings with minimal code. As usage grows, the app can evolve into full interval overlap checking.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
