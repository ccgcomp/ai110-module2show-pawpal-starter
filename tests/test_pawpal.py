from datetime import date, timedelta

from pawpal_system import Owner, Pet, Scheduler, Task


def make_owner():
    """One owner with two pets and no tasks."""
    owner = Owner("Cody")
    buddy = Pet("Buddy", "dog")
    whiskers = Pet("Whiskers", "cat")
    owner.add_pet(buddy)
    owner.add_pet(whiskers)
    return owner, buddy, whiskers


# --- Core classes ---

def test_mark_complete_changes_status():
    task = Task("Morning walk", "07:30")
    assert task.completed is False
    task.mark_complete()
    assert task.completed is True


def test_add_task_increases_pet_task_count():
    pet = Pet("Buddy", "dog")
    assert len(pet.get_tasks()) == 0
    pet.add_task(Task("Morning walk", "07:30"))
    assert len(pet.get_tasks()) == 1


def test_owner_gathers_tasks_from_all_pets():
    owner, buddy, whiskers = make_owner()
    buddy.add_task(Task("Walk", "07:30"))
    whiskers.add_task(Task("Breakfast", "08:00"))
    pets_seen = {pet.name for pet, _ in owner.get_all_tasks()}
    assert pets_seen == {"Buddy", "Whiskers"}


# --- Sorting ---

def test_schedule_is_in_chronological_order_across_pets():
    owner, buddy, whiskers = make_owner()
    buddy.add_task(Task("Evening feeding", "18:00"))
    whiskers.add_task(Task("Breakfast", "08:00"))
    buddy.add_task(Task("Morning walk", "07:30"))
    times = [task.time for _, task in Scheduler(owner).get_todays_schedule()]
    assert times == ["07:30", "08:00", "18:00"]


def test_schedule_only_includes_tasks_due_today():
    owner, buddy, _ = make_owner()
    buddy.add_task(Task("Walk", "07:30"))
    buddy.add_task(Task("Future walk", "07:30", due_date=date.today() + timedelta(days=1)))
    descriptions = [task.description for _, task in Scheduler(owner).get_todays_schedule()]
    assert descriptions == ["Walk"]


def test_pet_with_no_tasks_and_owner_with_no_pets_give_empty_schedule():
    owner, _, _ = make_owner()
    assert Scheduler(owner).get_todays_schedule() == []
    assert Scheduler(Owner("Nobody")).get_todays_schedule() == []


# --- Filtering ---

def test_filter_by_pet_name_ignores_case():
    owner, buddy, whiskers = make_owner()
    buddy.add_task(Task("Walk", "07:30"))
    whiskers.add_task(Task("Breakfast", "08:00"))
    result = Scheduler(owner).filter_tasks(pet_name="buddy")
    assert [task.description for _, task in result] == ["Walk"]


def test_filter_by_completion_status():
    owner, buddy, _ = make_owner()
    done = Task("Walk", "07:30")
    done.mark_complete()
    buddy.add_task(done)
    buddy.add_task(Task("Feed", "18:00"))
    scheduler = Scheduler(owner)
    assert [t.description for _, t in scheduler.filter_tasks(completed=True)] == ["Walk"]
    assert [t.description for _, t in scheduler.filter_tasks(completed=False)] == ["Feed"]


def test_filter_with_no_options_returns_everything():
    owner, buddy, whiskers = make_owner()
    buddy.add_task(Task("Walk", "07:30"))
    whiskers.add_task(Task("Breakfast", "08:00"))
    assert len(Scheduler(owner).filter_tasks()) == 2


# --- Recurring tasks ---

def test_completing_daily_task_creates_next_day_task():
    owner, buddy, _ = make_owner()
    walk = Task("Walk", "07:30", "daily")
    buddy.add_task(walk)
    next_task = Scheduler(owner).complete_task(buddy, walk)
    assert walk.completed is True
    assert next_task.due_date == walk.due_date + timedelta(days=1)
    assert next_task.completed is False
    assert next_task in buddy.get_tasks()


def test_completing_weekly_task_creates_task_seven_days_later():
    owner, buddy, _ = make_owner()
    meds = Task("Flea medication", "12:00", "weekly")
    buddy.add_task(meds)
    next_task = Scheduler(owner).complete_task(buddy, meds)
    assert next_task.due_date == meds.due_date + timedelta(days=7)


def test_completing_one_time_task_creates_nothing():
    owner, buddy, _ = make_owner()
    vet = Task("Vet appointment", "15:00", "once")
    buddy.add_task(vet)
    assert Scheduler(owner).complete_task(buddy, vet) is None
    assert len(buddy.get_tasks()) == 1


# --- Conflict detection ---

def test_scheduler_flags_duplicate_times_for_different_pets():
    owner, buddy, whiskers = make_owner()
    buddy.add_task(Task("Walk", "07:30"))
    whiskers.add_task(Task("Play", "07:30"))
    warnings = Scheduler(owner).find_conflicts()
    assert len(warnings) == 1
    assert "07:30" in warnings[0] and "Buddy" in warnings[0] and "Whiskers" in warnings[0]


def test_scheduler_flags_duplicate_times_for_same_pet():
    owner, buddy, _ = make_owner()
    buddy.add_task(Task("Feed", "18:00"))
    buddy.add_task(Task("Brush teeth", "18:00"))
    assert len(Scheduler(owner).find_conflicts()) == 1


def test_no_conflicts_when_times_differ():
    owner, buddy, whiskers = make_owner()
    buddy.add_task(Task("Walk", "07:30"))
    whiskers.add_task(Task("Breakfast", "08:00"))
    assert Scheduler(owner).find_conflicts() == []


def test_completed_task_is_not_a_conflict():
    owner, buddy, whiskers = make_owner()
    done = Task("Walk", "07:30")
    done.mark_complete()
    buddy.add_task(done)
    whiskers.add_task(Task("Play", "07:30"))
    assert Scheduler(owner).find_conflicts() == []


def test_same_time_on_different_days_is_not_a_conflict():
    owner, buddy, _ = make_owner()
    buddy.add_task(Task("Walk", "07:30"))
    buddy.add_task(Task("Walk", "07:30", due_date=date.today() + timedelta(days=1)))
    assert Scheduler(owner).find_conflicts() == []
