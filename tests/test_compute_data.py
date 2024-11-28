from unittest.mock import Mock
from inflammation.compute_data import analyse_data
import numpy.testing as npt
import math


def test_compute_data_mock_source():
    data_source = Mock()
    data_source.load_inflammation_data.return_value = [[[0, 2, 0]],
                                                       [[0, 1, 0]]]

    result = analyse_data(data_source)
    npt.assert_array_almost_equal(result, [0, math.sqrt(0.25), 0])