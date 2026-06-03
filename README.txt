Speed and SoC vs Time (Dual Line Chart)

import plotly.graph_objects as go

fig = go.Figure()

fig.add_trace(
    go.Scatter(
        x=df["timestamp"],
        y=df["vehicle_speed_kmph"],
        name="Speed (km/h)"
    )
)

fig.add_trace(
    go.Scatter(
        x=df["timestamp"],
        y=df["soc_percent"],
        name="SoC (%)",
        yaxis="y2"
    )
)

fig.update_layout(
    template="plotly_dark",
    title="Speed vs Battery Charge",
    yaxis=dict(title="Speed"),
    yaxis2=dict(
        title="SoC",
        overlaying="y",
        side="right"
    )
)

st.plotly_chart(fig, use_container_width=True)