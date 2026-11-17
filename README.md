# WhatsApp Gemini Reply Bot

A small Python desktop automation project that reads copied text from a WhatsApp Web chat, asks Google Gemini to draft a reply, and lets you review the draft before sending it.

> **Important:** This project interacts with a live WhatsApp Web session through screen coordinates. It is fragile, may break when the browser layout changes, and should only be used with the account owner's consent and in accordance with WhatsApp and Google policies. Sending is gated by a confirmation prompt; review every draft before approving it.

## Security: rotate the previously exposed key

An earlier version of `main.py` contained a Gemini API key in source code. Treat that key as compromised: **revoke it in Google AI Studio immediately and create a replacement**. This updated code does not include an API key. Store the replacement in your local `.env` file, which is ignored by Git. Never commit `.env` or paste a real key into an issue, pull request, or chat.

## Requirements

- Python 3.10 or later
- A Google Gemini API key
- WhatsApp Web open and logged in in a desktop browser
- A desktop session where PyAutoGUI mouse/keyboard automation is supported

## Setup

```bash
python -m venv .venv
# macOS/Linux
source .venv/bin/activate
# Windows PowerShell: .venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Create a local `.env` from the example and set your new key:

```bash
# macOS/Linux
cp .env.example .env
# Windows PowerShell: Copy-Item .env.example .env
```

Edit `.env` and set `GEMINI_API_KEY`. Adjust the sender and screen coordinates to match your own setup. Do not commit the edited `.env` file.

## Run

With WhatsApp Web open to the intended chat, run:

```bash
python main.py
```

The script copies chat text, drafts a response when the configured sender appears in the final non-empty line, and asks for approval in the terminal before pasting and sending. Type `y` to send; any other response skips that draft. Press `Ctrl+C` to stop.

Run the unit tests with:

```bash
python -m unittest discover -s tests -v
```

## Configuration

See `.env.example` for all supported settings:

- `GEMINI_API_KEY`: required; local secret, never commit it
- `GEMINI_MODEL`: model name (default: `gemini-1.5-pro`; change it if that model is unavailable to your account)
- `WHATSAPP_SENDER_NAME`: sender name used to decide whether to draft a response
- `BOT_NAME`, `BOT_REAL_NAME`, `BOT_LANGUAGE`: prompt/personality details
- `APP_LOAD_DELAY_SECONDS`, `REPLY_DELAY_SECONDS`: UI wait times
- `WHATSAPP_WEB_ICON`, `RIGHT_CLICK_POSITION`, `SELECT_MESSAGES_OPTION`, `REPLY_BOX`: `x,y` screen coordinates

Coordinates and copied-chat formatting are environment- and UI-dependent. The script does not use an official WhatsApp API and does not guarantee reliable message detection or delivery.

## Project layout

```text
main.py                 Application entry point
config.py               Environment-based settings
whatsapp_bot.py         Desktop automation and message approval flow
gemini_client.py        Gemini client and reply prompt
.env.example            Safe configuration template
requirements.txt        Python dependencies
tests/                  Unit tests for sender detection
```

## Limitations

- This is UI automation, not an official WhatsApp integration.
- Fixed screen coordinates can click the wrong place if the display, browser, or WhatsApp layout changes.
- The copied chat format can vary; test sender detection with your own setup before use.
- Gemini model availability depends on your Google account and API access.
- No automated end-to-end WhatsApp test is included; the tests only cover a local text helper.
