# -*- coding: utf-8 -*-
import os
from server import log, server
import flask
import dash
from layout import layout
from dash.dependencies import Input, Output

from plot import make_figure


app = dash.Dash(server=server)
app.title = 'Large dataset demo'  # https://community.plot.ly/t/including-page-titles-favicon-etc-in-dash-app/4648
app.layout = layout

css_directory = os.path.join(os.getcwd(), 'static/css')
stylesheets = ['stylesheet.css']
static_css_route = '/static/'


@app.server.route('{}<stylesheet>'.format(static_css_route))
def serve_stylesheet(stylesheet):
    if stylesheet not in stylesheets:
        raise Exception(
            '"{}" is excluded from the allowed static files'.format(stylesheet)
        )
    log.debug('CSS directory: {}, CSS file: {}'.format(css_directory, stylesheet))
    return flask.send_from_directory(css_directory, stylesheet)


for stylesheet in stylesheets:
    app.css.append_css({"external_url": "/static/{}".format(stylesheet)})


# main plot
def resolve_range(relayoutData, axis='x'):
    """Extract xrange from relayoutData. Return either [start, end] or 'auto'"""
    log.debug(relayoutData)
    assert axis in 'xy'
    ax = axis
    if not relayoutData or ax+'axis.autorange' in relayoutData or 'autosize' in relayoutData:
        range = 'auto'
    elif ax+'axis.range' in relayoutData:
        range = relayoutData[ax+'axis.range']
    else:
        range = [relayoutData[ax+'axis.range[0]'], relayoutData[ax+'axis.range[1]']]
    return range


@app.callback(Output('main-graph', 'figure'),
              [Input('file-dropdown', 'value'),
               Input('main-graph', 'relayoutData')])
def cbk_update_graph(file_id, relayoutData):
    xrange = resolve_range(relayoutData, 'x')
    yrange = resolve_range(relayoutData, 'y')
    return make_figure(file_id, xrange=xrange, yrange=yrange)
