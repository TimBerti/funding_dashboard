import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from math import ceil

user_count = int(st.text_input('User count:', value=8000))
time_frame = int(st.text_input('after (in months):', value=24))
revenue_per_user = float(st.text_input('Revenue per user (in EUR):', value=10))
monthly_cost = int(st.text_input('Monthly expenses (in EUR):', value=15000))

break_even = time_frame * \
    np.log(monthly_cost/revenue_per_user) / np.log(user_count)

x = np.arange(0, ceil(break_even) + 2)
revenue = revenue_per_user * np.exp(x/time_frame*np.log(user_count))

df = pd.DataFrame({'Revenue': revenue, 'Expenses': np.ones(
    len(x)) * monthly_cost, 'Month': x})

needed_funding = df[df['Month'] < break_even]['Expenses'].sum(
) - df[df['Month'] < break_even]['Revenue'].sum()

fig = go.Figure()

fig.add_trace(go.Scatter(
    x=pd.concat(
        [df[df['Month'] < break_even]['Month'], pd.Series(break_even), df[df['Month'] < break_even]['Month'][::-1]]),
    y=pd.concat(
        [df[df['Month'] < break_even]['Revenue'],  pd.Series(monthly_cost), df[df['Month'] < break_even]['Expenses']]),
    mode='none',
    fill='toself',
    fillcolor='red',
    opacity=.5,
    name='Losses',
    showlegend=False
))

fig.add_trace(go.Scatter(
    x=pd.concat(
        [pd.Series(break_even), df[df['Month'] > break_even]['Month'], df[df['Month'] > break_even]['Month'][::-1], pd.Series(break_even)]),
    y=pd.concat(
        [pd.Series(monthly_cost), df[df['Month'] > break_even]['Revenue'], df[df['Month'] > break_even]['Expenses'], pd.Series(monthly_cost)]),
    mode='none',
    fill='toself',
    fillcolor='green',
    opacity=.5,
    name='Earnings',
    showlegend=False
))

fig.add_trace(go.Scatter(
    x=[break_even / 2],
    y=[monthly_cost / 2],
    mode='text',
    text=f'{needed_funding:.2f} EUR',
    name='Necessary Funding',
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
    title_text='EUR',
    range=[0, revenue[ceil(break_even) + 1]]
)

fig.update_xaxes(
    title_text='Month'
)

st.plotly_chart(fig)
