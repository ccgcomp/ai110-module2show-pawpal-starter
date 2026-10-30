# PawPal+ Project Reflection

## 1. System Design

**Three core actions a user should be able to do**

1. Add a pet (the owner enters their name, the pet's name, and the species)
2. Add a task for a pet
3. See the schedule

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

My design has four classes. **Task** is a dataclass holding a description, a time ("HH:MM"), a frequency (once,
daily or weekly) and a completed flag, and it can mark itself complete. **Pet** is a dataclass with a name,
species and a list of its tasks, and it can add and list them. **Owner** holds the owner's name and list of pets
and can gather every task across all of them. **Scheduler** takes an Owner and builds the daily schedule from the
tasks of all their pets, so the organizing logic lives in one place and the other three classes mostly just hold
data.

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

Yes. In my first design, `Owner.get_all_tasks()` and `Scheduler.get_todays_schedule()` returned plain lists of
Tasks. During the skeleton review I noticed a schedule line like "08:00 Walk" can't say which pet it is for once
the owner has 2 or more pets. I considered adding a `pet_name` to Task, but that would give Task a back-link to
Pet that I'd have to keep in sync. Instead both methods now return `(pet, task)` pairs, so Task stays unchanged
and the Scheduler, which works across pets, is the one that knows where each task came from.

A second change came in the algorithms phase. Recurring tasks need a date to add one day or one week to, but Task
only had a time, so I added a `due_date` field (defaulting to today). Completing a daily or weekly task now creates
a new Task with `due_date` moved forward using `timedelta`, and `get_todays_schedule()` only shows tasks due today.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

My scheduler only flags a conflict when two unfinished tasks have exactly the same date and "HH:MM" time. It does
not check overlapping durations, so a 30-minute walk at 07:30 and a feeding at 07:45 are not flagged. That is
reasonable here because Task has no duration (I kept it out of the design on purpose), exact matches are simple to
explain and test, and a warning that never crashes the app is more useful to a busy owner than a complicated rule
that might be wrong.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

When I asked the AI to simplify `find_conflicts()`, it offered a version using `itertools.groupby` instead of
building a dictionary with `setdefault`. I ran both on the same mixed set of tasks and they returned identical
warnings, so the question was readability. The `groupby` version was not shorter: it needs the list sorted first,
the key lambda written out twice, and `list(group)` before it can check the length. The dictionary version reads
top to bottom without those extra requirements, so I kept my original and rejected the suggestion.

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
