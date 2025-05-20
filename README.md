# 🤖 Odoo - Telegram Integration

Seamless integration between **Odoo ERP** and **Telegram Bot API** for real-time messaging, automation, and interaction with users and customers directly from your ERP.

![Odoo + Telegram](https://upload.wikimedia.org/wikipedia/commons/8/82/Telegram_logo.svg) <!-- Replace with your own repo image if needed -->

---

## 🔍 Overview

This module enables **real-time communication** between Odoo and Telegram users, allowing your system to send and receive messages, manage multiple bots, and log message history seamlessly.

### ✅ Key Features

* 🤖 **Multiple Bot Configuration**
* 📬 **Send Messages from Odoo to Telegram**
* 🔄 **Receive Messages via Webhook**
* 🕒 **Message Logging & Tracking**
* 🔐 **User Chat Binding and Verification**
* 🔧 **Customizable Telegram Handlers**

---

## 🧱 Architecture

This integration includes a unified Odoo module:

| Module              | Responsibilities                                          |
| -------------------| ---------------------------------------------------------- |
| `telegram_connector` | Handles bot configuration, message sending, webhook reception, and logging |

---

## ⚙️ Installation

### Requirements

* Odoo **16.0**
* Python **3.10+**
* Public domain or tunnel (e.g. `ngrok`, `cloudflared`)

### Steps

```bash
git clone https://github.com/doanmandev/odoo-telegram-integration.git
```

1. Copy `telegram_connector/` to your Odoo `addons` directory.
2. Add the path to your `odoo.conf` under `addons_path`.
3. Restart Odoo and update the apps list.
4. Install **"Telegram Connector"** from the Apps menu.

---

## 🔧 Configuration

### 1. Create Telegram Bot

* Talk to [@BotFather](https://t.me/BotFather)
* Use `/newbot` and follow instructions
* Save the generated **Bot Token**

### 2. Setup Bot in Odoo

* Go to **Telegram > Bot Configuration**
* Fill in the token and name
* Click **Check Connection**

### 3. Set Webhook

```bash
curl -X POST "https://api.telegram.org/bot<your_token>/setWebhook" \
     -d "url=https://yourdomain.com/telegram/webhook"
```

> You can also use `ngrok` or `cloudflared` for local development

---

## 🖠️ Usage Examples

### 🔹 Send Telegram Message

```python
self.env['telegram.service'].send_message(
    chat_id=123456789,
    text="Hello from Odoo!"
)
```

### 🔹 Log Incoming Messages

Telegram messages are logged in `telegram.message.log`, accessible via UI or ORM:
```python
logs = self.env['telegram.message.log'].search([], limit=10)
```

---

## 🧠 Advanced Features

* 🌐 **Webhook Dispatcher for Multiple Bots**
* 🔐 **Secure Chat ID Binding**
* 💬 **Message Context Parsing**
* 📊 **Telegram Usage Statistics**

---

## ✅ Best Practices

* Always validate the incoming Telegram payload
* Use environment-specific bot tokens
* Secure your webhook endpoint
* Log and monitor all outbound/inbound traffic
* Gracefully handle webhook retries and failures

---

## 🤝 Contributing

We welcome your ideas and improvements!

```bash
# Steps to contribute
1. Fork this repository
2. Create a new branch
3. Make your changes
4. Submit a Pull Request 🚀
```

---

## 📄 License

Licensed under the **LGPL-3.0**. See [LICENSE](./LICENSE) for details.

---

## 🤛 Contact

* **Author**: Doan Man
* 📧 **Email**: [doanman.dev@gmail.com](mailto:doanman.dev@gmail.com)

> ⚠️ *Note: This module is under active development. Feedback and PRs are appreciated!*

---