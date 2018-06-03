# data settings
FILENAMES_LIST = [
    ('1e6 points with ARes', 'data/demo1e6.hdf'),
    ('1e6 points raw', 'data/demo1e6_raw.hdf'),
    ('1e7 points with ARes', 'data/demo1e7.hdf'),
]
IDs = [id for id, fn in FILENAMES_LIST]
FILENAMES = {id: fn for id, fn in FILENAMES_LIST}

# plot settings
PRELOAD_MARGIN = 1.  # multiple of viewport xrange in either direction pre-rendered at max resolution
MAX_POINTS_VIEWPORT = 5000  # target number of points to be shown on-screen
MAX_POINTS_TOTAL = 10000  # target number of points to be loaded
