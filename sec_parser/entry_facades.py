from __future__ import annotations

from typing import TYPE_CHECKING

from sec_parser.data_sources.sec_api_io_data_retriever import SecApiIoDataRetriever
from sec_parser.parsing_engine.sec_parser import SecParser
from sec_parser.semantic_tree_transformations.tree_builder import TreeBuilder

if TYPE_CHECKING:
    from sec_parser.data_sources.sec_edgar_types import DocumentType
    from sec_parser.semantic_tree_transformations.semantic_tree import SemanticTree


def parse_latest(
    doc_type: DocumentType, /, *, ticker: str, sec_api_io_api_key: str | None = None,
) -> SemanticTree:
    retriever = SecApiIoDataRetriever(api_key=sec_api_io_api_key)
    html = retriever.get_latest_html_from_ticker(doc_type, ticker=ticker)

    parser = SecParser()
    elements = parser.parse(html)

    tree_builder = TreeBuilder()
    return tree_builder.build(elements)
