import logging

from bot import Bot
from core.config import settings
from quotes_client.http_client import QuotesClientHttp

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


def main():
    quote_service_client = QuotesClientHttp(settings.quote_service_url)
    bot = Bot(quote_service_client)
    bot.run()


if __name__ == '__main__':
    main()
