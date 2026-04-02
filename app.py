import streamlit as st
from datetime import datetime, time
from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to **PawPal+** - Your pet care planning assistant!

This app helps you organize your pet's daily tasks based on your availability and priorities.
"""
)


st.divider()

# ===== INITIALIZE SESSION STATE =====
# Store the Owner object so it persists across page refreshes
if "owner" not in st.session_state:
    st.session_state.owner = None

if "selected_pet" not in st.session_state:
    st.session_state.selected_pet = None

# ===== OWNER SETUP SECTION =====
st.subheader("👤 Owner Setup")

owner_name = st.text_input("Owner name", value="Jordan", key="owner_name_input")
available_hours = st.slider(
    "Available pet care time per day (hours)", 
    min_value=0.5, 
    max_value=24.0, 
    value=4.0, 
    step=0.5,
    key="available_hours"
)

if st.button("Create/Update Owner", key="btn_owner"):
    st.session_state.owner = Owner(name=owner_name, available_hours=available_hours)
    st.success(f"✓ Owner '{owner_name}' created with {available_hours}h availability per day")

if st.session_state.owner:
    st.info(f"📌 Current owner: **{st.session_state.owner.name}** ({st.session_state.owner.available_hours}h available)")
else:
    st.warning("⚠️ Please create an owner first")

st.divider()

# ===== PET MANAGEMENT SECTION =====
if st.session_state.owner:
    st.subheader("🐾 Pet Management")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        pet_name = st.text_input("Pet name", value="Mochi", key="pet_name_input")
    with col2:
        species = st.selectbox("Species", ["dog", "cat", "other"], key="species_select")
    with col3:
        age = st.number_input("Age (years)", min_value=0.1, max_value=50.0, value=3.0, step=0.1, key="age_input")
    
    health_notes = st.text_input("Health notes (optional)", value="Energetic and playful", key="health_notes")
    
    if st.button("Add Pet", key="btn_add_pet"):
        new_pet = Pet(name=pet_name, species=species, age=age, health_notes=health_notes)
        st.session_state.owner.add_pet(new_pet)
        st.session_state.selected_pet = new_pet
        st.success(f"✓ Added {pet_name} the {species}")
    
    # Display current pets
    if st.session_state.owner.get_pets():
        st.markdown("**Current pets:**")
        for idx, pet in enumerate(st.session_state.owner.get_pets()):
            col1, col2 = st.columns([3, 1])
            with col1:
                if st.button(f"📌 {pet.name} ({pet.species}, age {pet.age})", key=f"pet_{idx}"):
                    st.session_state.selected_pet = pet
            with col2:
                st.text(f"{len(pet.get_tasks())} tasks")
    
    st.divider()
    
    # ===== TASK MANAGEMENT SECTION =====
    if st.session_state.selected_pet:
        st.subheader(f"✏️ Tasks for {st.session_state.selected_pet.name}")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            task_title = st.text_input("Task title", value="Morning walk", key="task_title")
        with col2:
            duration = st.number_input("Duration (min)", min_value=1, max_value=240, value=30, key="task_duration")
        with col3:
            priority = st.selectbox("Priority", ["low", "medium", "high"], index=2, key="task_priority")
        with col4:
            frequency = st.selectbox("Frequency", ["daily", "weekly", "as_needed"], key="task_frequency")
        
        if st.button("Add Task", key="btn_add_task"):
            new_task = Task(
                title=task_title,
                duration_minutes=int(duration),
                priority=priority,
                frequency=frequency
            )
            st.session_state.selected_pet.add_task(new_task)
            st.success(f"✓ Added task '{task_title}' to {st.session_state.selected_pet.name}")
        
        # Display tasks for selected pet
        tasks = st.session_state.selected_pet.get_tasks()
        if tasks:
            st.markdown(f"**Tasks for {st.session_state.selected_pet.name}:**")
            
            # Add sorting/filtering options
            col1, col2, col3 = st.columns(3)
            with col1:
                sort_option = st.selectbox(
                    "Sort by:", 
                    ["Priority", "Time", "Title"], 
                    key="sort_option"
                )
            with col2:
                filter_option = st.selectbox(
                    "Filter:", 
                    ["All", "Completed", "Pending"], 
                    key="filter_option"
                )
            with col3:
                if st.button("🔄 Refresh Tasks", key="refresh_tasks"):
                    st.rerun()
            
            # Apply sorting and filtering
            scheduler = Scheduler(st.session_state.owner, st.session_state.selected_pet)
            
            if sort_option == "Priority":
                sorted_tasks = scheduler.sort_tasks_by_priority()
            elif sort_option == "Time":
                sorted_tasks = scheduler.sort_tasks_by_time()
            else:  # Title
                sorted_tasks = sorted(tasks, key=lambda t: t.title)
            
            # Apply filtering
            if filter_option == "Completed":
                filtered_tasks = scheduler.filter_tasks(completed=True)
            elif filter_option == "Pending":
                filtered_tasks = scheduler.filter_tasks(completed=False)
            else:
                filtered_tasks = sorted_tasks
            
            # Display tasks in a nice table
            task_data = []
            for task in filtered_tasks:
                status_icon = "✅" if task.is_completed else "⏳"
                priority_icon = {"low": "🟢", "medium": "🟡", "high": "🔴"}.get(task.priority, "⚪")
                time_str = task.scheduled_time or "Not set"
                task_data.append({
                    "Status": status_icon,
                    "Title": task.title,
                    "Time": time_str,
                    "Priority": f"{priority_icon} {task.priority}",
                    "Duration": f"{task.duration_minutes}m",
                    "Frequency": task.frequency
                })
            
            if task_data:
                st.table(task_data)
            else:
                st.info("No tasks match the current filter.")
        else:
            st.info("No tasks yet. Add one above.")
        
        st.divider()
        
        # ===== SCHEDULE GENERATION =====
        st.subheader("📅 Generate Daily Schedule")
        
        # Check for conflicts before scheduling
        if st.session_state.owner:
            conflicts = st.session_state.owner.detect_all_time_conflicts()
            if conflicts:
                st.warning("⚠️ **Time Conflicts Detected:**")
                for conflict in conflicts:
                    st.text(f"  • {conflict}")
                st.info("💡 Tip: Edit task times to resolve conflicts before scheduling.")
        
        if st.button("Generate Schedule", key="btn_generate_schedule"):
            scheduler = Scheduler(st.session_state.owner, st.session_state.selected_pet)
            schedule = scheduler.generate_schedule(datetime.now())
            
            # Display results
            st.markdown("### 📋 Today's Schedule")
            st.info(schedule.get_explanation())
            
            # Feasibility check
            if schedule.is_feasible():
                st.success("✓ Schedule is feasible - all tasks fit within available time!")
            else:
                st.error("⚠️ Schedule exceeds available time or has conflicts.")
            
            # Show scheduled tasks in a nice format
            if schedule.scheduled_tasks:
                st.markdown("**Scheduled Tasks:**")
                schedule_data = []
                for st_task in schedule.scheduled_tasks:
                    schedule_data.append({
                        "Time": st_task.start_time.strftime("%I:%M %p"),
                        "Task": st_task.task.title,
                        "Duration": f"{st_task.task.duration_minutes}m",
                        "Priority": st_task.task.priority
                    })
                st.table(schedule_data)
            
            # Check for conflicts in the generated schedule
            schedule_conflicts = scheduler.check_time_conflicts()
            if schedule_conflicts:
                st.warning("⚠️ **Scheduling Issues:**")
                for conflict in schedule_conflicts:
                    st.text(f"  • {conflict}")
else:
    st.warning("⚠️ Please set up an owner first to manage pets and tasks.")
