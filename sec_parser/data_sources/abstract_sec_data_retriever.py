from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from sec_parser.data_sources.sec_edgar_types import (
    DocumentType,
    SectionType,
    validate_sections,
)
from sec_parser.exceptions.core_exceptions import SecParserValueError

if TYPE_CHECKING:
    from collections.abc import Iterable


class InvalidURLError(SecParserValueError):
    pass


class InvalidTickerError(SecParserValueError):
    pass


class DocumentTypeNotSupportedError(SecParserValueError):
    pass


class DocumentNotFoundError(SecParserValueError):
    pass


class AbstractSECDataRetriever(ABC):
    SUPPORTED_DOCUMENT_TYPES: frozenset[DocumentType] = frozenset()

    def __init__(self) -> None:
        if self.SUPPORTED_DOCUMENT_TYPES is None:
            msg = "SUPPORTED_DOCUMENT_TYPES must be set in subclass"
            raise NotImplementedError(
                msg,
            )

    def get_html_from_url(
        self: AbstractSECDataRetriever,
        doc_type: DocumentType | str,
        *,
        url: str,
        sections: Iterable[SectionType | str] | None = None,
    ) -> str:
        doc_type, sections = self._validate_and_convert(doc_type, sections)
        return self._get_html_from_url(
            doc_type,
            url=url,
            sections=sections,
        )

    def get_latest_html_from_ticker(
        self: AbstractSECDataRetriever,
        doc_type: DocumentType | str,
        *,
        ticker: str,
        sections: Iterable[SectionType | str] | None = None,
    ) -> str:
        doc_type, sections = self._validate_and_convert(doc_type, sections)
        return self._get_latest_html_from_ticker(
            doc_type,
            ticker=ticker,
            sections=sections,
        )

    @abstractmethod
    def _get_html_from_url(
        self: AbstractSECDataRetriever,
        doc_type: DocumentType,
        *,
        url: str,
        sections: Iterable[SectionType] | None = None,
    ) -> str:
        raise NotImplementedError  # pragma: no cover

    @abstractmethod
    def _get_latest_html_from_ticker(
        self: AbstractSECDataRetriever,
        doc_type: DocumentType,
        *,
        ticker: str,
        sections: Iterable[SectionType] | None = None,
    ) -> str:
        raise NotImplementedError  # pragma: no cover

    def _validate_and_convert(
        self,
        doc_type: DocumentType | str,
        sections: Iterable[SectionType | str] | None = None,
    ) -> tuple[DocumentType, Iterable[SectionType] | None]:
        new_doc_type = (
            DocumentType.from_str(doc_type) if isinstance(doc_type, str) else doc_type
        )
        if new_doc_type not in self.SUPPORTED_DOCUMENT_TYPES:
            msg = f"Document type {doc_type} not supported."
            raise DocumentTypeNotSupportedError(msg)
        new_sections = (
            [
                SectionType.from_str(section) if isinstance(section, str) else section
                for section in sections
            ]
            if sections
            else None
        )
        validate_sections(new_doc_type, new_sections)
        return new_doc_type, new_sections
