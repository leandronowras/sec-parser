import pytest
from sec_parser.semantic_elements.semantic_elements import (
    BoldElement,
)
from tests.unit.parsing_plugins._utils import get_elements_from_html
from sec_parser.parsing_plugins.bold_section_plugin import BoldSectionPlugin


# Main Test Function
@pytest.mark.parametrize(
    "html_str, expected_types, expected_tags",
    [
        (
            """<b>0</b>
            """,
            [
                BoldElement,
            ],
            ["b"],
        )
    ],
)
def test_bold_section_plugin(html_str, expected_types, expected_tags):
    # Arrange
    elements = get_elements_from_html(html_str)
    print("elements", elements[0].html_tag.bs4.name)
    plugin = BoldSectionPlugin()

    # Act
    processed_elements = plugin.apply(elements)
    second_run = plugin.apply(processed_elements)

    # Assert
    assert second_run is None  # Plugin should only run once
    print("processed_elements", processed_elements)

    assert len(processed_elements) == len(expected_types)
    for ele, expected_type, expected_tag in zip(
        processed_elements, expected_types, expected_tags
    ):
        assert isinstance(ele, expected_type)
        assert ele.html_tag.bs4.name == expected_tag
