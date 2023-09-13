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

        for i, element in enumerate(elements):
            if self._is_document_bold_section(element.html_tag.bs4):
                to_be_returned.append(element)
            else:
                continue # or append as unclaimed?

        return to_be_returned

    def _is_document_bold_section(self, tag: bs4.Tag) -> bool:
      if tag.name == "b":
        return True
      try:
        return tag["font-weight"] == "700"
      except:
        return False

    def _handle_document_bold_section(
        self,
        elements: list[AbstractSemanticElement],
        index: int,
    ) -> tuple[AbstractSemanticElement, bool]:
      # i dont get the index yet
        return BoldElement(elements[0].html_tag), True
