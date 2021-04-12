import os
import yaml
import pytest
import pandas as pd
from typing import Tuple
from network_wrangler import ProjectCard


def add_cards_to_registry(
    card_file_list: list, input_df: pd.DataFrame, config: dict, write_to_disk: bool
) -> pd.DataFrame:
    """
    Returns an updated registry dataframe.
    Args:
        card_file_list: a list of project cards and their filenames
        df: input registry DataFrame. See the format in `registry.csv`.
        config: input configuration
        write_cards: a boolean indicating whether project card updates should be written to disk. If True, the input project cards will be overwritten.
    Returns:
        Registry DataFrame updated

    """

    s_node = config["start_node_number"]
    s_link = config["start_link_number"]
    out_df = input_df

    for card, filename in card_file_list:
        node_df, node_update, updated_card_dict = _update_registry_nodes(
            out_df, card, s_node
        )
        link_df, link_update, updated_card_dict = _update_registry_links(
            out_df, card, s_link
        )
        out_df = (
            out_df.append(node_df, ignore_index=True)
            .append(link_df, ignore_index=True)
            .drop_duplicates()
            .reset_index(drop=True)
        )
        if node_update or link_update:
            card.__dict__.update(updated_card_dict)
            if write_to_disk:
                card.write(filename=filename)

    return out_df


def _update_registry_nodes(
    input_df: pd.DataFrame, card: ProjectCard, start: int
) -> Tuple[pd.DataFrame, bool, dict]:
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
    write_updated_card = False
    node_df = input_df[input_df["type"] == "node"]

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

            if new_node not in node_df["id"].values:
                node_updates_df = pd.DataFrame(
                    {
                        "type": "node",
                        "id": [new_node],
                        "project_added": [card_dict["project"]],
                    }
                )
                node_df = node_df.append(node_updates_df)
            else:
                number = 1 + node_df["id"].max()
                card_dict["nodes"][node_index]["model_node_id"] = number
                for i in range(0, len(card_dict["links"])):
                    if card_dict["links"][i]["A"] == new_node:
                        card_dict["links"][i]["A"] = number
                    if card_dict["links"][i]["B"] == new_node:
                        card_dict["links"][i]["B"] = number
                node_updates_df = pd.DataFrame(
                    {
                        "type": "node",
                        "id": [number],
                        "project_added": [card_dict["project"]],
                    }
                )
                node_df = node_df.append(node_updates_df)
                write_updated_card = True

            node_index = node_index + 1

    return node_df, write_updated_card, card_dict


def _update_registry_links(
    input_df: pd.DataFrame, card: ProjectCard, start: int
) -> Tuple[pd.DataFrame, bool, dict]:
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
    write_updated_card = False
    link_df = input_df[input_df["type"] == "link"]

    link_index = 0
    for link in card_dict["links"]:
        new_link = link["model_link_id"]

        if new_link <= start:
            msg = "New link id ({}) in project '{}' is less than the \
            starting link number in config file of {}".format(
                new_link, card_dict["project"], start,
            )
            raise ValueError(msg)

        if new_link not in link_df["id"].values:
            link_updates_df = pd.DataFrame(
                {
                    "type": "link",
                    "id": [new_link],
                    "project_added": [card_dict["project"]],
                }
            )
            link_df = link_df.append(link_updates_df)
        else:
            number = 1 + link_df["id"].max()
            card_dict["links"][link_index]["model_link_id"] = number
            for i in range(0, len(card_dict["links"])):
                if card_dict["links"][i]["model_link_id"] == new_link:
                    card_dict["links"][i]["model_link_id"] = number
            link_updates_df = pd.DataFrame(
                {
                    "type": "link",
                    "id": [number],
                    "project_added": [card_dict["project"]],
                }
            )
            link_df = link_df.append(link_updates_df)
            write_updated_card = True

        link_index = link_index + 1

    return link_df, write_updated_card, card_dict
