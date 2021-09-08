import pytest

# def test_genric():
#     a = 2
#     b = 2
#     assert a == b
#     # assert a != b

class NotInRange(Exception):
    def __init__(self, message="value not in range"):
        self.message = message
        super().__init__(self.message)


class MinValue(Exception):
    def __init__(self, message="Less than min value required"):
        self.message = message
        super().__init__(self.message)



def test_check_value_range():
    a = 5
    with pytest.raises(NotInRange):
        if a not in range(10,20):
            raise NotInRange


def test_check_min_value():
    a = 5
    with pytest.raises(NotInRange):
        if a < 10:
            raise MinValue