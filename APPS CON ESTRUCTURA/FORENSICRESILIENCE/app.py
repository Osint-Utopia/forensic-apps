import streamlit as st
import pandas as pd
import datetime
import plotly.express as px
import os # To check if the file exists

# --- Configuration ---
DATA_FILE = "baby_tracker_data.csv"
st.set_page_config(page_title="Baby Tracker Deluxe", layout="wide", page_icon="👶")

# --- Data Handling Functions ---
def load_data():
    """Loads tracking data from CSV, creates file if it doesn't exist."""
    if os.path.exists(DATA_FILE):
        try:
            df = pd.read_csv(DATA_FILE, parse_dates=['Timestamp', 'Start Time', 'End Time'])
            # Ensure correct data types after loading
            df['Duration (min)'] = pd.to_numeric(df['Duration (min)'], errors='coerce')
            return df
        except pd.errors.EmptyDataError:
            # Handle empty file case
             return pd.DataFrame(columns=['Timestamp', 'Event Type', 'Details', 'Start Time', 'End Time', 'Duration (min)', 'Amount (ml/oz)', 'Food Type', 'Pee', 'Poo', 'Notes'])
        except Exception as e:
            st.error(f"Error loading data: {e}")
            # Return empty df on other errors to prevent app crash
            return pd.DataFrame(columns=['Timestamp', 'Event Type', 'Details', 'Start Time', 'End Time', 'Duration (min)', 'Amount (ml/oz)', 'Food Type', 'Pee', 'Poo', 'Notes'])

    else:
        # Create Dataframe with specific columns if file doesn't exist
        return pd.DataFrame(columns=['Timestamp', 'Event Type', 'Details', 'Start Time', 'End Time', 'Duration (min)', 'Amount (ml/oz)', 'Food Type', 'Pee', 'Poo', 'Notes'])


def save_data(df):
    """Saves the DataFrame to the CSV file."""
    try:
        df.to_csv(DATA_FILE, index=False)
    except Exception as e:
        st.error(f"Error saving data: {e}")

def add_entry(df, entry_data):
    """Adds a new entry dictionary to the DataFrame."""
    new_entry = pd.DataFrame([entry_data])
    df = pd.concat([df, new_entry], ignore_index=True)
    # Ensure Timestamp is datetime
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])
    return df.sort_values(by="Timestamp", ascending=False) # Keep most recent on top

# --- Load initial data ---
df = load_data()

# --- App Layout ---
st.title("👶 Baby Tracker Deluxe ✨")
st.markdown("Log your little one's daily adventures!")

tab1, tab2, tab3 = st.tabs(["📊 Dashboard", "📝 Log New Entry", "📜 View Full Log"])

