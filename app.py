import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from math import ceil

def draw_graph(df, break_even, needed_funding):

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=[df['Month'].iloc[-1]/2],
        y=[df['Expenses'].mean()/2],
        mode='text',
        text=f'Needed Funding: {needed_funding:.2f} EUR',
        name='Funding',
        showlegend=False
    ))

    fig.add_trace(go.Scatter(
        x=df['Month'],
        y=df['Expenses'],
        line=dict(
            width=3,
            color='red'
        ),
        name='Expenses'
    ))

    fig.add_trace(go.Scatter(
        x=df['Month'],
        y=df['Revenue'],
        line=dict(
            width=3,
            color='blue'
        ),
        name='Revenue'
    ))

    fig.add_vline(
        x=break_even,
        annotation_text=f'Break-even: {break_even:.1f} months',
        annotation_position='bottom right'
    )

    fig.update_layout({
        'plot_bgcolor': 'rgba(0, 0, 0, 0)',
    })

    fig.update_yaxes(
        title_text='EUR'
    )

    fig.update_xaxes(
        title_text='Month'
    )

    st.plotly_chart(fig)

month = np.array([])
revenue = np.array([])
total_time_frame = 0

st.title('Phase 1')

user_count1 = int(st.text_input('1. Final user count:', value=0))
time_frame1 = int(st.text_input('1. Duration (in months):', value=6))
revenue_per_user1 = float(st.text_input('1. Revenue per user (in EUR):', value=10))
monthly_cost1 = int(st.text_input('1. Monthly expenses (in EUR):', value=4000))


st.title('Phase 2')

user_count2 = int(st.text_input('2. Final user count:', value=500))
time_frame2 = int(st.text_input('2. Duration (in months):', value=12))
revenue_per_user2 = float(st.text_input('2. Revenue per user (in EUR):', value=10))
monthly_cost2 = int(st.text_input('2. Monthly expenses (in EUR):', value=8000))


st.title('Phase 3')

user_count3 = int(st.text_input('3. Final user count:', value=2000))
time_frame3 = int(st.text_input('3. Duration (in months):', value=12))
revenue_per_user3 = float(st.text_input('3. Revenue per user (in EUR):', value=10))
monthly_cost3 = int(st.text_input('3. Monthly expenses (in EUR):', value=15000))

costs = np.concatenate([np.ones(time_frame1) * monthly_cost1,
                np.ones(time_frame2) * monthly_cost2,
                np.ones(time_frame3) * monthly_cost3])

revenues = np.concatenate([(0 + np.arange(1, time_frame1 + 1, 1) * (user_count1 - 0) / time_frame1) * revenue_per_user1,
                    (user_count1 + np.arange(1, time_frame2 + 1, 1) * (user_count2 - user_count1) / time_frame2) * revenue_per_user2,
                    (user_count2 + np.arange(1, time_frame3 + 1, 1) * (user_count3 - user_count2) / time_frame3) * revenue_per_user3])

month = np.arange(0, time_frame1 + time_frame2 + time_frame3)

df = pd.DataFrame({'Revenue': revenues, 'Expenses': costs, 'Month': month})

print(df)

break_even = 1000000

for index, (revenue, cost) in enumerate(zip(revenues, costs)):
    if revenue > cost:
        revenue_growth = revenues[index] - revenues[index - 1]
        break_even = index - 1 + (costs[index] - revenues[index - 1]) / revenue_growth

needed_funding = df[df['Month'] < break_even]['Expenses'].sum(
) - df[df['Month'] < break_even]['Revenue'].sum()

draw_graph(df, break_even, needed_funding)
