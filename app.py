import streamlit as st
import pandas as pd
import datetime as dt

st.title("Zoner: Jet Lag Adjustment Planner")

# --- Inputs ---
st.header("🌐 Input Your Travel Details")
direction = st.selectbox("Travel Direction", ["East (Advance Clock)", "West (Delay Clock)"])
bedtime_current = st.time_input("Current Bedtime (Home Time Zone)", value=dt.time(23, 0))
wake_current = st.time_input("Current Wake-Up Time (Home Time Zone)", value=dt.time(7, 0))
bedtime_local = st.time_input("Target Bedtime (Destination Time Zone)", value=dt.time(22, 0))
wake_local = st.time_input("Target Wake-Up Time (Destination Time Zone)", value=dt.time(6, 0))
meal_time_current = st.time_input("Current Meal Time", value=dt.time(12, 0))
time_shift = st.number_input("Total Hours to Shift (e.g., 6 for 6-hour shift)", min_value=1, max_value=12, value=6)
days_available = st.number_input("Number of Days for Adjustment", min_value=1, max_value=7, value=3)

# --- Helper Functions ---
def adjust_time(base_time, shift, days, advance=True):
    """Adjust a time by a shift per day."""
    delta = dt.timedelta(hours=shift * days)
    return base_time - delta if advance else base_time + delta

def format_schedule(schedule):
    """Format schedule DataFrame for display."""
    return schedule.applymap(lambda t: t.strftime('%H:%M') if isinstance(t, dt.time) else t)

# --- Calculations ---
# Convert times to datetime for calculations
base_date = dt.date.today()
bedtime_current_dt = dt.datetime.combine(base_date, bedtime_current)
wake_current_dt = dt.datetime.combine(base_date, wake_current)
meal_time_current_dt = dt.datetime.combine(base_date, meal_time_current)
t_min_dt = wake_current_dt - dt.timedelta(minutes=90)

# Calculate shift per day
shift_per_day = time_shift / days_available
advance = direction == "East (Advance Clock)"

# --- Generate Schedule ---
schedule = {
    "Activity": [
        "New Bedtime",
        "New Wake-Up",
        "New Meal Time",
        "Light Exposure Start",
        "Light Exposure End",
        "Light Avoidance Start",
        "Light Avoidance End",
        "Exercise Start",
        "Exercise End",
    ]
}

for day in range(1, days_available + 1):
    bedtime_new = adjust_time(bedtime_current_dt, shift_per_day, day, advance)
    wake_new = adjust_time(wake_current_dt, shift_per_day, day, advance)
    meal_time_new = adjust_time(meal_time_current_dt, shift_per_day, day, advance)
    light_time_start = t_min_dt + dt.timedelta(hours=2) if advance else t_min_dt - dt.timedelta(hours=6)
    light_time_end = t_min_dt + dt.timedelta(hours=4) if advance else t_min_dt - dt.timedelta(hours=4)

    bedtime_local_dt = dt.datetime.combine(base_date, bedtime_local)
    wake_local_dt = dt.datetime.combine(base_date, wake_local)

    light_avoid_start = bedtime_local_dt - dt.timedelta(hours=6) if advance else wake_local_dt + dt.timedelta(hours=2)
    light_avoid_end = bedtime_local_dt - dt.timedelta(hours=4) if advance else wake_local_dt + dt.timedelta(hours=4)
    exercise_start = t_min_dt + dt.timedelta(hours=1) if advance else t_min_dt - dt.timedelta(hours=4)
    exercise_end = t_min_dt + dt.timedelta(hours=4) if advance else t_min_dt - dt.timedelta(hours=1)

    schedule[f"Day {day}"] = [
        bedtime_new.time(),
        wake_new.time(),
        meal_time_new.time(),
        light_time_start.time(),
        light_time_end.time(),
        light_avoid_start.time(),
        light_avoid_end.time(),
        exercise_start.time(),
        exercise_end.time(),
    ]

# Convert schedule to DataFrame
schedule_df = pd.DataFrame(schedule)

# --- Display Schedule ---
st.header("📅 Personalized Adjustment Schedule")
st.write("Adjust your circadian rhythm day-by-day based on your travel details:")
st.dataframe(schedule_df.set_index("Activity").applymap(lambda t: t.strftime('%H:%M') if isinstance(t, dt.time) else t))

# --- Additional Tips ---
st.header("💡 Helpful Tips")
if advance:
    st.write("""
    - Expose yourself to bright light 2–4 hours after T_min each day.
    - Avoid light 4–6 hours before your local bedtime.
    - Shift meals and exercise routines earlier each day.
    """)
else:
    st.write("""
    - Expose yourself to bright light 4–6 hours before T_min each day.
    - Avoid light during the first 2–4 hours after waking.
    - Shift meals and exercise routines later each day.
    """)
