from datetime import datetime
from pawpal_system import Task, Pet, Owner, Scheduler


def test_task_completion():
    task = Task(
        id=1,
        title="Feed",
        category="feeding",
        duration_minutes=10,
        priority=3,
        due_time=datetime.now()
    )

    assert task.completed is False

    task.mark_completed()

    assert task.completed is True


def test_add_task_to_pet():
    pet = Pet(
        id=1,
        name="Milo",
        species="Dog",
        age=3
    )

    task = Task(
        id=2,
        title="Walk",
        category="walk",
        duration_minutes=20,
        priority=4
    )

    assert len(pet.tasks) == 0

    pet.add_task(task)

    assert len(pet.tasks) == 1


def test_sort_tasks_by_due_time():
    scheduler = Scheduler()

    t1 = Task(
        id=1,
        title="Walk",
        category="walk",
        duration_minutes=20,
        priority=3,
        due_time=datetime(2026, 1, 1, 12, 0),
    )
    t2 = Task(
        id=2,
        title="Feed",
        category="feeding",
        duration_minutes=10,
        priority=3,
        due_time=datetime(2026, 1, 1, 9, 0),
    )
    t3 = Task(
        id=3,
        title="Medicine",
        category="medication",
        duration_minutes=5,
        priority=3,
        due_time=datetime(2026, 1, 1, 10, 0),
    )

    sorted_tasks = scheduler.sort_tasks([t1, t2, t3])

    assert [task.id for task in sorted_tasks] == [2, 3, 1]


def test_recurring_task_creates_next_day_task():
    pet = Pet(
        id=1,
        name="Milo",
        species="Dog",
        age=3
    )

    recurring_task = Task(
        id=10,
        title="Daily Feeding",
        category="feeding",
        duration_minutes=10,
        priority=3,
        due_time=datetime(2026, 1, 1, 8, 0),
        recurrence={"freq": "daily", "interval": 1},
    )

    pet.add_task(recurring_task)
    new_task = pet.mark_task_complete(10)

    assert recurring_task.completed is True
    assert new_task is not None
    assert new_task.due_time == datetime(2026, 1, 2, 8, 0)
    assert len(pet.tasks) == 2


def test_conflict_detection_flags_duplicate_due_times():
    scheduler = Scheduler()
    owner = Owner(
        id=1,
        name="Altair"
    )

    dog = Pet(
        id=1,
        name="Milo",
        species="Dog",
        age=4
    )
    cat = Pet(
        id=2,
        name="Luna",
        species="Cat",
        age=2
    )

    same_time = datetime(2026, 1, 1, 9, 0)

    t1 = Task(
        id=1,
        title="Morning Walk",
        category="walk",
        duration_minutes=20,
        priority=3,
        due_time=same_time,
    )
    t2 = Task(
        id=2,
        title="Feed Breakfast",
        category="feeding",
        duration_minutes=10,
        priority=3,
        due_time=same_time,
    )

    dog.add_task(t1)
    cat.add_task(t2)
    owner.add_pet(dog)
    owner.add_pet(cat)

    warnings = scheduler.detect_due_time_conflicts([t1, t2], owner)

    assert len(warnings) == 1
    assert "same due time" in warnings[0]