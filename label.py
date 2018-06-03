from server import log, cache, flat_key
import pandas as pd
import time


def empty_label_df():
    columns = ['user_id', 'session_id', 'file_id', 'time_added', 'start', 'end', 'label', 'comment']
    label_df = pd.DataFrame(columns=columns)
    return label_df


def submit_label(label=None, xrange='auto', comment=None, autoscroll=False,
                 session_id=None, user_id=None):
    if xrange == 'auto':
        xrange = cache.get(flat_key(session_id, 'auto_xrange'))
        if xrange is None:
            raise KeyError('auto_xrange not found in cache')
    try:
        if True in autoscroll:
            autoscroll = True
        else:
            autoscroll = False
    except TypeError:
        autoscroll = autoscroll
    if autoscroll:
        log.debug('Triggering autoscroll...')
        cache.set(flat_key(session_id, 'autoscroll'), True)
        cache.set(flat_key(session_id, 'autoscroll_xrange'), xrange)

    label_df = cache.get(flat_key(user_id, 'label_df'))

    if label_df is None:
        log.debug('Initialised in-memory label store')
        label_df = empty_label_df()

    new_entry = dict(
        user_id=user_id,
        session_id=session_id,
        file_id=cache.get(flat_key(session_id, 'file_id')),
        time_added=time.time(),
        start=xrange[0],
        end=xrange[1],
        label=label,
        comment=comment
    )
    label_df = label_df.append(new_entry, ignore_index=True)
    cache.set(flat_key(user_id, 'label_df'), label_df)
    log.debug('Stored new label: {}'.format(new_entry))
    log.debug('All labels:\n{}'.format(label_df))
    return None
