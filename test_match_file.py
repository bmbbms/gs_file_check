import pytest
import match_gs_check


kRESULT = "result"


def test_match_file():
    match_gs_check.match_gs_file()[kRESULT] == True

def func(x):
    return x + 1


def test_answer():
    assert func(4) == 5


if __name__ == "__main__":
    pytest.main("-s test_match_file.py")
