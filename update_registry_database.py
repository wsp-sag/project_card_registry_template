import os
import yaml
import pytest
import pandas as pd
from network_wrangler import ProjectCard


def update_registry_database(
    card_tuple: tuple, df: pd.DataFrame, config: dict, write_to_disk: bool
) -> pd.DataFrame:
    """
    Returns an updated registry dataframe.
    Args:
        cards_tuple: a list of project cards and their filenames
        df: input registry DataFrame
        config: input configuration
        write_cards: a boolean indicating whether project card updates should be written to disk
    Returns:
        Registry DataFrame updated

    """

    s_node = config_dict["start_node_number"]
    s_link = config_dict["start_link_number"]

    for card in card_tuple:
        df, needs_updating, card_dict = update_nodes(df, card[0], s_node)
        df, needs_updating, card_dict = update_links(df, card[0], s_link)
        if needs_updating:
            card[0].__dict__.update(card_dict)
            if write_to_disk:
                card[0].write(filename=card[1])

    return df


def update_nodes(input_df: pd.DataFrame, card: ProjectCard, start: int):
    """
    Updates node entries in the registry database
    Args:
        input_df: input registry DataFrame
        card: ProjectCard
        start: largest node number in the existing network
    Returns:
        An updated registry database with new node entries
        A flag as to whether the card needs to be modified
        An updated dictionary of the card entries
    """

    card_dict = card.__dict__
    node_df = input_df[input_df["type"] == "node"]
    write_updated_card = False

    if card_dict["category"] == "New Roadway":
        node_index = 0
        for node in card_dict["nodes"]:
            new_node = node["model_node_id"]
            if new_node <= start:
                msg = "New node number ({}) in project '{}' is less than the \
                 starting node number in config file of {}".format(
                    new_node, card_dict["project"], start,
                )
                raise ValueError(msg)

            if new_node not in node_df["number"].values:
                df = pd.DataFrame(
                    {
                        "type": "node",
                        "id": [new_node],
                        "project_added": [card_dict["project"]],
                    }
                )
                node_df = node_df.append(df)
            else:
                number = 1 + node_df["number"].max()
                card_dict["nodes"][node_index]["model_node_id"] = number
                for i in range(0, len(card_dict["links"])):
                    if card_dict["links"][i]["A"] == new_node:
                        card_dict["links"][i]["A"] = number
                    if card_dict["links"][i]["B"] == new_node:
                        card_dict["links"][i]["B"] = number
                df = pd.DataFrame(
                    {
                        "type": "node",
                        "id": [number],
                        "project_added": [card_dict["project"]],
                    }
                )
                node_df = node_df.append(df)
                write_updated_card = True

            node_index = node_index + 1

    return node_df, write_updated_card, card_dict


def update_links(input_df: pd.DataFrame, card: ProjectCard, start: int):
    """
    Updates link entries in the registry database
    Args:
        input_df: input registry DataFrame
        card: ProjectCard
        start: largest link number in the existing network
    Returns:
        An updated registry database with new link entries
    """

    card_dict = card.__dict__
    link_df = input_df[input_df["type"] == "link"]
    write_updated_card = False

    link_index = 0
    for link in card_dict["links"]:
        new_link = link["model_link_id"]

        if new_link <= start:
            msg = "New link id ({}) in project '{}' is less than the \
            starting link number in config file of {}".format(
                new_link, card_dict["project"], start,
            )
            raise ValueError(msg)

        if new_link not in link_df["number"].values:
            df = pd.DataFrame(
                {
                    "type": "link",
                    "id": [new_link],
                    "project_added": [card_dict["project"]],
                }
            )
            link_df = link_df.append(df)
        else:
            number = 1 + link_df["number"].max()
            card_dict["links"][link_index]["model_link_id"] = number
            for i in range(0, len(card_dict["links"])):
                if card_dict["links"][i]["model_link_id"] == new_link:
                    card_dict["links"][i]["model_link_id"] = number
            df = pd.DataFrame(
                {
                    "type": "link",
                    "id": [number],
                    "project_added": [card_dict["project"]],
                }
            )
            link_df = link_df.append(df)
            write_updated_card = True

        link_index = link_index + 1

    return link_df, write_updated_card, card_dict
