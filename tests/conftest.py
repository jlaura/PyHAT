import pytest
import numpy as np


@pytest.fixture
def n_dim(n):
    return np.repeat(np.arange(1, n + 1), (25)).reshape(n,-1,5)

@pytest.fixture
def eight_dim():
    return n_dim(8)

@pytest.fixture
def seven_dim():
    return n_dim(7)

@pytest.fixture
def six_dim():
    return n_dim(6)

@pytest.fixture
def five_dim():
    return n_dim(5)

@pytest.fixture
def three_dim():
    return n_dim(3)

@pytest.fixture
def four_dim():
    return n_dim(4)

@pytest.fixture
def two_dim():
    return n_dim(2)
