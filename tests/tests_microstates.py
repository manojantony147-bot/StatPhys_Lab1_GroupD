from src.microstates import enumerate_microstates, group_macrostates


def test_enumerate_microstates():
    microstates = list(enumerate_microstates(3))

    assert len(microstates) == 8
    assert len(set(microstates)) == 8


def test_group_macrostates():
    assert group_macrostates(3) == {0: 1, 1: 3, 2: 3, 3: 1}