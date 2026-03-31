from datetime import datetime
from pawpal_system import Task, Pet


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