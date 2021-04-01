# Project Card Registry Template 
A template repository for Network Wrangler Project Card registries.

[Network Wrangler 2.0](https://github.com/wsp-sag/network_wrangler) is a Python library for managing travel model network scenarios. Network Wrangler uses `Project Cards` to define network edits. The purpose of this repository is to automate the reconciliation of conflicting Project Cards.

Consider, for example, an existing base year network that includes nodes A, B, and C. Project Card X extends Main Street, adding Node 1 at Location Alpha. Project Card Y extends Broad Street, adding a different node at Location Beta, but also labeling the new node Node 1. In the current Network Wrangler framework, users must manually manage the conflicting "Node 1" definitions. The purpose of this repository is to automate the node number process via a registry.

## Instructions
1. This repository is a [`template`](https://docs.github.com/en/github/creating-cloning-and-archiving-repositories/creating-a-repository-from-a-template), meaning it is designed to be used to create repositories that have the same functionality.
2. To get started, set the `start_node_number` in the `registry_config.yml` file. This number should be the largest node number used in your Network Wrangler base year network.
3. Next, set the `start_link_number` in the `registry_config.yml` file. This number should be the largest link number used in your Network Wrangler base year network. 
4. Add a Project Card to the `projects` directory. Commit the change to GitHub. That's it.

## How Does this Work
When a Project Card is added to the `projects` directory and committed to GitHub, the repository runs a set of procedures to do the following:
1. Identify Project Cards that add roadway or transit links to the network.
2. Warn the user if the new nodes or links are less than the `start_node_number` or `start_link_number` parameter.
3. Update the `registry.csv` database with the new nodes and/or new links, identifying the project that adds them.
4. If a Project Card that adds links conflicts with nodes or links identified in the `registry.csv` database, these nodes and links are updated to use a node or link number that is not in the registry. The Project Cards are updated accordingly.
