import os
import sys
import inspect
import pytest
import pandas as pd

c_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
p_dir = os.path.dirname(c_dir)
sys.path.insert(0, p_dir)

from update_registry import update_registry

"""
Run tests from bash/shell
Run just the tests labeled project using `pytest -m update_registry`
To run with print statments, use `pytest -s -m update_registry`
"""


@pytest.mark.basic
@pytest.mark.update_registry
def test_update_registry(request):

    output_file = "test_update_registry.csv"

    update_registry(
        config_file="registry_config.yml",
        input_reg_file="registry.csv",
        output_reg_file=output_file,
        card_dir=os.path.join(".", "reference_projects"),
        write_card_updates=False,
    )

    data = [
        ["node", 1001, "Project B"],
        ["node", 1002, "Project B"],
        ["node", 1003, "Project A"],
        ["node", 1004, "Project A"],
        ["link", 501, "Project B"],
        ["link", 502, "Project A"],
    ]
    target_df = pd.DataFrame(data, columns=["type", "id", "project_added"])
    target_df = target_df.sort_values(by=["type", "id"]).reset_index(drop=True)

    outcome_df = pd.read_csv(output_file)
    outcome_df = outcome_df.sort_values(by=["type", "id"]).reset_index(drop=True)

    assert target_df.equals(outcome_df) is True


@pytest.mark.basic
@pytest.mark.update_registry
def test_update_registry_existing(request):

    output_file = "test_update_registry.csv"
    temp_file = "temp_registry.csv"
    data = [
        ["node", 1001, "Project Z"],
        ["node", 1002, "Project Z"],
        ["link", 501, "Project Z"],
    ]
    temp_df = pd.DataFrame(data, columns=["type", "id", "project_added"])
    temp_df.to_csv(temp_file, index=False)

    update_registry(
        config_file="registry_config.yml",
        input_reg_file=temp_file,
        output_reg_file=output_file,
        card_dir=os.path.join(".", "reference_projects"),
        write_card_updates=False,
    )

    os.remove(temp_file)

    data = [
        ["node", 1001, "Project Z"],
        ["node", 1002, "Project Z"],
        ["link", 501, "Project Z"],
        ["node", 1003, "Project B"],
        ["node", 1004, "Project B"],
        ["node", 1005, "Project A"],
        ["node", 1006, "Project A"],
        ["link", 502, "Project B"],
        ["link", 503, "Project A"],
    ]
    target_df = pd.DataFrame(data, columns=["type", "id", "project_added"])
    target_df = target_df.sort_values(by=["type", "id"]).reset_index(drop=True)

    outcome_df = pd.read_csv(output_file)
    outcome_df = outcome_df.sort_values(by=["type", "id"]).reset_index(drop=True)

    assert target_df.equals(outcome_df) is True
