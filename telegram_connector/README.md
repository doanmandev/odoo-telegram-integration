# Telegram Connector Module Documentation

### Part 1: Document Summary
### Part 2: Details

## Part 1
### Document Summary

This document provides a comprehensive guide to the Telegram Connector module for Odoo.

It includes:
- Introduction and purpose of the Telegram Connector module
- System architecture and components
- Detailed workflow for Telegram Bot integration
- Message handling and storage
- API endpoints for webhook integration
- Utility functions for data processing
- Integration with other Odoo modules
- Security considerations
- Deployment instructions
- Usage examples

This documentation helps developers understand how to implement and extend the Telegram Connector for real-time messaging applications in Odoo.

# Part 2
### Introduction

The Telegram Connector module provides a webhook-based integration between Odoo and Telegram through the Telegram Bot API. It allows Odoo to receive and process messages from Telegram users, store them in the database, and send responses back to users.

### Design Purpose

- **Webhook Integration:** Receives updates from Telegram via webhooks for real-time processing
- **Message Persistence:** Stores all received and sent messages in the database for auditing and processing
- **Bot Configuration:** Provides an interface to manage Telegram bot configurations
- **Two-way Communication:** Supports both receiving messages from and sending responses to Telegram users

### System Architecture

#### Main Components

##### 1. Telegram Configuration (`telegram.config`)
- Manages Telegram bot settings including bot tokens and chat IDs
- Provides API for sending messages to Telegram users
- Implements test functionality to verify configuration

##### 2. Telegram Webhook Controller
- Implements HTTP endpoints to receive webhook callbacks from Telegram
- Processes incoming messages and updates
- Stores message data in the database

##### 3. Message History Storage
- Uses `telegram.message.log` to store message history
- Records sender information, chat details, message content, and timestamps
- Supports both incoming and outgoing messages

### Data Flow

1. **Webhook Registration:**  
   A Telegram Bot is configured to send updates to the Odoo webhook endpoint (`/telegram/webhook`).

2. **Message Reception:**  
   When a user sends a message to the bot, Telegram forwards it to the webhook endpoint.

3. **Message Processing:**  
   The webhook controller extracts message data, creates a record in `telegram.message.log`, and returns a confirmation.

4. **Message Response:**  
   Odoo can send responses to users by calling the `send_telegram_message` method on the `telegram.config` model.

### Models and Fields

#### Telegram Config (`telegram.config`)
| Field             | Type      | Description                                    |
|-------------------|-----------|------------------------------------------------|
| name              | Char      | Configuration name                             |
| bot_token         | Char      | Telegram Bot API Token                         |
| telegram_chat_id  | Char      | Telegram Chat/User ID                          |
| ping_message      | Char      | Test message (default: "Message test from Odoo!") |
| note              | Html      | Additional notes                               |

**Key Methods:**
- `send_telegram_message(message, chat_id=None)`: Sends a message to a Telegram chat
- `action_send_test_message()`: Sends a test message to verify configuration

#### Telegram Message Log (`telegram.message.log`)
| Field              | Type      | Description                                    |
|--------------------|-----------|------------------------------------------------|
| display_name       | Char      | Display name (computed)                        |
| telegram_config_id | Many2one  | Reference to bot configuration                 |
| telegram_update_id | Char      | Telegram update ID                             |
| message            | Text      | Message content                                |
| direction          | Selection | Direction (in/out)                             |
| status             | Char      | Status code                                    |
| response           | Text      | Raw response data                              |
| date               | Char      | Timestamp from Telegram                        |
| timestamp          | Datetime  | Message timestamp in Odoo                      |
| formatted_date     | Char      | Formatted date (computed)                      |
| bot_id             | Char      | Bot/sender ID                                  |
| is_bot             | Boolean   | Whether sender is a bot                        |
| bot_first_name     | Char      | Bot/sender first name                          |
| bot_last_name      | Char      | Bot/sender last name                           |
| bot_username       | Char      | Bot/sender username                            |
| chat_id            | Char      | Chat ID                                        |
| chat_type          | Char      | Chat type                                      |
| first_name         | Char      | User first name                                |
| last_name          | Char      | User last name                                 |
| username           | Char      | User username                                  |

### Utility Functions

The module provides utility functions to handle Telegram data:

- `extract_telegram_fields(source, mapping)`: Extracts and maps fields from Telegram data
- `encode_telegram_response(data, ensure_ascii=False)`: Encodes data as JSON for storage

### Example Usage

#### 1. Configure a Telegram Bot

1. Create a bot through BotFather on Telegram
2. Get the bot token and configure it in Odoo:
   ```python
   bot_config = env['telegram.config'].create({
       'name': 'My Bot',
       'bot_token': '123456789:ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghi',
       'telegram_chat_id': '123456789',
       'ping_message': 'Hello from Odoo!'
   })
   ```

#### 2. Send a Message to a Telegram User
```python
bot_config = env['telegram.config'].search([('name', '=', 'My Bot')])
bot_config.send_telegram_message('Hello, this is a message from Odoo!', chat_id='123456789')
```

#### 3. Test Bot Configuration
```python
bot_config.action_send_test_message()
```

### Webhook Setup

To receive messages from Telegram, you need to configure the webhook URL in Telegram:

1. Make sure your Odoo instance is accessible from the internet
2. Set the webhook URL using the Telegram Bot API:
   ```
   https://api.telegram.org/bot<BOT_TOKEN>/setWebhook?url=https://yourodoodomain.com/telegram/webhook
   ```

### Message Handling

When a message is received by the webhook, it follows this process:

1. The message data is extracted from the request
2. The data is validated to ensure it contains all required fields
3. A new record is created in `telegram.message.log` with the direction 'in'
4. A confirmation response is sent back to Telegram

When sending a message:

1. The `send_telegram_message` method is called with the message content and chat ID
2. The method makes a POST request to the Telegram API
3. The response is processed and a new record is created in `telegram.message.log` with the direction 'out'

### Security Considerations

- The webhook endpoint uses public authentication to receive data from Telegram
- Bot tokens are stored in the database and protected by Odoo's security model
- The module uses `sudo()` when creating log entries to ensure proper access rights

### Integration with Other Odoo Modules

The Telegram Connector is designed to be extended by other modules:

- Both models inherit from `mail.thread` and `mail.activity.mixin` for chatter support
- The message logs can be queried by other modules for further processing
- Additional business logic can be implemented to respond to specific messages

### Deployment Instructions

1. Install the module through Odoo's module installation interface
2. Configure your Telegram bot in the Configuration menu
3. Set up the webhook URL in Telegram to point to your Odoo instance
4. Test the configuration using the "Send Message Test" button

### Best Practices

- **Security:**
  - Validate all incoming data from webhooks
  - Keep bot tokens secure and never share them

- **Performance:**
  - Monitor the number of messages being processed
  - Consider implementing rate limiting for high-volume bots

- **Error Handling:**
  - Check log entries for error messages
  - Implement proper exception handling in custom extensions

### References

1. [Telegram Bot API Documentation](https://core.telegram.org/bots/api)
2. [Odoo Development Documentation](https://www.odoo.com/documentation/16.0/developer.html)
3. [Python Requests Library](https://docs.python-requests.org/)
4. [JSON Processing in Python](https://docs.python.org/3/library/json.html)