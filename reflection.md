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

My scheduler looks at four things about each task: its due date, its time of day, its frequency, and whether it is
done. Due date and time matter most because they decide what appears in today's schedule and in what order. A task
that is not due today is left out, and everything else is sorted by `HH:MM` across all pets. Completion status comes
next: finished tasks stop causing conflict warnings, and the filter can show done or not-done tasks. Frequency only
matters at the moment a task is completed, when it decides whether a next task is created and how far ahead (1 day
or 7 days). I left priority and duration out on purpose. The README mentions them, but my three core actions did
not need them, and adding them would have meant more fields to keep correct and more tests.

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

I used Claude Code in VS Code for most of the project: brainstorming the class attributes and methods, writing the
Mermaid diagram, reviewing the class skeleton for missing relationships, writing the method bodies, drafting the
test suite, and connecting the Streamlit UI. The most helpful prompts gave it a boundary. Asking for "only what my
three actions need" kept the design to the four required classes, the same lesson as ByteBites. Asking it to review
my skeleton for missing relationships found the real gap, that a schedule line could not say which pet a task
belonged to. Asking it to simplify an algorithm and then comparing the result was also useful, because it forced me
to judge the answer instead of just accepting it. I did not use separate chat sessions for the algorithm and test
phases, so I can't say how much they would have helped. Everything was done in one long session.

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

I wrote 17 tests. They cover the core classes (marking a task complete, adding a task to a pet, gathering tasks
across pets), sorting (chronological order across pets, only tasks due today, empty pet and empty owner), filtering
(by pet name ignoring case, by status, and with no options), recurring tasks (daily creates tomorrow's task, weekly
creates one 7 days later, a one-time task creates nothing), and conflicts (same time for different pets and for the
same pet are flagged; different times, completed tasks, and the same time on different days are not). These matter
because the scheduler is the part of the system that makes decisions. A wrong sort order or a missed conflict would
not crash anything, so the app would look fine while giving the owner a bad plan. Tests are the only thing that
would notice.

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

I'm fairly confident, about 4 out of 5. Every scheduling behavior has a passing test, including edge cases, and the
demo script produces the output I expect. None of my tests failed when I first ran them, which I don't take as proof
that nothing is wrong. The one real bug I found was in the UI, not in the tested logic: a success message shown just
before `st.rerun()` disappeared instantly, and I caught that by rereading the code, not through a test. The UI itself
has no automated tests. Next I would test invalid time strings like "25:99" or an empty time, two pets with the same
name (filtering by name would mix them up), overdue tasks (a daily task not completed yesterday drops out of today's
schedule instead of showing as overdue), and tasks that overlap by duration, which my exact-time check ignores.

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

I'm most satisfied with how the Scheduler ended up. It works across all pets, never stores its own copy of the data,
and every feature (sorting, filtering, recurring tasks, conflicts) is a small method that can be tested on its own.
Returning `(pet, task)` pairs was a small design change that made the schedule readable for more than one pet without
adding a back-link from Task to Pet.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

I would add editing and removing tasks and pets, since right now a mistake can't be undone. I would add a duration
to Task so conflicts can catch overlapping tasks, not only identical times. I would show overdue tasks instead of
dropping them from today's schedule. I would also save the data to a file, because everything is lost when the
Streamlit app restarts, and add automated tests for the UI.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?

Deciding the design first and then telling the AI what not to add produced a much smaller and more correct system
than letting it propose features. Every addition I accepted (returning pairs, `due_date`) came from a specific
problem I could point to, and the one I rejected (the `groupby` rewrite) did not make anything easier to read. My job
as the lead architect was less about writing code and more about asking "is this needed?" and checking claims by
running them.
