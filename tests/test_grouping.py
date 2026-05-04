from sportslab.grouping.create_groups import _group_sizes


def test_group_sizes_12():
    assert _group_sizes(12) == [3, 3, 3, 3]


def test_group_sizes_13():
    assert _group_sizes(13) == [4, 3, 3, 3]


def test_group_sizes_15():
    assert _group_sizes(15) == [4, 4, 4, 3]


def test_group_sizes_16_plus():
    assert _group_sizes(16) == [4, 4, 4, 4]
    assert _group_sizes(20) == [4, 4, 4, 4]