# --- Tab 1: Dashboard ---
with tab1:
    st.header("📊 Quick Overview")

    if df.empty:
        st.info("No data logged yet. Add some entries in the 'Log New Entry' tab!")
    else:
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("😴 Recent Sleep")
            sleep_df = df[df['Event Type'] == 'Sleep'].copy() # Use copy to avoid SettingWithCopyWarning
            if not sleep_df.empty:
                 # Convert duration to numeric, coercing errors
                sleep_df['Duration (min)'] = pd.to_numeric(sleep_df['Duration (min)'], errors='coerce')
                # Drop rows where duration couldn't be converted (NaN)
                sleep_df.dropna(subset=['Duration (min)'], inplace=True)

                if not sleep_df.empty:
                    # Ensure 'Start Time' is datetime before formatting
                    sleep_df['Start Time'] = pd.to_datetime(sleep_df['Start Time'])
                    sleep_df['Date'] = sleep_df['Start Time'].dt.strftime('%Y-%m-%d') # Group by day
                    daily_sleep = sleep_df.groupby('Date')['Duration (min)'].sum().reset_index()
                    daily_sleep.rename(columns={'Duration (min)': 'Total Sleep (min)'}, inplace=True)

                    fig_sleep = px.bar(daily_sleep.tail(10), # Show last 10 days
                                       x='Date',
                                       y='Total Sleep (min)',
                                       title="Total Daily Sleep (Last 10 Days)",
                                       labels={'Total Sleep (min)': 'Total Sleep (minutes)'})
                    fig_sleep.update_layout(xaxis_title="Date", yaxis_title="Total Sleep (minutes)")
                    st.plotly_chart(fig_sleep, use_container_width=True)
                else:
                    st.write("No valid sleep duration data to display.")

            else:
                st.write("No sleep entries logged yet.")


        with col2:
            st.subheader("🍼 Recent Feedings")
            food_df = df[df['Event Type'] == 'Food'].copy()
            if not food_df.empty:
                 # Ensure 'Amount (ml/oz)' is numeric, coercing errors
                food_df['Amount (ml/oz)'] = pd.to_numeric(food_df['Amount (ml/oz)'], errors='coerce')
                food_df.dropna(subset=['Food Type'], inplace=True) # Need food type for pie chart

                if not food_df.empty:
                    # Pie chart for food types
                    food_type_counts = food_df['Food Type'].value_counts().reset_index()
                    food_type_counts.columns = ['Food Type', 'Count'] # Rename columns for Plotly
                    fig_food_type = px.pie(food_type_counts,
                                           names='Food Type',
                                           values='Count',
                                           title="Feeding Type Distribution",
                                           hole=0.3) # Donut chart style
                    st.plotly_chart(fig_food_type, use_container_width=True)

                    # Optional: Bar chart for amount per day (if amounts are logged)
                    food_df_amount = food_df.dropna(subset=['Amount (ml/oz)', 'Timestamp'])
                    if not food_df_amount.empty:
                        food_df_amount['Date'] = pd.to_datetime(food_df_amount['Timestamp']).dt.strftime('%Y-%m-%d')
                        daily_amount = food_df_amount.groupby('Date')['Amount (ml/oz)'].sum().reset_index()
                        daily_amount.rename(columns={'Amount (ml/oz)': 'Total Amount'}, inplace=True)
                        fig_food_amount = px.bar(daily_amount.tail(10),
                                                 x='Date',
                                                 y='Total Amount',
                                                 title="Total Daily Feed Amount (Last 10 Days)",
                                                 labels={'Total Amount': 'Total Amount (ml/oz)'})
                        st.plotly_chart(fig_food_amount, use_container_width=True)

                else:
                    st.write("No valid feeding data to display.")

            else:
                st.write("No feeding entries logged yet.")

        # Add more charts here (e.g., diaper counts, activity types) if desired

