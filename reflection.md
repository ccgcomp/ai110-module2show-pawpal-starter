# PawPal+ Project Reflection

## 1. System Design

**Three core actions a user should be able to do**

1. Add a pet (the owner enters their name, the pet's name, and the species)
2. Add a task for a pet
3. See the schedule

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

Yes. In my first design, `Owner.get_all_tasks()` and `Scheduler.get_todays_schedule()` returned plain lists of
Tasks. During the skeleton review I noticed a schedule line like "08:00 Walk" can't say which pet it is for once
the owner has 2 or more pets. I considered adding a `pet_name` to Task, but that would give Task a back-link to
Pet that I'd have to keep in sync. Instead both methods now return `(pet, task)` pairs, so Task stays unchanged
and the Scheduler, which works across pets, is the one that knows where each task came from.

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
