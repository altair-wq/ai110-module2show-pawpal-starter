from datetime import date, datetime, timedelta

from pawpal_system import Owner, Pet, Task, Scheduler


def print_task_list(title: str, tasks: list[Task]) -> None:
    print(f"\n=== {title} ===\n")
    if not tasks:
        print("No tasks found.")
        return

    for task in tasks:
        due = task.due_time.strftime("%Y-%m-%d %H:%M") if task.due_time else "No due time"
        status = "completed" if task.completed else "incomplete"
        print(
            f"- {task.title} ({task.category}) | due {due} | "
            f"priority {task.priority} | {status}"
        )


def main() -> None:
    owner = Owner(
        id=1,
        name="Altair",
        contact="altair@example.com",
        available_time={
            "mon": [(9, 11)],
            "tue": [(9, 11)],
            "wed": [(9, 11)],
            "thu": [(9, 11)],
            "fri": [(9, 11)],
            "sat": [(10, 12)],
            "sun": [(10, 12)],
        },
        preferences={"prefer_high_priority": True},
    )

    dog = Pet(id=1, name="Milo", species="Dog", age=4, notes="Needs daily walk")
    cat = Pet(id=2, name="Luna", species="Cat", age=2, notes="Takes medication")

    now = datetime.now()
    today = date.today()

    same_time = datetime.combine(today, (now + timedelta(hours=1)).time())

    # Added out of order on purpose for sorting + conflict demo
    walk_task = Task(
        id=1,
        title="Morning Walk",
        category="walk",
        duration_minutes=30,
        priority=5,
        due_time=same_time,
    )
    feed_task = Task(
        id=2,
        title="Feed Breakfast",
        category="feeding",
        duration_minutes=10,
        priority=4,
        due_time=same_time,
    )
    med_task = Task(
        id=3,
        title="Give Medication",
        category="medication",
        duration_minutes=5,
        priority=5,
        due_time=datetime.combine(today, (now + timedelta(hours=2)).time()),
    )

    dog.add_task(walk_task)
    dog.add_task(feed_task)
    cat.add_task(med_task)

    owner.add_pet(dog)
    owner.add_pet(cat)

    scheduler = Scheduler()

    all_tasks: list[Task] = []
    for pet in owner.pets:
        all_tasks.extend(pet.tasks)

    print_task_list("Tasks Added Out of Order", all_tasks)

    sorted_tasks = scheduler.sort_tasks(all_tasks)
    print_task_list("Sorted Tasks", sorted_tasks)

    filtered_by_pet = scheduler.filter_tasks(all_tasks, pet_name="Milo", owner=owner)
    print_task_list("Filtered Tasks: Milo Only", filtered_by_pet)

    filtered_incomplete = scheduler.filter_tasks(all_tasks, completed=False)
    print_task_list("Filtered Tasks: Incomplete Only", filtered_incomplete)

    print("\n=== Recurring Task Demo ===\n")

    daily_task = Task(
        id=10,
        title="Daily Feeding",
        category="feeding",
        duration_minutes=10,
        priority=3,
        due_time=datetime.combine(today, now.time()),
        recurrence={"freq": "daily", "interval": 1},
    )

    dog.add_task(daily_task)

    print("Before completion:")
    print_task_list("Dog Tasks", dog.tasks)

    next_task = dog.mark_task_complete(10)

    print("\nAfter completion:")
    print_task_list("Dog Tasks", dog.tasks)

    if next_task:
        print(f"\nNew recurring task created for: {next_task.due_time}")

    conflict_warnings = scheduler.detect_due_time_conflicts(all_tasks, owner)

    print("\n=== Conflict Warnings ===\n")
    if conflict_warnings:
        for warning in conflict_warnings:
            print(warning)
    else:
        print("No conflicts detected.")

    plan = scheduler.generate_daily_plan(owner, today)

    print("\n=== Today's Schedule ===\n")

    scheduled = plan.get("scheduled", [])
    unscheduled = plan.get("unscheduled", [])

    if not scheduled:
        print("No tasks scheduled for today.")
    else:
        for item in scheduled:
            print(
                f"- {item['task_title']} ({item['pet_name']})\n"
                f"  Time: {item['start'].strftime('%H:%M')} - {item['end'].strftime('%H:%M')}\n"
                f"  Reason: {item['reason']}\n"
            )

    if unscheduled:
        print("=== Unscheduled Tasks ===\n")
        for task_id in unscheduled:
            print(f"- Task ID: {task_id}")


if __name__ == "__main__":
    main()