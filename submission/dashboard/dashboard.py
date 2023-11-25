import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

# Import csv yang sudah dibersihkan
day_df = pd.read_csv("./cleaned_day.csv", parse_dates=["dteday"])
hour_df = pd.read_csv("./cleaned_hour.csv", parse_dates=["dteday"])

# Membuat title dan header
st.title("Proyek Analisis Data Dicoding")
st.header("Bike Sharing Dataset :bike:")

# Membuat filter waktu di sidebar
min_date = day_df["dteday"].min()
max_date = day_df["dteday"].max()
with st.sidebar:
    st.image("./bikelogo.jpg")
    start_date, end_date = st.date_input(
        label="Rentang Waktu",
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date],
    )

# Membuat dataframe yang sudah diintegrasi dengan filter waktu
main_day_df = day_df[
    (day_df["dteday"] >= str(start_date)) & (day_df["dteday"] <= str(end_date))
]
main_hour_df = hour_df[
    (hour_df["dteday"] >= str(start_date)) & (hour_df["dteday"] <= str(end_date))
]

# Rental Summary
st.subheader("Rental Summary")
col1, col2, col3 = st.columns(3)

with col1:
    casual_rental = main_day_df["casual"].sum()
    st.metric("Casual", value=casual_rental)

with col2:
    registered_rental = main_day_df["registered"].sum()
    st.metric("Registered", value=registered_rental)

with col3:
    total_rental = main_day_df["total_count"].sum()
    st.metric("Total Rental", value=total_rental)


# Explore #1: Weather Condition
st.subheader("Average Bike Rentals Based on Weather Condition")
daily_weather = main_day_df.groupby("weathersit")["total_count"].mean()
fig1 = plt.figure(figsize=(8, 6))
plt.bar(daily_weather.index, daily_weather, color=["r", "g", "b"])
plt.xlabel("Weather", size=15)
plt.xticks(rotation=0, size=12)

for i in range(len(daily_weather.index)):
    plt.text(i, daily_weather[i] * 1.01, round(daily_weather[i]), ha="center")

st.pyplot(fig1)


# Explore #2: Rental Trend (Hourly)
st.subheader("Average Bike Rentals Based on Hour")
new_cols = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday",
]
hourly = (
    main_hour_df.groupby(["hr", "weekday"])["total_count"]
    .mean()
    .unstack()
    .reindex(columns=new_cols)
)
fig2 = plt.figure(figsize=(8, 6))
for day in hourly.columns:
    plt.plot(hourly.index, hourly[day], label=day)
plt.xlabel("Hour")
plt.ylabel("Number of Bike Rentals")
plt.legend(title="Weekday", loc="best")
plt.xticks(range(24))
plt.grid(visible=True, linestyle="--")

st.pyplot(fig2)

st.caption("Copyright (c) Rivaldo 2023")
