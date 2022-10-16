import matplotlib.pyplot as plt
from importlib_resources import files


class Images:
    TWITTER = plt.imread(files('common.images-src').joinpath('twitter.png'))