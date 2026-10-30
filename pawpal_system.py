from dataclasses import dataclass, field
from datetime import date, timedelta


@dataclass
class Task:
    description: str
    time: str  # "HH:MM"
    frequency: str = "once"  # "once", "daily" or "weekly"
    completed: bool = False
    due_date: date = field(default_factory=date.today)

    def mark_complete(self) -> None:
        """Mark this task as done."""
        self.completed = True


@dataclass
class Pet:
    name: str
    species: str
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a task to this pet's task list."""
        self.tasks.append(task)

    def get_tasks(self) -> list[Task]:
        """Return this pet's tasks."""
        return self.tasks


class Owner:
    def __init__(self, name: str):
        self.name = name
        self.pets: list[Pet] = []

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner."""
        self.pets.append(pet)

    def get_all_tasks(self) -> list[tuple[Pet, Task]]:
        """Return a (pet, task) pair for every task across all pets."""
        return [(pet, task) for pet in self.pets for task in pet.get_tasks()]


class Scheduler:
    def __init__(self, owner: Owner):
        self.owner = owner

    def sort_by_time(self, pairs: list[tuple[Pet, Task]]) -> list[tuple[Pet, Task]]:
        """Return (pet, task) pairs ordered by due date, then by "HH:MM" time."""
        return sorted(pairs, key=lambda pair: (pair[1].due_date, pair[1].time))

    def filter_tasks(
        self, completed: bool | None = None, pet_name: str | None = None
    ) -> list[tuple[Pet, Task]]:
        """Return pairs matching the given completion status and/or pet name (case-insensitive)."""
        pairs = self.owner.get_all_tasks()
        if completed is not None:
            pairs = [(pet, task) for pet, task in pairs if task.completed == completed]
        if pet_name is not None:
            pairs = [(pet, task) for pet, task in pairs if pet.name.lower() == pet_name.lower()]
        return pairs

    def get_todays_schedule(self) -> list[tuple[Pet, Task]]:
        """Return tasks due today across all pets, ordered by time."""
        today = [(pet, task) for pet, task in self.owner.get_all_tasks() if task.due_date == date.today()]
        return self.sort_by_time(today)

    def complete_task(self, pet: Pet, task: Task) -> Task | None:
        """Mark a task complete; for daily or weekly tasks, add the next one to the pet and return it."""
        task.mark_complete()
        days = {"daily": 1, "weekly": 7}.get(task.frequency)
        if days is None:
            return None
        next_task = Task(task.description, task.time, task.frequency, due_date=task.due_date + timedelta(days=days))
        pet.add_task(next_task)
        return next_task

    def find_conflicts(self) -> list[str]:
        """Return a warning for each time slot with two or more unfinished tasks (same or different pets)."""
        slots: dict[tuple[date, str], list[tuple[Pet, Task]]] = {}
        for pet, task in self.filter_tasks(completed=False):
            slots.setdefault((task.due_date, task.time), []).append((pet, task))
        return [
            f"Conflict on {due} at {time}: " + ", ".join(f"{pet.name} - {task.description}" for pet, task in pairs)
            for (due, time), pairs in sorted(slots.items())
            if len(pairs) > 1
        ]
