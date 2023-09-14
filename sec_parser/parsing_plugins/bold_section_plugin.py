from __future__ import annotations

import bs4

from sec_parser.parsing_plugins.abstract_parsing_plugin import AbstractParsingPlugin
from sec_parser.semantic_elements.semantic_elements import (
    AbstractSemanticElement
)

# change name to HighlightedPlugin?
class BoldSectionPlugin(AbstractParsingPlugin):
    def __init__(self) -> None:
        self._already_ran = False
        self.element_ranking = []
        self.BOLD_TAG_RANKING = 2
        self.HIGH_FONT_WEIGHT_RANKING = 3
        self.ITALIC_RANKING = 1

    def apply(
        self,
        elements: list[AbstractSemanticElement],
    ) -> list[AbstractSemanticElement] | None:
        if self._already_ran:
            return None
        self._already_ran = True

        to_be_returned: list[AbstractSemanticElement] = []

        for i, element in enumerate(elements):
          ranking = [0]  #list to make it mutable inside methods
          ranking[0] = 0
          # better name: is_highlighted?
          is_bold = [
              self._has_bold_tag(element.html_tag.bs4, ranking),
              self._has_font_weight(element.html_tag.bs4, ranking),
              self._has_italic_tag(element.html_tag.bs4, ranking),
              ]
          if any(is_bold):
            self.element_ranking.append([element, ranking])
            to_be_returned.append(element)

        return to_be_returned


    def _has_bold_tag(self, tag: bs4.Tag, ranking: list[int]) -> bool:
      if tag.name == "b":
        ranking[0] = ranking[0] + self.BOLD_TAG_RANKING
        return True
      return False

    def _has_font_weight(self, tag: bs4.Tag, ranking: list[int]) -> bool:
      try:
        has_high_font_weight = tag["font-weight"] == "700"
        if has_high_font_weight:
          ranking[0] = ranking[0] + self.HIGH_FONT_WEIGHT_RANKING
          return True
        return False
      except:
        return False

    def _has_italic_tag(self, tag: bs4.Tag, ranking: list[int]) -> bool:
      if tag.name == "i":
        ranking[0] = ranking[0] + self.ITALIC_RANKING
        return True
      return False

