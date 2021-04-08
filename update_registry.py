import os
import yaml
import pytest
import pandas as pd

from read_project_cards import read_project_cards
from update_registry_database import update_registry_database

CARD_DIR = os.path.join(".", "projects")
REGISTRY_FILE = "registry.csv"
CONFIG_FILE = "registry_config.yml"


def update_registry(
    config_file: str = CONFIG_FILE,
    input_reg_file: str = REGISTRY_FILE,
    output_reg_file: str = REGISTRY_FILE,
    card_dir: str = CARD_DIR,
    write_card_updates: bool = True,
):

    input_reg_df = pd.read_csv(input_reg_file)
    with open(config_file, "r") as file:
        config_dict = yaml.safe_load(file)

    card_file_list = read_project_cards(card_dir)
    df = update_registry_database(
        card_file_list, input_reg_df, config_dict, write_card_updates
    )
    df.to_csv(output_reg_file, index=False)


if __name__ == "__main__":
    update_registry(
        config_file, input_reg_file, output_reg_file, card_dir, write_card_updates
    )
