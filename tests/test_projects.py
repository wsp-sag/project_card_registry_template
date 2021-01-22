import os
from geopandas import GeoDataFrame
import pytest
from network_wrangler import ProjectCard
import numpy as np
import pandas as pd

pd.set_option("display.max_rows", 500)
pd.set_option("display.max_columns", 500)
pd.set_option("display.width", 50000)

"""
Run just the tests labeled basic using `pytest -m ci`
To run with print statments, use `pytest -s -m ci`
"""

@pytest.mark.ci
def test_project_card_read(request):
    assert True
    print("--Finished")
