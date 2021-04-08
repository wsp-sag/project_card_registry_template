import os
import pytest
import pandas as pd

from ..update_registry import update_registry

"""
Run tests from bash/shell
Run just the tests labeled project using `pytest -m update_registry`
To run with print statments, use `pytest -s -m update_registry`
"""


@pytest.mark.basic
def test_update_registry(request):

    update_registry(
        config_file="registry_config.yml",
        input_reg_file="registry.csv",
        output_reg_file="test_update_registry.csv",
        card_dir=os.path.join(".", "reference_projects"),
        write_updates=False,
    )

    data = [
        ["node", 1001, "Project B"],
        ["node", 1002, "Project B"],
        ["node", 1003, "Project A"],
        ["node", 1004, "Project A"],
        ["link", 501, "Project B"],
        ["link", 502, "Project A"],
    ]
    target_df = pd.DataFrame(data, columens=["type", "id", "project_added"])

    outcome_df = pd.read_csv(output_reg_file)

    assert target_df == outcome_df
