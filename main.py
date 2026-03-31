from datetime import date, datetime, timedelta

from pawpal_system import Owner, Pet, Task, Scheduler


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

    walk_task = Task(
        id=1,
        title="Morning Walk",
        category="walk",
        duration_minutes=30,
        priority=5,
        due_time=datetime.combine(today, (now + timedelta(hours=1)).time()),
    )
    feed_task = Task(
        id=2,
        title="Feed Breakfast",
        category="feeding",
        duration_minutes=10,
        priority=4,
        due_time=datetime.combine(today, (now + timedelta(minutes=30)).time()),
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