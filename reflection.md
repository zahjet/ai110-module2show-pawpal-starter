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

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

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
