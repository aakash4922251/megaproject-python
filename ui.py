'''
Run with:
    python -m streamlit run ui.py
currently using bms_data.csv until actual dataset is approved
'''

import streamlit as st
import pandas as pd
# import matplotlib.pyplot as plt
# import seaborn as sns
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go


st.set_page_config(layout="wide") #make Streamlit wider
# sns.set_style("darkgrid") #graph will have grid lines
# plt.rcParams["font.size"] = 10 #larger text for visiblity everywhere 

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

#VEHICLE DETAILS
st.subheader("Vehicle Information")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Vehicle", "BMW i3")
    st.metric("Battery Capacity", "22 kWh")

with col2:
    st.metric("Battery Rating", "60 Ah")
    st.metric("Battery Type", "Li-Ion")

with col3:
    st.metric("Owner Name:", "Name")

st.markdown("---")

# #VEHICLE DETAILS
# st.subheader("Vehicle Information")
# st.info(
#     '''
# **Vehicle:** BMW i3
# **Battery Capacity:** 22 kWh
# **Battery Rating:** 60 Ah
# **Battery Type:** Li-Ion
# **Owner:** Name'''
# )

# st.markdown("---")

st.subheader("Current Battery Status")
col1, col2, col3, col4  = st.columns(4) #create 4 columns
col1.metric("Battery SOC", f"{latest['soc_percent']}%")
col2.metric("Voltage", f"{latest['battery_voltage_v']} V")
col3.metric("Temperature", f"{latest['battery_temp_c']} °C")
col4.metric("Battery Health", f"{latest['soh_percent']}%")
st.markdown("---")

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

st.markdown("---")

# Battery Performance Trends
st.subheader("Battery Performance Trends")

# SoC vs Time
fig_soc = px.scatter(
    df,
    x="timestamp",
    y="soc_percent",
    title="State of Charge (%)",
    template="plotly_dark",
    color_discrete_sequence=["#636EFA"]
)
st.plotly_chart(fig_soc, use_container_width=True)

# Voltage vs Time
fig_voltage = px.scatter(
    df,
    x="timestamp",
    y="battery_voltage_v",
    title="Battery Voltage (V)",
    template="plotly_dark",
    color_discrete_sequence=["#EF553B"]
)
st.plotly_chart(fig_voltage, use_container_width=True)

# Temperature vs Time
fig_temp = px.scatter(
    df,
    x="timestamp",
    y="battery_temp_c",
    title="Battery Temperature (°C)",
    template="plotly_dark",
    color_discrete_sequence=["#00CC96"]
)
st.plotly_chart(fig_temp, use_container_width=True)

# Current vs Time
fig_current = px.scatter(
    df,
    x="timestamp",
    y="battery_current_a",
    title="Battery Current (A)",
    template="plotly_dark",
    color_discrete_sequence=["#AB63FA"]
)
st.plotly_chart(fig_current, use_container_width=True)


# # SLIDER MECHANISM - ON HOLD 
# view = st.radio(
#     "Select Time Resolution",
#     ["10 Seconds", "10 Minutes", "1 Hour"],
#     horizontal=True
# )

# df_10s = df.copy()
# df_10m = (
#     df.set_index("timestamp")
#     .resample("10min")
#     .mean(numeric_only=True)
#     .reset_index()
# )
# df_1h = (
#     df.set_index("timestamp")
#     .resample("1h")
#     .mean(numeric_only=True)
#     .reset_index()
# )

# if view == "10 Seconds":
#     plot_df = df_10s
# elif view == "10 Minutes":
#     plot_df = df_10m
# else:
#     plot_df = df_1h

# fig = px.line(
#     plot_df,
#     x = "timestamp",
#     y = "soc_percent",
#     title = "State of Charge (%)",
#     template = "plotly_dark"
# )

# fig.update_layout(
#     xaxis = dict(
#         rangeslider = dict(
#             visible = True
#         )
#     )
# )

# st.plotly_chart(
#     fig,
#     use_container_width=True
# )

#2x2 Battery Performace Trends  
st.subheader("Battery Performace at a Glance")

fig = make_subplots(
    rows=2,
    cols=2,
    subplot_titles=(
        "State of Charge (%)",
        "Battery Voltage (V)",
        "Battery Temperture (°C)",
        "Battery Current (A)"
    )
)

#SoC Graph
fig.add_trace(
    go.Scatter(
        x = df["timestamp"],
        y = df["soc_percent"],
        mode = "lines",
        name = "SoC"
    ),
    row=1,
    col=1
    )