# --- Tab 2: Log New Entry ---
with tab2:
    st.header("📝 Log a New Event")

    current_time = datetime.datetime.now().time()
    current_date = datetime.datetime.now().date() # Use current date by default

    # --- Sleep Log ---
    with st.expander("😴 Log Sleep"):
        sleep_start_time = st.time_input("Start Time", value=current_time, key="sleep_start")
        sleep_end_time = st.time_input("End Time", value=current_time, key="sleep_end")
        sleep_date = st.date_input("Date", value=current_date, key="sleep_date")
        sleep_notes = st.text_area("Sleep Notes", key="sleep_notes")

        if st.button("Log Sleep Entry", key="log_sleep"):
             # Combine date and time
            start_dt = datetime.datetime.combine(sleep_date, sleep_start_time)
            end_dt = datetime.datetime.combine(sleep_date, sleep_end_time)

             # Handle overnight sleep or end time before start time
            if end_dt <= start_dt:
                 # Assume it ended the next day or handle potential input error
                 # Simple approach: Add a day if end time is earlier
                 # More robust: Ask user if it crossed midnight
                 st.warning("End time is before start time. Assuming end time is on the next day if start time is late. Please verify calculation.")
                 # Basic check: if start is PM and end is AM, likely next day
                 if start_dt.hour >= 12 and end_dt.hour < 12:
                     end_dt += datetime.timedelta(days=1)
                 elif end_dt < start_dt: # If still less, maybe input error or same day short nap?
                     st.error("End time cannot be before start time on the same day. Please correct.")
                     # Optionally prevent logging here
                     st.stop() # Stop execution for this entry if invalid


            duration = end_dt - start_dt
            duration_min = round(duration.total_seconds() / 60)

            entry = {
                "Timestamp": datetime.datetime.now(),
                "Event Type": "Sleep",
                "Start Time": start_dt,
                "End Time": end_dt,
                "Duration (min)": duration_min,
                "Notes": sleep_notes,
                "Details": f"{duration_min} minutes", # Simple detail string
                 # Add NaN/None for columns not relevant to this event type
                "Amount (ml/oz)": None, "Food Type": None, "Pee": None, "Poo": None,
            }
            df = add_entry(df, entry)
            save_data(df)
            st.success(f"😴 Sleep entry logged for {duration_min} minutes!")
            st.rerun() # Rerun to update dashboard/log view immediately


    # --- Food Log ---
    with st.expander("🍼 Log Feeding"):
        food_time = st.time_input("Feeding Time", value=current_time, key="food_time")
        food_date = st.date_input("Feeding Date", value=current_date, key="food_date")
        food_type = st.selectbox("Food Type", ["Breast Milk", "Formula", "Solids", "Water", "Other"], key="food_type")
        food_amount = st.number_input("Amount (ml/oz)", min_value=0.0, step=1.0, key="food_amount", format="%.1f")
        food_notes = st.text_area("Feeding Notes", key="food_notes")

        if st.button("Log Feeding Entry", key="log_food"):
            entry_time = datetime.datetime.combine(food_date, food_time)
            entry = {
                "Timestamp": entry_time, # Use feeding time as main timestamp
                "Event Type": "Food",
                "Food Type": food_type,
                "Amount (ml/oz)": food_amount if food_amount > 0 else None, # Store None if 0
                "Notes": food_notes,
                "Details": f"{food_type} - {food_amount if food_amount > 0 else 'N/A'} ml/oz",
                # Add NaN/None for columns not relevant
                "Start Time": None, "End Time": None, "Duration (min)": None, "Pee": None, "Poo": None,
            }
            df = add_entry(df, entry)
            save_data(df)
            st.success(f"🍼 {food_type} entry logged!")
            st.rerun()

    # --- Diaper Log ---
    with st.expander("💩 Log Diaper Change"):
        diaper_time = st.time_input("Diaper Time", value=current_time, key="diaper_time")
        diaper_date = st.date_input("Diaper Date", value=current_date, key="diaper_date")
        pee = st.checkbox("Pee 💧", key="diaper_pee")
        poo = st.checkbox("Poo 💩", key="diaper_poo")
        diaper_notes = st.text_area("Diaper Notes", key="diaper_notes")

        if st.button("Log Diaper Entry", key="log_diaper"):
            if not pee and not poo:
                st.warning("Please select at least 'Pee' or 'Poo' for the diaper change.")
            else:
                entry_time = datetime.datetime.combine(diaper_date, diaper_time)
                details = []
                if pee: details.append("Pee")
                if poo: details.append("Poo")
                entry = {
                    "Timestamp": entry_time,
                    "Event Type": "Diaper",
                    "Pee": pee,
                    "Poo": poo,
                    "Notes": diaper_notes,
                    "Details": " & ".join(details),
                    # Add NaN/None for columns not relevant
                    "Start Time": None, "End Time": None, "Duration (min)": None, "Amount (ml/oz)": None, "Food Type": None,
                }
                df = add_entry(df, entry)
                save_data(df)
                st.success(f"💩 Diaper change ({' & '.join(details)}) logged!")
                st.rerun()

    # --- Activity Log ---
    with st.expander("🤸 Log Activity"):
        activity_time = st.time_input("Activity Time", value=current_time, key="activity_time")
        activity_date = st.date_input("Activity Date", value=current_date, key="activity_date")
        activity_type = st.text_input("Activity Type (e.g., Tummy time, Play, Bath)", key="activity_type")
        activity_notes = st.text_area("Activity Notes", key="activity_notes")

        if st.button("Log Activity Entry", key="log_activity"):
            if not activity_type:
                st.warning("Please enter an activity type.")
            else:
                entry_time = datetime.datetime.combine(activity_date, activity_time)
                entry = {
                    "Timestamp": entry_time,
                    "Event Type": "Activity",
                    "Details": activity_type,
                    "Notes": activity_notes,
                     # Add NaN/None for columns not relevant
                    "Start Time": None, "End Time": None, "Duration (min)": None, "Amount (ml/oz)": None, "Food Type": None, "Pee": None, "Poo": None,
                }
                df = add_entry(df, entry)
                save_data(df)
                st.success(f"🤸 Activity '{activity_type}' logged!")
                st.rerun()

    # --- Screen Time Log ---
    with st.expander("📺 Log Screen Time"):
        screen_start_time = st.time_input("Start Time", value=current_time, key="screen_start")
        screen_end_time = st.time_input("End Time", value=current_time, key="screen_end")
        screen_date = st.date_input("Date", value=current_date, key="screen_date")
        screen_notes = st.text_area("Screen Time Notes (e.g., show watched)", key="screen_notes")

        if st.button("Log Screen Time Entry", key="log_screen"):
            start_dt = datetime.datetime.combine(screen_date, screen_start_time)
            end_dt = datetime.datetime.combine(screen_date, screen_end_time)

            if end_dt <= start_dt:
                 st.error("Screen time end time cannot be before or same as start time. Please correct.")
                 st.stop()

            duration = end_dt - start_dt
            duration_min = round(duration.total_seconds() / 60)

            entry = {
                "Timestamp": datetime.datetime.now(), # Log time is now, but track start/end
                "Event Type": "Screen Time",
                "Start Time": start_dt,
                "End Time": end_dt,
                "Duration (min)": duration_min,
                "Notes": screen_notes,
                "Details": f"{duration_min} minutes",
                 # Add NaN/None for columns not relevant
                "Amount (ml/oz)": None, "Food Type": None, "Pee": None, "Poo": None,
            }
            df = add_entry(df, entry)
            save_data(df)
            st.success(f"📺 Screen time entry logged for {duration_min} minutes!")
            st.rerun() # Rerun to update


