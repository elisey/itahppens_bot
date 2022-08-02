import http

import aiohttp
from pydantic import BaseModel, ValidationError

from .interface import QuotesClientInterface, QuoteNotFound, QuoteServiceError


class Quote(BaseModel):
    item_id: int
    text: str


class QuotesClientHttp(QuotesClientInterface):

    def __init__(self, quote_service_url: str):
        self.quote_service_url = quote_service_url

    async def get_quote(self, quote_id: int) -> str:
        async with aiohttp.ClientSession() as session:
            request_url = self.quote_service_url + str(quote_id)
            async with session.get(request_url) as resp:

                if resp.status == http.HTTPStatus.OK:
                    data = await resp.json()
                    try:
                        quote: Quote = Quote.parse_obj(data)
                    except ValidationError:
                        raise QuoteServiceError(f'Error parse response from quote service. data={data}')
                    return quote.text

                if resp.status == http.HTTPStatus.NOT_FOUND:
                    raise QuoteNotFound
                else:
                    raise QuoteServiceError(f'Error get quote from quote service. status={resp.status}')
