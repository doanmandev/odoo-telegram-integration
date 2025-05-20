# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
from ..utils import extract_telegram_fields, encode_telegram_response

import json
import logging

_logger = logging.getLogger(__name__)

class TelegramWebhook(http.Controller):

    @http.route('/telegram/webhook', type='json', auth='public', methods=['POST'], csrf=False)
    def telegram_webhook(self, **kwargs):
        try:
            # Read data from the request
            data = json.loads(request.httprequest.data)
            _logger.info("Received data from Telegram: %s", data)

            # Get a message according to Telegram data
            message = data.get('message')
            if not message:
                _logger.warning("No message found in the request: %s", data)
                return {'status': 'error', 'message': 'No message found'}

            from_user = message.get('from', {})
            chat = message.get('chat', {})
            text = message.get('text', '')
            date = message.get('date', '')

            user_fields = extract_telegram_fields(from_user, {
                "bot_id": ("id", 0),
                "is_bot": ("is_bot", False),
                "bot_first_name": ("first_name", ""),
                "bot_last_name": ("last_name", ""),
                "bot_username": ("username", ""),
            })

            chat_fields = extract_telegram_fields(chat, {
                "usr_chat_id": ("id", 0),
                "usr_type": ("type", ""),
                "usr_first_name": ("first_name", ""),
                "usr_last_name": ("last_name", ""),
                "usr_username": ("username", ""),
            })

            # Check important data
            if not (chat_fields["usr_chat_id"] and text and user_fields["bot_id"]):
                _logger.warning(
                    "Invalid message format (missing chat_id, text or bot_id): chat_id: %s, text: %s, bot_id: %s",
                    chat_fields["usr_chat_id"], text, user_fields["bot_id"]
                )
                return {'status': 'error', 'message': 'Invalid message format'}

            _logger.info("Message from chat %s by user %s (@%s): %s",
                         chat_fields["usr_chat_id"],
                         user_fields["bot_first_name"],
                         user_fields["bot_username"], text)
            
            # Log messages received into the system
            config = request.env['telegram.config'].sudo().search([], limit=1)
            request.env['telegram.message.log'].sudo().create({
                'telegram_config_id': config.id or False,
                'bot_id': user_fields["bot_id"],
                'is_bot': user_fields["is_bot"],
                'bot_first_name': user_fields["bot_first_name"],
                'bot_last_name': user_fields["bot_last_name"],
                'bot_username': user_fields["bot_username"] or config.name,
                'chat_id': chat_fields["usr_chat_id"],
                'chat_type': chat_fields["usr_type"],
                'first_name': chat_fields["usr_first_name"],
                'last_name': chat_fields["usr_last_name"],
                'username': chat_fields["usr_username"] or 'Guest',
                'message': text,
                'direction': 'in',
                'date': date,
                'status': '200',
                'response': encode_telegram_response(data, ensure_ascii=False),
            })

            return {'status': 'success', 'message': 'Message received'}

        except Exception as e:
            _logger.error("Error processing webhook: %s", str(e), exc_info=True)
            return {'status': 'error', 'message': str(e)}