#Voltage Graph
fig.add_trace(
    go.Scatter(
        x = df["timestamp"],
        y = df["battery_voltage_v"],
        mode = "lines",
        name = "Voltage"
    ),
    row=1,
    col=2
    )

#Temperature Graph
fig.add_trace(
    go.Scatter(
        x = df["timestamp"],
        y = df["battery_temp_c"],
        mode = "lines",
        name = "Tempertaure"
    ),
    row=2,
    col=1
    )

#Current Graph
fig.add_trace(
    go.Scatter(
        x = df["timestamp"],
        y = df["battery_current_a"],
        mode = "lines",
        name = "Current"
    ),
    row=2,
    col=2
    ) 

#Format
fig.update_layout(
    template = "plotly_dark",
    height = 800,
    showlegend = False,
    title = "Battery Performance Trends "
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.markdown("---")

#BATTERY PERFORMANCE TRENDS DASHBOARD USING PLOTLY
# import plotly.subplots.make_subplots()

# #Charging Behvaior
# st.subheader("CHARGING BEHAVIOR")
# charging_df = df[df["state"] == "Charging"]
# # st.dataframe(charging_df)

# col1, col2 = st.columns(2)
# #charging hours 
# charging_hours = len(charging_df)*10/3600 #in hours
# col1.metric("Total Charging Time", f"{charging_hours:.2f} Hours") #why 2f

# #Total Charge Added
# starting_soc = charging_df["soc_percent"].iloc[0]
# ending_soc = charging_df["soc_percent"].iloc[-1]
# soc_gain = ending_soc - starting_soc
# col2.metric("Charge Added", f"{soc_gain:.1f}%")

# #SoC During Charging Plot
# fig = px.line(
#     charging_df,
#     x = "timestamp",
#     y = "soc_percent",
#     title = "State of Charge During Charging"
# )
# st.plotly_chart(fig, use_container_width=True)

# #Charging Power Trend
# fig = px.line(
#     charging_df,
#     x = "timestamp",
#     y = "power_kw",
#     title = "Charging Power"
# )
# st.plotly_chart(fig, use_container_width=True)

# #Charging Temperature
# fig = px.line(
#     charging_df,
#     x = "timestamp",
#     y = "battery_temp_c",
#     title = "Battery Temperature During Charging"
# )
# st.plotly_chart(fig, use_container_width=True)

# #Speed vs Battery Charge
# fig = px.scatter(
#     df,
#     x = "vehicle_speed_kmph",
#     y = "soc_percent",
#     title = "Vehicle speed vs State of Charge",
#     template="plotly_dark"
# )
# st.plotly_chart(fig, use_container_width=True)

#Charging Behaviour 
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

fig = make_subplots(
    rows = 2,
    cols = 2,
    subplot_titles=(
        "SoC During Charging",
        "Charging Power",
        "Battery Temperature",
        "Speed vs Battery Charge"
    )
)

#SoC During Charging
fig.add_trace(
    go.Scatter(
        x = charging_df["timestamp"],
        y = charging_df["soc_percent"],
        mode = "lines",
        name = "SoC"
    ),
    row = 1,
    col = 1
)

#Charging Power
fig.add_trace(
    go.Scatter(
        x = charging_df["timestamp"],
        y = charging_df["power_kw"],
        mode = "lines",
        name = "Power"
    ),
    row = 1,
    col = 2
)

#Battery temperature
fig.add_trace(
    go.Scatter(
        x = charging_df["timestamp"],
        y = charging_df["battery_temp_c"],
        mode = "lines",
        name = "Temperature"
    ),
    row = 2,
    col = 1
)

#Speed Vs SoC
fig.add_trace(
    go.Scatter(
        x = df["vehicle_speed_kmph"],
        y = df["soc_percent"],
        mode = "markers",
        name = "Speed vs SoC"
    ),
    row = 2,
    col = 2
)

#final layout 
fig.update_layout(
    template = "plotly_dark",
    height = 800,
    showlegend = False,
    title = "Charging Behaviour Charts"
)

st.plotly_chart(
    fig, 
    use_container_width=True
)

st.markdown("---")


#OPERATING STATE DISTRIBUTION
st.subheader("Operating State Distribution")

state_counts = df["state"].value_counts()

fig = px.pie(
    values = state_counts.values,
    names = state_counts.index,
    hole = 0.4,
    title = "Operating State Distribution",
    template = "plotly_dark"
)

fig.update_traces(
    textinfo = "percent + label"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# show battery data
st.header("Battery Data Information")
st.dataframe(df)

st.markdown("---")

#Caption at the end 
st.caption(
    "EV Battery Management System Analytics Platform"
)