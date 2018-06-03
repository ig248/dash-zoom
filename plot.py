from server import log, cache, flat_key
from config import PRELOAD_MARGIN, MAX_POINTS_VIEWPORT, MAX_POINTS_TOTAL
from config import FILENAMES
import numpy as np
import pandas as pd


@cache.memoize(timeout=3600)
def get_data(file_id):
    """Get data for all users"""
    if file_id not in FILENAMES:
        raise KeyError('Unknown file ID {}'.format(file_id))
    filename = FILENAMES[file_id]
    df = pd.read_hdf(filename)
    levels, counts = np.unique(df['ares'], return_counts=True)
    counts = counts[::-1].cumsum()[::-1]
    log.debug('<<< Loaded {}'.format(filename))
    return df, levels, counts


def make_figure(file_id, xrange='auto', yrange='auto', session_id=None,
                level=None, baselevel=None):
    # Re-set view range on file change
    if session_id:
        old_filename = cache.get(flat_key(session_id, 'filename'))
        if old_filename and old_filename != file_id:
            log.debug('Filename changed, resetting xrange')
            xrange = 'auto'
            yrange = 'auto'
        cache.set(flat_key(session_id, 'file_id'), file_id)
    log.debug('Filename: {}'.format(file_id))
    # plot data
    df, levels, counts = get_data(file_id)

    x = df['t']
    y = df['x']

    auto_xrange = [x.min(), x.max()]
    cache.set(flat_key(session_id, 'auto_xrange'), auto_xrange)

    duration = auto_xrange[1] - auto_xrange[0]
    if xrange == 'auto':
        xrange = auto_xrange

    xdelta = xrange[1] - xrange[0]

    preload_xstart = xrange[0] - PRELOAD_MARGIN * xdelta
    preload_xend = xrange[1] + PRELOAD_MARGIN * xdelta

    viewport_idx = (preload_xstart <= x) & (x <= preload_xend)

    log.debug('X-axis range: {}'.format(xdelta))

    # auto-choose baselevel
    if baselevel is None:
        for l, c in zip(levels, counts):
            if c <= MAX_POINTS_TOTAL:
                baselevel = l
                break
            else:
                baselevel = levels[-1]
    # auto-choose level
    if level is None:
        for l, c in zip(levels, counts):
            if c * (xdelta / duration) <= MAX_POINTS_VIEWPORT:
                level = l
                break
            else:
                level = levels[-1]
    log.debug('level: {}, baselevel: {}'.format(level, baselevel))

    idx = (df['ares'] >= level) & viewport_idx  # fine points inside viewport
    idx = (df['ares'] >= baselevel) | idx  # coarse points outside viewport
    filtered_x = x[idx]
    filtered_y = y[idx]
    log.debug('Display points: {}'.format(len(filtered_x)))

    # figure
    figure = {
        'data': [
            {
                'x': filtered_x,
                'y': filtered_y,
                'name': 'data',
            }
        ],
        'layout': {
            'dragmode': 'pan',
            'xaxis': {
                'range': xrange,
                'title': 'time',
            },
            'yaxis': {
                'range': yrange,
                'title': 'value',
            }
        }
    }
    return figure
