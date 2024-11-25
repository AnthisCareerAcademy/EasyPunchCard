import pytest
from Clock import Clock

def test_invalid_id_type():
    # Test with invalid types
    invalid_ids = [1234, 12.34, None, True, {"id": "1234"}, ["1234"], ("1234",)]

    for invalid_id in invalid_ids:
        with pytest.raises(TypeError):
            clock = Clock(invalid_id)