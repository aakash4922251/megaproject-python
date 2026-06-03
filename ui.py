'''
Run with:
    python -m streamlit run ui.py
currently using bms_data.csv until actual dataset is approved
'''

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

st.set_page_config(layout="wide") #make Streamlit wider
sns.set_style("darkgrid") #graph will have grid lines
plt.rcParams["font.size"] = 10 #larger text for visiblity everywhere 

# st.title("EV BMS Data Analysis")
st.markdown(
    """
<h1 style = 'text-align: center; color: gray;'>
Battery Management System 
</h1>

<h4 style = 'text-align: center; color: gray;'>
Battery Analytics System
</h4>
""",
unsafe_allow_html=True
)

# df = pd.read_csv("data/bms_data.csv")
df = pd.read_csv("data/BMWi3_22kWh_24h_battery_timeline.csv", sep="\t")
# df.columns=df.columns.str.strip()
# st.write(df.columns.tolist())

latest = df.iloc[-1] #latest battery reading
# st.write(latest) #error checking
soc = latest["soc_percent"]
voltage = latest["battery_voltage_v"]
temp = latest["battery_temp_c"]
soh = latest["soh_percent"]
state = latest["state"]

#Vehicle Details
st.subheader("Vehicle Details")
col1, col2 = st.columns(2)
col1.metric("Vehicle Model","BMW I3")
col2.metric("Vehicle Owner Name","Ijaz MD")
st.markdown("---")

st.subheader("Current Battery Status")
col1, col2, col3, col4  = st.columns(4) #create 4 columns
col1.metric("Battery SOC", f"{latest['soc_percent']}%")
col2.metric("Voltage", f"{latest['battery_voltage_v']} V")
col3.metric("Temperature", f"{latest['battery_temp_c']} °C")
col4.metric("Battery Health", f"{latest['soh_percent']}%")

# df = pd.read_csv("data/bms_data.csv")
df["timestamp"] = pd.to_datetime(df["timestamp"]) #This converts text time into real datetime objects.


#ALERT SYSTEM
st.subheader("Battery Condition")

def check_temperature(temp):
    if temp > 50:
        return"Critical"
    elif temp > 40:
        return"Warning"
    else:
        return"Normal"

status = check_temperature(temp)

if status == "Critical":
    st.error("Temperature status: Critical")
if status == "Warning":
    st.warning("Temperature status: Warning")
if status == "Normal":
    st.success("Temperature status: Normal")


alerts = []
if temp > 40:
    alerts.append("High Battery Temperature")

if soc<20:
    alerts.append("Low State of Charge")

if soh<80:
    alerts.append("Battery Health Warning")

for alert in alerts:
    st.write(alert)

if alerts:
    for alert in alerts:
        st.error(alert)
else:
    st.success("No Active Alerts")


# #Un Comment this Line of code to show indiduval Charts
# # SOC Trend Chart
# st.subheader("Battery SOC Trend")

# fig4, ax = plt.subplots(figsize = (10,4))

# sns.lineplot(data = df,
#             x = "timestamp",
#             y = "soc",
#             marker = "o",
#             color = "green",
#             ax = ax
#             )

# ax.set_title("State of Charge Over Time")
# ax.set_xlabel("Time")
# ax.set_ylabel("SOC(%)")

# st.pyplot(fig4)

# # Voltage trend
# st.subheader("Battery Voltage Trend")

# fig2, ax2 = plt.subplots(figsize = (10,4))

# sns.lineplot(data = df,
#              x = "timestamp",
#              y = "voltage",
#              marker = "o",
#              color = "blue",
#              ax = ax2
#              )

# ax2.set_title("Voltage Over Time")
# ax2.set_xlabel("Time")
# ax2.set_ylabel("Voltage (V)")

# st.pyplot(fig2)

# # Temperature Trend
# st.subheader("Battery Temperature Trend")

# fig3, ax3 = plt.subplots(figsize = (10,4))

# sns.lineplot( data = df,
#              x = "timestamp",
#              y = "temperature",
#              marker = "o",
#              color = "red",
#              ax = ax3
#              )

# ax3.set_title("Temperature Over Time")
# ax3.set_xlabel("Time")
# ax3.set_ylabel("Temperature (°C)")

# st.pyplot(fig3)

# # Current Trend
# st.subheader("Battery Current Trend")

# fig4, ax4 = plt.subplots(figsize=(10, 4))

# sns.lineplot( data = df,
#             x = "timestamp",
#             y = "current",
#             marker = "o",
#             color = "orange",
#             ax = ax4
#             )

# ax4.set_title("Current Over Time")
# ax4.set_xlabel("Time")
# ax4.set_ylabel("Current (A)")

# st.pyplot(fig4)



# # Analystics Dashboard using seaborn and matplotlib
# st.subheader("Battery Analystics Dashboard")

