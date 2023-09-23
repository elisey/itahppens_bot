import logging

import app.text as text_module
from app.core.config import settings
from app.quotes_client.interface import QuoteNotFound, QuotesClientInterface, QuoteServiceError
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CallbackQueryHandler, CommandHandler, ContextTypes


logger = logging.getLogger(__name__)


class Bot:
    def __init__(self, quote_service: QuotesClientInterface) -> None:
        self.quote_service = quote_service

    def run(self) -> None:
        self.application = ApplicationBuilder().token(settings.telegram_bot_token).build()

        start_handler = CommandHandler("start", self.start)
        it_handler = CommandHandler("it", self.it_command)
        button_handler = CallbackQueryHandler(self.button)

        self.application.add_handler(start_handler)
        self.application.add_handler(it_handler)
        self.application.add_handler(button_handler)

        logger.info("Start BOT")

        self.application.run_polling()

    @staticmethod
    def _build_keyboard(current_id: int) -> InlineKeyboardMarkup:
        keyboard = [
            [
                # Uncomment for previous button functionality
                # InlineKeyboardButton(f'{current_id - 1} ⬅', callback_data=str(current_id - 1)),
                InlineKeyboardButton(f"➡ {current_id + 1}", callback_data=str(current_id + 1)),
            ],
        ]

        return InlineKeyboardMarkup(keyboard)

    async def _send_quote(self, chat_id: int, context: ContextTypes.DEFAULT_TYPE, quote_id: int) -> None:
        keyboard = Bot._build_keyboard(quote_id)
        quote_head = str(quote_id) + "\n"
        try:
            quote_text = await self.quote_service.get_quote(quote_id)
        except QuoteNotFound:
            quote_text = quote_head + text_module.EMPTY_QUOTE
        except QuoteServiceError:
            quote_text = quote_head + text_module.SOMETHING_WENT_WRONG
        else:
            quote_text = quote_head + quote_text

        await context.bot.send_message(chat_id, text=quote_text, reply_markup=keyboard)

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        if update.effective_chat is None:
            logger.error("Unexpected update object received in start handler")
            return
        chat_id = update.effective_chat.id
        logger.info(f"Start received from {chat_id}")
        await context.bot.send_message(chat_id=chat_id, text=text_module.START_MESSAGE)

        await self._send_quote(chat_id, context, 1)

    async def it_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        if update.effective_chat is None or update.effective_message is None:
            logger.error("Unexpected update object received in it_command handler")
            return
        message = update.effective_message
        chat_id = update.effective_chat.id
        logger.info(f"IT received from {chat_id}")
        text = message.text
        if text is None:
            logger.error("Unexpected message text received in it_command handler")
            return

        try:
            quote_id_str = text.split(maxsplit=1)[1]
        except IndexError:
            await message.reply_text(text_module.INVALID_IT_COMMAND)
            return

        try:
            quote_id = int(quote_id_str)
        except ValueError:
            await message.reply_text(text_module.INVALID_IT_COMMAND)
            return

        await self._send_quote(chat_id, context, quote_id)

    async def button(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        if update.effective_chat is None or update.callback_query is None:
            logger.error("Unexpected update object received in button handler")
            return
        chat_id = update.effective_chat.id
        query = update.callback_query
        logger.info(f"button event received from {chat_id}, data={query.data}")

        await query.answer()

        await query.edit_message_reply_markup(reply_markup=None)
        if query.data is None:
            logger.error("Unexpected query.data received in button handler")
            return
        quote_id = int(query.data)
        await self._send_quote(chat_id, context, quote_id)
