from pawpal_system import Owner, Pet, Scheduler, Task


def main() -> None:
    owner = Owner("Cody")

    buddy = Pet("Buddy", "dog")
    whiskers = Pet("Whiskers", "cat")
    owner.add_pet(buddy)
    owner.add_pet(whiskers)

    buddy.add_task(Task("Morning walk", "07:30", "daily"))
    buddy.add_task(Task("Evening feeding", "18:00", "daily"))
    buddy.add_task(Task("Flea medication", "12:00", "weekly"))
    whiskers.add_task(Task("Breakfast", "08:00", "daily"))
    whiskers.add_task(Task("Clean litter box", "19:30", "daily"))
    whiskers.add_task(Task("Vet appointment", "15:00", "once"))

    print(f"Today's Schedule for {owner.name}")
    print("-" * 40)
    for pet, task in Scheduler(owner).get_todays_schedule():
        status = "x" if task.completed else " "
        print(f"[{status}] {task.time}  {pet.name} ({pet.species}): {task.description} [{task.frequency}]")


if __name__ == "__main__":
    main()
