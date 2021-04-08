import os
import pytest
from network_wrangler import ProjectCard

CARD_DIR = os.path.join(".", "projects")


def read_project_cards(card_dir: str = CARD_DIR) -> tuple:
    """
    Returns a list of project cards from a directory.
    Args:
        card_dir: a folder location storing project cards
    Returns:
        tuple of ProjectCard and card filename

    """

    card_tuple = ()
    for (dirpath, dirnames, filenames) in os.walk(card_dir):
        for filename in filenames:
            name, extension = os.path.splitext(filename)
            if extension in [".yml", ".yaml"]:
                card_file = os.path.join(card_dir, filename)
                card = ProjectCard.read(card_file, validate=False)
                card_tuple + (card, card_file)
        break

    return card_tuple
