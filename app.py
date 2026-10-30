import streamlit as st

from pawpal_system import Owner, Pet, Scheduler, Task

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")
st.caption("Track pet care tasks and see one schedule across all your pets.")

# Create the Owner once; session_state keeps it alive across Streamlit reruns.
if "owner" not in st.session_state:
    st.session_state.owner = Owner("Jordan")
owner = st.session_state.owner

st.divider()

st.subheader("Owner")
owner.name = st.text_input("Owner name", value=owner.name)

st.subheader("Add a Pet")
pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])

if st.button("Add pet"):
    if not pet_name.strip():
        st.error("Please enter a pet name.")
    else:
        owner.add_pet(Pet(pet_name.strip(), species))
        st.success(f"Added {pet_name.strip()} the {species}.")

if owner.pets:
    st.write("Your pets:")
    st.table([{"Name": p.name, "Species": p.species, "Tasks": len(p.get_tasks())} for p in owner.pets])
else:
    st.info("No pets yet. Add one above.")

st.subheader("Add a Task")
if owner.pets:
    pet_choice = st.selectbox("Pet", [p.name for p in owner.pets])
    task_description = st.text_input("Task description", value="Morning walk")
    col1, col2 = st.columns(2)
    with col1:
        task_time = st.time_input("Time", value=None)
    with col2:
        frequency = st.selectbox("Frequency", ["once", "daily", "weekly"], index=1)

    if st.button("Add task"):
        if not task_description.strip() or task_time is None:
            st.error("Please enter a description and a time.")
        else:
            pet = next(p for p in owner.pets if p.name == pet_choice)
            pet.add_task(Task(task_description.strip(), task_time.strftime("%H:%M"), frequency))
            st.success(f"Added '{task_description.strip()}' for {pet.name}.")
else:
    st.info("Add a pet first, then you can give it tasks.")

st.divider()

st.subheader("Today's Schedule")
schedule = Scheduler(owner).get_todays_schedule()
if schedule:
    st.table(
        [
            {
                "Time": task.time,
                "Pet": f"{pet.name} ({pet.species})",
                "Task": task.description,
                "Frequency": task.frequency,
                "Done": task.completed,
            }
            for pet, task in schedule
        ]
    )
else:
    st.info("No tasks scheduled yet.")