# fig, axes = plt.subplots(2, 2, figsize = (15, 10))

# # SOC Chart
# sns.lineplot(
#     data=df,
#     x="timestamp",
#     y="soc_percent",
#     marker="o",
#     color="green",
#     ax=axes[0, 0]
# )

# axes[0, 0].set_title("SOC Trend")
# axes[0, 0].set_ylabel("SOC (%)")

# # Volatage Chart
# sns.lineplot(
#     data=df,
#     x="timestamp",
#     y="battery_voltage_v",
#     marker="o",
#     color="blue",
#     ax=axes[0, 1]
# )

# axes[0, 1].set_title("Voltage Trend")
# axes[0, 1].set_ylabel("Voltage (V)")

# # Temperature Chart
# sns.lineplot(
#     data=df,
#     x="timestamp",
#     y="battery_temp_c",
#     marker="o",
#     color="red",
#     ax=axes[1, 0]
# )

# axes[1, 0].set_title("Temperature Trend")
# axes[1, 0].set_ylabel("Temperature (°C)")

# # Current Chart
# sns.lineplot(
#     data=df,
#     x="timestamp",
#     y="battery_current_a",
#     marker="o",
#     color="orange",
#     ax=axes[1, 1]
# )

# axes[1, 1].set_title("Current Trend")
# axes[1, 1].set_ylabel("Current (A)")

# plt.tight_layout() #title with overlap axis, good spacing
# st.pyplot(fig) #display chart in streamlit



#BATTERY PERFORMANCE TRENDS DASHBOARD USING PLOTLY
# import plotly.subplots.make_subplots()

#Charging Behvaior
st.subheader("CHARGING BEHAVIOR")
charging_df = df[df["state"] == "Charging"]
# st.dataframe(charging_df)

col1, col2 = st.columns(2)
#charging hours 
charging_hours = len(charging_df)*10/3600 #in hours
col1.metric("Total Charging Time", f"{charging_hours:.2f} Hours") #why 2f

#Total Charge Added
starting_soc = charging_df["soc_percent"].iloc[0]
ending_soc = charging_df["soc_percent"].iloc[-1]
soc_gain = ending_soc - starting_soc
col2.metric("Charge Added", f"{soc_gain:.1f}%")

#SoC During Charging Plot
fig = px.line(
    charging_df,
    x = "timestamp",
    y = "soc_percent",
    title = "State of Charge During Charging"
)
st.plotly_chart(fig, use_container_width=True)

#Charging Power Trend
fig = px.line(
    charging_df,
    x = "timestamp",
    y = "power_kw",
    title = "Charging Power"
)
st.plotly_chart(fig, use_container_width=True)

#Charging Temperature
fig = px.line(
    charging_df,
    x = "timestamp",
    y = "battery_temp_c",
    title = "Battery Temperature During Charging"
)
st.plotly_chart(fig, use_container_width=True)

#Speed vs Battery Charge
fig = px.scatter(
    df,
    x = "vehicle_speed_kmph",
    y = "soc_percent",
    title = "Vehicle speed vs State of Charge",
    template="plotly_dark"
)
st.plotly_chart(fig, use_container_width=True)

# from plotly.subplots import make_subplots
# import plotly.graph_objects as go

# fig = make_subplots(
#     rows = 2,
#     cols = 2,
#     subplot_titles=(
#         "SoC During Charging",
#         "Charging Power",
#         "Battery Temperature",
#         "Speed vs Battery Charge"
#     )
# )

# #SoC During Charging
# fig.add_trace(
#     go.scatter(
#         x = charging_df["timestamp"],
#         y = charging_df["soc_percent"],
#         mode = "lines",
#         name = "SoC"
#     ),
#     row = 1,
#     col = 1
# )

# #Charging Power
# fig.add_trace(
#     go.scatter(
#         x = charging_df["timestamp"],
#         y = charging_df["power_kw"],
#         mode = "lines",
#         name = "Power"
#     ),
#     row = 1,
#     col = 2
# )

# #Battery temperature
# fig.add_trace(
#     go.scatter(
#         x = charging_df["timestamp"],
#         y = charging_df["battery_temp_c"],
#         mode = "lines",
#         name = "Temperature"
#     ),
#     row = 2,
#     col = 1
# )

# #Speed Vs SoC
# fig.add_trace(
#     go.scatter(
#         x = df["vehicle_speed_kmph"],
#         y = df["soc_percent"],
#         mode = "markers",
#         name = "Speed vs SoC"
#     ),
#     row = 2,
#     col = 2
# )




# show battery data
st.header("Battery Data Information")
st.dataframe(df)

st.markdown("---")

#Caption at the end 
st.caption(
    "EV Battery Management System Analytics Platform"
)