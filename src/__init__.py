"""Main survey file.
"""
import os
import random

from flask_login import current_user
from hemlock import User, Page
from hemlock.functional import compile, validate, test_response
from hemlock.questions import Check, Input, Label, Range, Select, Textarea
from hemlock.utils.random import Assigner
from hemlock.utils.statics import make_figure
from sqlalchemy_mutable.utils import partial

BANANAS_SRC = "https://images-cdn.9gag.com/photo/a7yANnA_700b.jpg"
ORANGES_SRC = "http://justfunfacts.com/wp-content/uploads/2015/12/orange-fruit.jpg"
PROBABILITY_BANANAS = .75

assigner = Assigner(
    {
        "default_bananas": (0, 1),
        "animal": (
            CHICK := "chick",
            PUPPY := "puppy",
            KITTEN := "kitten",
            BUNNY := "bunny",
            SEAL := "seal",
            HAMSTER := "hamster",
            BEAR := "bear",
            OTTER := "otter",
            SHEEP := "sheep",
            ELEPHANT := "elephant"
        )
    }
)

animal_urls = {
    CHICK: "https://www.pixelstalk.net/wp-content/uploads/2016/03/Cute-animal-wallpapers-hd-desktop.jpg",
    PUPPY: "https://www.pixelstalk.net/wp-content/uploads/2016/03/Cute-Animal-Wallpaper-HD-desktop.jpg",
    KITTEN: "https://www.pixelstalk.net/wp-content/uploads/2016/03/Cute-Animal-Wallpapers-Background-free.jpg",
    BUNNY: "https://www.pixelstalk.net/wp-content/uploads/2016/03/Cute-Animal-Wallpapers-For-Desktop-Background-Full-Screen.jpg",
    SEAL: "https://www.pixelstalk.net/wp-content/uploads/2016/03/Cute-Animal-1920x1080-wallpaper-HD.jpg",
    HAMSTER: "https://www.pixelstalk.net/wp-content/uploads/2016/03/Cute-animal-hd-wallpaper-download-free.jpg",
    BEAR: "https://www.pixelstalk.net/wp-content/uploads/images2/Animal-Wallpapers-Bear-Baby-Cute.jpg",
    OTTER: "https://www.pixelstalk.net/wp-content/uploads/images2/Baby-Animals-Otter-Ocean-Sea-Cute-Funny-Pictures-Wallpapers.jpg",
    SHEEP: "https://www.pixelstalk.net/wp-content/uploads/images2/Cute-baby-sheep-wallpapers.jpg",
    ELEPHANT: "https://www.pixelstalk.net/wp-content/uploads/images2/Nature-Animals-Cute-Little-Baby-Elephant.jpg"
}


@User.route("/survey")
def seed():
    """Creates the main survey branch.

    Returns:
        List[Page]: List of pages shown to the user.
    """
    bananas = random.random() < PROBABILITY_BANANAS
    current_user.meta_data["bananas"] = int(bananas)
    assignment = assigner.assign_user()
    return [
        Page(
            Label(
                make_figure(animal_urls[assignment["animal"]], figure_align="center")
            ),
            Check(
                """
                On the next page, we will show you a picture of oranges or bananas.
                Which do you think we will show you?
                """,
                [(0, "Oranges"), (1, "Bananas")],
                default=assignment["default_bananas"],
                variable="guess_bananas"
            )
        ),
        Page(
            Label(
                make_figure(
                    BANANAS_SRC if bananas else ORANGES_SRC, figure_align="center"
                )
            )
        )
    ]
