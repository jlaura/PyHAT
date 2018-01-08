import pytest
import numpy as np

@pytest.fixture
def five_dim():
    return np.repeat(np.arange(1,6), (25)).reshape(5,-1,5)

@pytest.fixture
def four_dim():
    return np.repeat(np.arange(1,5), (25)).reshape(4,-1,5)
