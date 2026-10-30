from pawpal_system import Owner, Pet, Scheduler, Task


def print_pairs(title: str, pairs) -> None:
    print(f"\n{title}")
    print("-" * 40)
    if not pairs:
        print("(none)")
    for pet, task in pairs:
        status = "x" if task.completed else " "
        print(f"[{status}] {task.due_date} {task.time}  {pet.name} ({pet.species}): {task.description} [{task.frequency}]")


def main() -> None:
    owner = Owner("Cody")

    buddy = Pet("Buddy", "dog")
    whiskers = Pet("Whiskers", "cat")
    owner.add_pet(buddy)
    owner.add_pet(whiskers)

    # Added out of time order on purpose, with two same-time pairs:
    # Buddy's walk vs Whiskers' play (different pets), and Buddy's feeding vs Buddy's teeth (same pet).
    buddy.add_task(Task("Evening feeding", "18:00", "daily"))
    buddy.add_task(Task("Morning walk", "07:30", "daily"))
    buddy.add_task(Task("Flea medication", "12:00", "weekly"))
    buddy.add_task(Task("Brush teeth", "18:00", "daily"))
    whiskers.add_task(Task("Clean litter box", "19:30", "daily"))
    whiskers.add_task(Task("Breakfast", "08:00", "daily"))
    whiskers.add_task(Task("Play time", "07:30", "once"))
    whiskers.add_task(Task("Vet appointment", "15:00", "once"))

    scheduler = Scheduler(owner)

    print_pairs(f"Today's Schedule for {owner.name} (sorted by time)", scheduler.get_todays_schedule())

    print("\nConflict warnings")
    print("-" * 40)
    for warning in scheduler.find_conflicts():
        print(f"WARNING: {warning}")

    # Complete Buddy's daily walk: it should create tomorrow's walk.
    walk = buddy.get_tasks()[1]
    next_walk = scheduler.complete_task(buddy, walk)
    print(f"\nCompleted '{walk.description}'. Next one created for {next_walk.due_date}.")

    print_pairs("Filter: Whiskers' tasks", scheduler.sort_by_time(scheduler.filter_tasks(pet_name="Whiskers")))
    print_pairs("Filter: completed tasks", scheduler.sort_by_time(scheduler.filter_tasks(completed=True)))
    print_pairs("Filter: Buddy's unfinished tasks", scheduler.sort_by_time(scheduler.filter_tasks(completed=False, pet_name="Buddy")))


if __name__ == "__main__":
    main()
