import matplotlib.font_manager as fm
from importlib_resources import files


class Fonts:
    BARLOW = fm.FontProperties(fname=files('common.fonts-src').joinpath('Barlow.otf'))
    BARLOW_BOLD = fm.FontProperties(fname=files('common.fonts-src').joinpath('Barlow-Bold.otf'))
