"""Test for searchprevious utility functions"""

from aiida_amber.utils import searchprevious


def test_link_formats():
    """
    Tests if given strings are formatted correctly with format_link_label
    function
    """

    str1 = searchprevious.format_link_label("1?.consecutive__underscores..txt")
    assert str1 == "1_consecutive_underscores_txt"
