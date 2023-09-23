from abc import ABC, abstractmethod


class QuoteNotFound(Exception):
    """Quote not found exception."""


class QuoteServiceError(Exception):
    """Quote service error exception."""


class QuotesClientInterface(ABC):
    @abstractmethod
    async def get_quote(self, quote_id: int) -> str:
        pass
