import streamlit as st
from datetime import datetime, date, time as dtime
from typing import Optional

from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

if "owner" not in st.session_state:
    st.session_state["owner"] = Owner(
        id=1,
        name="Owner",
        available_time={
            "mon": [(9, 11)],
            "tue": [(9, 11)],
            "wed": [(9, 11)],
            "thu": [(9, 11)],
            "fri": [(9, 11)],
            "sat": [(10, 12)],
            "sun": [(10, 12)],
        },
    )

if "scheduler" not in st.session_state:
    st.session_state["scheduler"] = Scheduler()

if "next_pet_id" not in st.session_state:
    st.session_state["next_pet_id"] = 1

if "next_task_id" not in st.session_state:
    st.session_state["next_task_id"] = 1

owner: Owner = st.session_state["owner"]
scheduler: Scheduler = st.session_state["scheduler"]

st.title("🐾 PawPal+")
st.markdown("Plan pet care tasks with scheduling, recurrence, filtering, and conflict warnings.")

with st.expander("Scenario", expanded=False):
    st.markdown(
        """
**PawPal+** helps a pet owner manage care tasks such as feeding, walks, medication,
and grooming. It uses task priority, due times, recurrence, and available time slots
to build a daily plan.
"""
    )

st.divider()

st.subheader("Owner")
owner_name = st.text_input("Owner name", value=owner.name)
if owner_name != owner.name:
    owner.name = owner_name

st.divider()

st.subheader("Add a Pet")
with st.form("add_pet_form"):
    pet_name = st.text_input("Pet name", value="Mochi")
    species = st.selectbox("Species", ["dog", "cat", "other"])
    pet_age = st.number_input("Age", min_value=0, step=1, value=1)
    pet_notes = st.text_area("Notes", value="")
    pet_submitted = st.form_submit_button("Add Pet")

    if pet_submitted:
        new_pet = Pet(
            id=st.session_state["next_pet_id"],
            name=pet_name,
            species=species,
            age=int(pet_age),
            notes=pet_notes,
        )
        owner.add_pet(new_pet)
        st.session_state["next_pet_id"] += 1
        st.success(f"Added pet: {new_pet.name}")

st.subheader("Current Pets")
if owner.pets:
    for pet in owner.pets:
        st.write(f"- **{pet.name}** ({pet.species}), age {pet.age}")
else:
    st.info("No pets added yet.")

st.divider()

st.subheader("Add a Task")
if not owner.pets:
    st.info("Add a pet first before assigning tasks.")
else:
    pet_options = {f"{pet.name} (id={pet.id})": pet for pet in owner.pets}
    selected_pet_label = st.selectbox("Choose pet", list(pet_options.keys()))
    selected_pet = pet_options[selected_pet_label]

    with st.form("add_task_form"):
        task_title = st.text_input("Task title", value="Morning walk")
        task_category = st.text_input("Category", value="walk")
        duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
        priority_label = st.selectbox("Priority", ["low", "medium", "high"], index=2)

        set_due = st.checkbox("Set due date/time", value=False)
        due_dt: Optional[datetime] = None
        if set_due:
            due_date = st.date_input("Due date", value=date.today())
            due_time = st.time_input("Due time", value=dtime(9, 0))
            due_dt = datetime.combine(due_date, due_time)

        recurrence_label = st.selectbox("Recurrence", ["none", "daily", "weekly"], index=0)
        task_submitted = st.form_submit_button("Add Task")

        if task_submitted:
            priority_map = {"low": 1, "medium": 2, "high": 3}
            recurrence = None
            if recurrence_label == "daily":
                recurrence = {"freq": "daily", "interval": 1}
            elif recurrence_label == "weekly":
                recurrence = {"freq": "weekly", "interval": 1}

            new_task = Task(
                id=st.session_state["next_task_id"],
                title=task_title,
                category=task_category,
                duration_minutes=int(duration),
                priority=priority_map[priority_label],
                due_time=due_dt,
                recurrence=recurrence,
            )
            selected_pet.add_task(new_task)
            st.session_state["next_task_id"] += 1
            st.success(f"Added task '{new_task.title}' to {selected_pet.name}")

st.subheader("Current Tasks")
has_tasks = any(pet.tasks for pet in owner.pets)

if has_tasks:
    for pet in owner.pets:
        st.write(f"**Tasks for {pet.name}**")
        if pet.tasks:
            rows = []
            for task in pet.tasks:
                rows.append(
                    {
                        "id": task.id,
                        "title": task.title,
                        "category": task.category,
                        "duration": task.duration_minutes,
                        "priority": task.priority,
                        "due": task.due_time.strftime("%Y-%m-%d %H:%M") if task.due_time else "",
                        "recurrence": task.recurrence if task.recurrence else "",
                        "completed": task.completed,
                    }
                )
            st.table(rows)
        else:
            st.write("- no tasks")
else:
    st.info("No tasks added yet.")

st.divider()

st.subheader("Build Schedule")
plan_date = st.date_input("Plan date", value=date.today())

if st.button("Generate Schedule"):
    plan = scheduler.generate_daily_plan(owner, plan_date)
    scheduled = plan.get("scheduled", [])
    unscheduled = plan.get("unscheduled", [])

    all_tasks = []
    for pet in owner.pets:
        all_tasks.extend(pet.tasks)

    conflicts = scheduler.detect_due_time_conflicts(all_tasks, owner)

    st.subheader("📅 Schedule Results")

    if scheduled:
        display_rows = []
        for item in scheduled:
            display_rows.append(
                {
                    "Pet": item.get("pet_name"),
                    "Task": item.get("task_title"),
                    "Start": item.get("start").strftime("%H:%M") if item.get("start") else "",
                    "End": item.get("end").strftime("%H:%M") if item.get("end") else "",
                    "Reason": item.get("reason"),
                }
            )
        st.success("Schedule generated successfully.")
        st.table(display_rows)
    else:
        st.warning("No tasks could be scheduled for this date.")

    if unscheduled:
        st.warning("Some tasks could not be scheduled.")
        for task_id in unscheduled:
            st.write(f"- Unscheduled task ID: {task_id}")

    if conflicts:
        st.error("Conflict warnings:")
        for warning in conflicts:
            st.write(f"- {warning}")
    else:
        st.info("No conflict warnings detected.")