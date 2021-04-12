import os
import warnings
import pytest
from network_wrangler import ProjectCard

CARD_DIR = os.path.join(".", "projects")


def read_project_cards(card_dir: str = CARD_DIR) -> list:
    """
    Returns a list of project cards from a directory.
    Args:
        card_dir: a folder location storing project cards
    Returns:
        List of tuples, with the ProjectCard and card filename

    """

    card_file_list = []
    for (dirpath, dirnames, filenames) in os.walk(card_dir):
        for filename in filenames:
            name, extension = os.path.splitext(filename)
            if extension in [".yml", ".yaml"]:
                card_file = os.path.join(card_dir, filename)
                try:
                    card = ProjectCard.read(card_file, validate=True)
                except ValidationError as exc:
                    msg = "Card ({}) did not validate. Trying without validation.".format(
                        card_file,
                    )
                    warnings.warn(msg)
                    warnings.warn(exc.message)
                except SchemaError as exc:
                    msg = "Card ({}) did not validate. Trying without validation.".format(
                        card_file,
                    )
                    warnings.warn(msg)
                    warnings.warn(exc.message)
                except yaml.YAMLError as exc:
                    msg = "Card ({}) did not validate. Trying without validation.".format(
                        card_file,
                    )
                    warnings.warn(msg)
                    warnings.warn(exc.message)
                else:
                    pass
                finally:
                    try:
                        card = ProjectCard.read(card_file, validate=False)
                    except ValueError as exc:
                        msg = "Card ({}) could not be read (even without validation).".format(
                            card_file,
                        )
                        raise ValueError(msg + exc.message)

                card = ProjectCard.read(card_file, validate=False)
                card_file_list.append((card, card_file))

    return card_file_list
