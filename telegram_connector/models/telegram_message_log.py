# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import datetime

class TelegramMessageLog(models.Model):
    _name = "telegram.message.log"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Telegram Message Log"
    _order = "timestamp desc"
    _rec_name = 'display_name'
    
    display_name = fields.Char(
        string="Display Name",
        compute="_compute_display_name",
        store=True
    )
    telegram_config_id = fields.Many2one(
        "telegram.config",
        string="Bot Config"
    )
    telegram_update_id = fields.Char(
        string="Update ID",
        help="ID received data from Telegram"
    )
    message = fields.Text(
        string="Message",
        required=True
    )
    direction = fields.Selection(
        [("in", "Received"), ("out", "Sent")],
        string="Direction",
        required=True
    )
    status = fields.Char(
        string="Status"
    )
    response = fields.Text(
        string="Response"
    )
    date = fields.Char(
        string="Date",
        readonly = True,
        default = lambda self: fields.Datetime.now(),
        help="Date received data from Telegram, type is timestamp"
    )
    timestamp = fields.Datetime(
        string='Timestamp',
        default=fields.Datetime.now
    )
    formatted_date = fields.Char(
        string="Telegram Create Date",
        compute="_compute_formatted_date",
        store=True
    )

    # for message - from (Telegram chatbot)
    bot_id = fields.Char(
        string="From ID",
        help="ID of the chatbot to which the message was sent"
    )
    is_bot = fields.Boolean(
        string="is Bot"
    )
    bot_first_name = fields.Char(
        string="First Name"
    )
    bot_last_name = fields.Char(
        string="Last Name"
    )
    bot_username = fields.Char(
        string="Username"
    )

    # for message - chat (user input from the Telegram)
    chat_id = fields.Char(
        string="Chat ID",
        help="ID of the chat to which the message was sent"
    )
    chat_type = fields.Char(
        string="Chat Type"
    )
    first_name = fields.Char(
        string="First Name"
    )
    last_name = fields.Char(
        string="Last Name"
    )
    username = fields.Char(
        string="Username"
    )

    @api.depends('telegram_config_id.telegram_chat_id', 'timestamp')
    def _compute_display_name(self):
        for rec in self:
            chat_id = rec.telegram_config_id.telegram_chat_id or "Unknown Chat Id"
            if rec.timestamp:
                # Use local timestamp and format
                local_timestamp = fields.Datetime.context_timestamp(rec, rec.timestamp)
                formatted_time = local_timestamp.strftime('%Y-%m-%d %H:%M:%S')
                rec.display_name = f"{chat_id} - {formatted_time}"
            else:
                rec.display_name = f"{chat_id} - No timestamp"

    @api.depends('date')
    def _compute_formatted_date(self):
        for rec in self:
            if rec.date:
                try:
                    # Telegram sends timestamp as int (seconds)
                    dt = datetime.fromtimestamp(int(rec.date))
                    local_dt = fields.Datetime.context_timestamp(rec, dt)
                    rec.formatted_date = local_dt.strftime('%Y/%m/%d %H:%M:%S')
                except Exception as _:
                    rec.formatted_date = rec.date
            else:
                rec.formatted_date = ''
