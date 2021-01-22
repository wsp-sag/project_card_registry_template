# project_card_registry_template
A template repository for Network Wrangler Project Card registries.

[Network Wrangler 2.0](https://github.com/wsp-sag/network_wrangler) is a Python library for managing travel model network scenarios. Network Wrangler uses `Project Cards` to define network edits. The purpose of this repository is to manage potentially conflicting Project Cards.

Consider, for example, an existing base year network that includes nodes A, B, and C. Project Card X extends Main Street, adding Node 1 at Location Alpha. Project Card Y extends Broad Street, adding a different a node at Location Beta, but also labeling the new node Node 1. In the current Network Wrangler framework, users must manually manage the conflicting "Node 1" definitions. The purpose of this repository is to automate the node number process via a registry.

## Instructions
  
