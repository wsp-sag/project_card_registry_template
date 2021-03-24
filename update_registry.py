import os
import yaml
import pytest
from network_wrangler import ProjectCard
import pandas as pd

card_dir = os.path.join('.', 'projects')
filename_node = 'node_registry.csv'
filename_config = 'registry_config.yml'

card_filenames = []
for (dirpath, dirnames, filenames) in os.walk(card_dir):
    for filename in filenames:
        name, extension = os.path.splitext(filename)
        if (extension in ['.yml', '.yaml']):
            card_filenames.append(os.path.join(card_dir, filename))
    break

node_df = pd.read_csv(filename_node)
with open(filename_config, "r") as config_file:
    config_dict = yaml.safe_load(config_file)

for card_filename in card_filenames:
    write_updated_card = False
    card = ProjectCard.read(card_filename, validate=False)
    card_dict = card.__dict__

    if (card_dict['category'] == 'New Roadway'):
        node_index = 0
        for node in card_dict['nodes']:
            new_node = node['model_node_id']

            if (new_node <= config_dict['start_node_number']):
                msg = "New node number ({}) in project '{}' is less than'\
                'the starting node number in config file of {}".format(
                    new_node,
                    card_dict['project'],
                    config_dict['start_node_number'],
                )
                raise ValueError(msg)

            if (new_node not in node_df['node'].values):
                df = pd.DataFrame(
                    {'node': [new_node], 'project': [card_dict['project']]}
                )
                node_df = node_df.append(df)
            else:
                number = 1 + node_df['node'].max()
                card_dict['nodes'][node_index]['model_node_id'] = number
                for i in range(0, len(card_dict['links'])):
                    if (card_dict['links'][i]['A'] == new_node):
                        card_dict['links'][i]['A'] = number
                    if (card_dict['links'][i]['B'] == new_node):
                        card_dict['links'][i]['B'] = number

                df = pd.DataFrame(
                    {'node': [number], 'project': [card_dict['project']]}
                )
                node_df = node_df.append(df)
                write_updated_card = True

            node_index = node_index + 1

    if (write_updated_card):
        card.__dict__.update(card_dict)
#        name, extension = os.path.splitext(card_filename)
        card.write(filename=card_filename)

node_df.to_csv(filename_node, index=False)
