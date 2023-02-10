from common import Fonts, Images, Colors

def add_twitter_handle(fig, x=0.75, y=0, fs=28, w=0.03):
    """ Plot the twitter logo and handle at the spcified position. """
    logo_dim = w
    label_ax = fig.add_axes([x + logo_dim, y, 0.1, 0.05])
    label_ax.text(
        0,
        0,
        "@agale137",
        color=Colors.BLACK,
        fontsize=fs,
        fontproperties=Fonts.BARLOW,
        va="bottom",
        ha="left",
    )
    #224x189
    aspect = 189 / 224
    label_ax.axis("off")
    logo_ax = fig.add_axes([x, y, logo_dim, logo_dim])
    logo_ax.set_ylim([200, -24])
    logo_ax.set_xlim([0, 224])
    logo_ax.imshow(Images.TWITTER, aspect=aspect)
    logo_ax.axis("off")
