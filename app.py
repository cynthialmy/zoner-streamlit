import streamlit as st
import pandas as pd
import datetime as dt

st.title("Zoner: Personalized Jet Lag Adjustment Planner")

# --- Inputs ---
st.header("🌐 Input Your Travel Details")
direction = st.selectbox("Travel Direction", ["East (Advance Clock)", "West (Delay Clock)"])
bedtime_current = st.time_input("Current Bedtime (Home Time Zone)", value=dt.time(23, 0))
wake_current = st.time_input("Current Wake-Up Time (Home Time Zone)", value=dt.time(7, 0))
bedtime_local = st.time_input("Target Bedtime (Destination Time Zone)", value=dt.time(22, 0))
wake_local = st.time_input("Target Wake-Up Time (Destination Time Zone)", value=dt.time(6, 0))
time_shift = st.number_input("Total Hours to Shift (e.g., 6 for 6-hour shift)", min_value=1, max_value=12, value=6)
days_available = st.number_input("Number of Days for Adjustment", min_value=1, max_value=7, value=3)

# --- Calculations ---
# Calculate T_min
wake_current_dt = dt.datetime.combine(dt.date.today(), wake_current)
t_min = wake_current_dt - dt.timedelta(minutes=90)
st.write(f"T_min: {t_min.time()} (90 minutes before wake-up)")

# Time shift per day
shift_per_day = time_shift / days_available

# Adjustment Logic
schedule = []

for day in range(1, days_available + 1):
    if direction == "East (Advance Clock)":
        # Advance schedule
        bedtime_current_dt = dt.datetime.combine(dt.date.today(), bedtime_current)
        wake_current_dt = dt.datetime.combine(dt.date.today(), wake_current)
        t_min_dt = dt.datetime.combine(dt.date.today(), t_min.time())
        bedtime_local_dt = dt.datetime.combine(dt.date.today(), bedtime_local)

        bedtime_new = bedtime_current_dt - dt.timedelta(hours=shift_per_day * day)
        wake_new = wake_current_dt - dt.timedelta(hours=shift_per_day * day)
        light_time_start = t_min_dt + dt.timedelta(hours=2)
        light_time_end = t_min_dt + dt.timedelta(hours=4)
        melatonin_time = bedtime_local_dt - dt.timedelta(hours=2)
    else:
        # Delay schedule
        bedtime_current_dt = dt.datetime.combine(dt.date.today(), bedtime_current)
        wake_current_dt = dt.datetime.combine(dt.date.today(), wake_current)
        t_min_dt = dt.datetime.combine(dt.date.today(), t_min.time())
        bedtime_local_dt = dt.datetime.combine(dt.date.today(), bedtime_local)

        bedtime_new = bedtime_current_dt + dt.timedelta(hours=shift_per_day * day)
        wake_new = wake_current_dt + dt.timedelta(hours=shift_per_day * day)
        light_time_start = t_min_dt - dt.timedelta(hours=6)
        light_time_end = t_min_dt - dt.timedelta(hours=4)
        melatonin_time = bedtime_local_dt - dt.timedelta(hours=6)

    # Append to schedule
    schedule.append({
        "Day": day,
        "New Bedtime": bedtime_new.time(),
        "New Wake-Up": wake_new.time(),
        "Light Start": light_time_start.time(),
        "Light End": light_time_end.time(),
        "Melatonin Time": melatonin_time.time()
    })

# Convert schedule to DataFrame
schedule_df = pd.DataFrame(schedule)

# --- Display Schedule ---
st.header("📅 Personalized Adjustment Schedule")
st.write("Adjust your circadian rhythm day-by-day based on your travel details:")
st.dataframe(schedule_df)

# --- Additional Tips ---
st.header("💡 Helpful Tips")
if direction == "East (Advance Clock)":
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
