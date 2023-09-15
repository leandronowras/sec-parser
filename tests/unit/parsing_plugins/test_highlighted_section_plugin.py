import pytest
from sec_parser.parsing_engine.html_parser import HtmlParser
from sec_parser.semantic_elements.abstract_semantic_elements import AbstractSemanticElement
from sec_parser.semantic_elements.semantic_elements import (
    HighlightedElement,
    UnclaimedElement,
)
from tests.unit.parsing_plugins._utils import get_elements_from_html
from sec_parser.parsing_plugins.highlighted_section_plugin import HighlightedPlugin
from bs4 import BeautifulSoup as bs
from sec_parser.parsing_engine.html_tag import HtmlTag


# Main Test Function
@pytest.mark.parametrize(
    "html_str, expected_types, expected_tags",
    [
        (
            """<b>bold text with bold tag</b>
            <p>normal text</p>
            <p font-weight='700'>bold text with font-weight</p>
            """, 
            [
                # expected to ignore what is not bold
                HighlightedElement,
                HighlightedElement,
            ],
            ["b", "p", "p"],
        )
    ],
)
def test_bold_section_plugin(html_str, expected_types, expected_tags):
    # Arrange
    # -- my helper because get_elements_from_html only parses to Unclaimed
    to_parser = HtmlParser()
    html_to_htmltag = to_parser.get_root_tags(html_str) # list of class bs htmltag
    elements: list[AbstractSemanticElement]= []

    for element in html_to_htmltag:
      elements.append(HighlightedElement(element))
    # --
    plugin = HighlightedPlugin()

    # Act
    processed_elements = plugin.apply(elements)
    second_run = plugin.apply(processed_elements)

    # Assert
    assert second_run is None  # Plugin should only run once

    assert len(processed_elements) == len(expected_types)
    # TODO: test to check the other elements  
    for ele, expected_type, expected_tag in zip(
        processed_elements, expected_types, expected_tags
    ):
        assert isinstance(ele, expected_type)
        assert ele.html_tag.bs4.name == expected_tag


@pytest.mark.parametrize(
    "html_str, expected_types",
    [
        (
            """<b>bold text with bold tag</b>
            <p>normal text</p>
            <i>italic text with italic tag</i>
            <p>normal text</p>
            <p font-weight='700'>bold text with font-weight</p>
            """, 
            [
                # expected to ignore what is not bold
                HighlightedElement,
                HighlightedElement,
            ],
        )
    ],
)
def test_ranking_of_bold_section_plugin(html_str, expected_types):
    # Arrange
    # -- my helper because get_elements_from_html only parses to Unclaimed
    to_parser = HtmlParser()
    html_to_htmltag = to_parser.get_root_tags(html_str) # list of class bs htmltag
    elements: list[AbstractSemanticElement]= []

    for element in html_to_htmltag:
      elements.append(HighlightedElement(element))
    # --
    plugin = HighlightedPlugin()

    # Act
    processed_elements = plugin.apply(elements)
    second_run = plugin.apply(processed_elements)


    # Assert
    assert second_run is None  # Plugin should only run once
    
    # TODO: better way to get the ranking
    print(plugin.element_ranking)
    assert plugin.element_ranking[0][1][0] == plugin.BOLD_TAG_RANKING
    assert plugin.element_ranking[1][1][0] == plugin.ITALIC_RANKING
    assert plugin.element_ranking[2][1][0] == plugin.HIGH_FONT_WEIGHT_RANKING

    for ele, expected_type in zip(
        processed_elements, expected_types
    ):
        assert isinstance(ele, expected_type)

