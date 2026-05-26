'''
Run with:
    python -m streamlit run ui.py
currently using bms_data.csv until actual dataset is approved
'''

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# st.set_page_config(layout="wide") #make Streamlit wider
sns.set_style("darkgrid")
plt.rcParams["font.size"] = 10 #larger text for visiblity

# st.title("EV BMS Data Analysis")
st.markdown(
    """
<h1 style = 'text-align: center; color: gray;'>
Battery Management System 
</h1>

<h4 style = 'text-align: center; color: gray;'>
Real-Time Battery Analytics System
</h4>
""",
unsafe_allow_html=True
)

df = pd.read_csv("data/bms_data.csv")

# show battery data
st.header("Battery Data")
st.dataframe(df)

latest = df.iloc[-1] #latest battery reading
print(latest)

st.subheader("Live Battery Status")
col1, col2, col3, col4  = st.columns(4)
col1.metric("Battery SOC", f"{latest['soc']}%")
col2.metric("Volatge", f"{latest['voltage']} V")
col3.metric("Temperature", f"{latest['temperature']} °C")
col4.metric("Battery Health", f"{latest['soh']}%")

df = pd.read_csv("data/bms_data.csv")
df["timestamp"] = pd.to_datetime(df["timestamp"]) #This converts text time into real datetime objects.



# #Un Comment this Line of code to show indivual Charts
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



# Analystics Dashboard 
st.subheader("Battery Analystics Dashboard")

fig, axes = plt.subplots(2, 2, figsize = (15, 10))

# SOC Chart
sns.lineplot(
    data = df,
    x = "timestamp",
    y = "soc",
    marker = "o",
    color = "green",
    ax = axes[0, 0]
)

axes[0, 0].set_title("SOC Trend")
axes[0, 0].set_ylabel("SOC (%)")

# Volatage Chart
sns.lineplot(
    data = df,
    x = "timestamp",
    y = "voltage",
    marker = "o",
    color = "blue",
    ax = axes[0, 1]
)

axes[0, 1].set_title("Voltage Trend")
axes[0, 1].set_ylabel("Voltage (V)")

# Temperature Chart
sns.lineplot(
    data = df,
    x = "timestamp",
    y = "temperature",
    marker = "o",
    color = "red",
    ax = axes[1, 0]
)

axes[1, 0].set_title("Temperature Trend")
axes[1, 0].set_ylabel("Temperature (°C)")

# Current Chart
sns.lineplot(
    data = df,
    x = "timestamp",
    y = "current",
    marker = "o",
    color = "orange",
    ax = axes[1, 1]
)

axes[1, 1].set_title("Current Trend")
axes[1, 1].set_ylabel("Current (A)")

plt.tight_layout()
st.pyplot(fig)