# --- Tab 3: View Full Log ---
with tab3:
    st.header("📜 Full Event Log")
    st.info("You can sort columns by clicking the headers.")

    if df.empty:
        st.warning("No data logged yet.")
    else:
        # Improve display: format timestamp, select/reorder columns
        display_df = df.copy()
        # Format timestamp for better readability
        display_df['Timestamp'] = display_df['Timestamp'].dt.strftime('%Y-%m-%d %H:%M:%S')
        # Format Start/End times if they exist
        for col in ['Start Time', 'End Time']:
            if col in display_df.columns:
                 # Check if column has datetime objects before trying to format
                if pd.api.types.is_datetime64_any_dtype(display_df[col]):
                    display_df[col] = display_df[col].dt.strftime('%H:%M')
                else:
                    # Handle cases where it might be loaded as string or object, attempt conversion
                    try:
                         display_df[col] = pd.to_datetime(display_df[col], errors='coerce').dt.strftime('%H:%M')
                    except Exception:
                         pass # Keep original if conversion fails


        # Select and reorder columns for display
        display_columns = ['Timestamp', 'Event Type', 'Details', 'Duration (min)', 'Amount (ml/oz)', 'Food Type', 'Pee', 'Poo', 'Notes', 'Start Time', 'End Time']
        # Filter out columns that might not exist if the file was created before they were added
        display_columns = [col for col in display_columns if col in display_df.columns]

        st.dataframe(display_df[display_columns], use_container_width=True)

    st.markdown("---")
    st.subheader("Manage Data")
    if st.button("🚨 Clear All Data 🚨"):
        # Add a confirmation step
        confirm = st.checkbox("Check this box to confirm you want to delete ALL data. This cannot be undone.")
        if confirm:
            df = pd.DataFrame(columns=df.columns) # Create empty dataframe with same columns
            save_data(df)
            st.success("All data has been cleared.")
            # Force a rerun to update the view immediately
            st.rerun()
        else:
            st.warning("Clear data operation cancelled. Check the box to confirm.")