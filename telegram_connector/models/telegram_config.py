# -*- coding: utf-8 -*-
from odoo import models, fields
from odoo.exceptions import UserError
from ..utils import extract_telegram_fields, encode_telegram_response
import json
import logging
import requests


_logger = logging.getLogger(__name__)

class TelegramConfig(models.Model):
    _name = "telegram.config"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Telegram Bot Config"

    name = fields.Char(
        string="Config Name",
        required=True
    )
    bot_token = fields.Char(
        string="Bot Token",
        required=True,
        placeholder="It's Chat Bot Token your Telegram"
    )
    telegram_chat_id = fields.Char(
        string="Chat ID",
        required=True,
        placeholder="It's userId or groupId your Telegram"
    )
    ping_message = fields.Char(
        string="Chat ID",
        required=True,
        default="Message test from Odoo!",
        placeholder="Used to ping via telegram chatbot"
    )
    note = fields.Html(
        string="Note"
    )

    def send_telegram_message(self, message, chat_id=None):
        chat_id = chat_id or self.telegram_chat_id
        if not self.bot_token or not chat_id:
            raise Exception("Invalid Bot token or Chat ID")
        url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
        data = {
            "chat_id": chat_id,
            "text": message,
        }
        try:
            resp = requests.post(url, data=data, timeout=10)
        except Exception as e:
            resp = type('obj', (object,), {'status_code': 500, 'text': str(e)})

        if resp.status_code != 200:
            _logger.error(f"Error sending message to Telegram: {resp.text}")

        try:
            resp_json = resp.json() if hasattr(resp, 'json') else json.loads(resp.text)
        except Exception:
            resp_json = {"error": resp.text}

        encoded = encode_telegram_response(resp_json, ensure_ascii=False)
        result = resp_json.get('result', {})
        from_user = result.get('from', {})
        chat = result.get('chat', {})

        user_fields = extract_telegram_fields(from_user, {
            "bot_id": ("id", 0),
            "is_bot": ("is_bot", False),
            "bot_first_name": ("first_name", ""),
            "bot_last_name": ("last_name", ""),
            "bot_username": ("username", ""),
        })

        chat_fields = extract_telegram_fields(chat, {
            "chat_type": ("type", ""),
            "first_name": ("first_name", ""),
            "last_name": ("last_name", ""),
            "username": ("username", ""),
        })

        self.env['telegram.message.log'].sudo().create({
            "telegram_config_id": self.id,
            "direction": "out",
            "message": message,
            "status": resp.status_code,
            'date': self.create_date,
            "response": encoded,
            'bot_id': user_fields["bot_id"],
            'is_bot': user_fields["is_bot"],
            'bot_first_name': user_fields["bot_first_name"],
            'bot_last_name': user_fields["bot_last_name"],
            'bot_username': user_fields["bot_username"],
            'chat_id': chat_id,  # chat_id is taken from telegram_chat_id, not from chat_fields
            'chat_type': chat_fields["chat_type"],
            'first_name': chat_fields["first_name"],
            'last_name': chat_fields["last_name"],
            'username': chat_fields["username"],
        })
        return resp

    def action_send_test_message(self):
        self.ensure_one()
        try:
            resp = self.send_telegram_message(self.ping_message)
            if resp.status_code == 200:
                return {
                    'type': 'ir.actions.client',
                    'tag': 'display_notification',
                    'params': {
                        'title': 'Success!',
                        'message': 'Successfully sent test message to Telegram.',
                        'type': 'success',
                        'sticky': False,
                    }
                }
            else:
                raise UserError('Send failed! Reason:\n%s' % resp.text)
        except Exception as e:
            raise UserError('Error sending: %s' % e)

    def write(self, vals):
        if 'bot_token' in vals or 'telegram_chat_id' in vals:
            for rec in self:
                if rec.bot_token and 'bot_token' in vals and vals['bot_token'] != rec.bot_token:
                    raise UserError("Bot Token cannot be changed after saved.")
                if rec.telegram_chat_id and 'telegram_chat_id' in vals and vals[
                    'telegram_chat_id'] != rec.telegram_chat_id:
                    raise UserError("Chat ID cannot be changed after saved.")
        return super().write(vals)
