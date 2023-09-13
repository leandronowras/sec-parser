from __future__ import annotations

import bs4

from sec_parser.parsing_plugins.abstract_parsing_plugin import AbstractParsingPlugin
from sec_parser.semantic_elements.semantic_elements import (
    AbstractSemanticElement,
    BoldElement
)


class BoldSectionPlugin(AbstractParsingPlugin):
    def __init__(self) -> None:
        self._already_ran = False

    def apply(
        self,
        elements: list[AbstractSemanticElement],
    ) -> list[AbstractSemanticElement] | None:
        if self._already_ran:
            return None
        self._already_ran = True

        to_be_returned: list[AbstractSemanticElement] = []
        skip_next_element = False

        for i, element in enumerate(elements):
            if skip_next_element:
                skip_next_element = False
                continue

            if self._is_document_bold_section(element.html_tag.bs4):
                bold_section_element, should_skip = self._handle_document_bold_section(
                    elements, i,
                )
                to_be_returned.append(bold_section_element)
                skip_next_element = should_skip
            else:
                to_be_returned.append(element)

        return to_be_returned

    def _is_document_bold_section(self, tag: bs4.Tag) -> bool:
        return tag.name == "b"

    def _handle_document_bold_section(
        self,
        elements: list[AbstractSemanticElement],
        index: int,
    ) -> tuple[AbstractSemanticElement, bool]:
      # i dont get the index yet
        return BoldElement(elements[0].html_tag), True
