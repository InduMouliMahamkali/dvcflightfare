import pytest


class OutofRange(Exception):
    def __init__(self, message="input not in range"):
        self.message=message
        super().__init__(self.message)

def test_generic():
    a = 5
    with pytest.raises(OutofRange):
        if a not in range(10, 20):
            raise OutofRange