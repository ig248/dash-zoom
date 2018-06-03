# -*- coding: utf-8 -*-
import uuid
import dash_core_components as dcc
import dash_html_components as html
from config import IDs


def get_session_id():
    return str(uuid.uuid4())


intro = '''
This demo shows how to make millions of datapoints available through Dash/Plotly, while maintaining
both performance and full detail at high zoom.
'''


def layout():
    """Create app layout"""
    session_id = get_session_id()
    return html.Div(children=[
        html.H1(
            children='Plotting millions of points with Dash and ARes',
            style={
                'textAlign': 'center',
            }
        ),
        #
        dcc.Markdown(intro),
        # select recording
        html.Label('Example:'),
        html.Div(
            style={'width': 500},
            children=[
                dcc.Dropdown(
                    id='file-dropdown',
                    options=[
                        {'label': '{:2d}: {}'.format(idx+1, id), 'value': id}
                        for idx, id in enumerate(IDs)
                    ],
                    value=IDs[0],
                ),
            ]
        ),
        # main figure
        dcc.Graph(
            id='main-graph',
            className='main-graph'
        ),
        html.Div(
            className='session-info',
            children=[
                html.Div(session_id, id='session-id'),
            ])
    ])
