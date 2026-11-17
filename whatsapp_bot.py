import time

import pyautogui
import pyperclip

from config import settings
from gemini_client import build_chat_session


def is_last_message_from_sender(chatlog: str, sender_name: str | None = None) -> bool:
    """Check whether the final non-empty copied line contains the target sender."""
    target = (sender_name or settings.whatsapp_sender_name).strip().casefold()
    if not target or not chatlog or not chatlog.strip():
        return False

    last_line = next((line.strip() for line in reversed(chatlog.splitlines()) if line.strip()), "")
    return target in last_line.casefold()


def run_bot() -> None:
    if not settings.gemini_api_key:
        raise ValueError("GEMINI_API_KEY is missing. Add your key to the local .env file.")

    print("Open the intended WhatsApp Web chat before continuing.")
    input("Press Enter when WhatsApp Web is ready, or Ctrl+C to exit: ")
    pyautogui.click(*settings.whatsapp_web_icon)
    time.sleep(settings.app_load_delay_seconds)
    chat_session = build_chat_session()

    while True:
        try:
            pyautogui.rightClick(*settings.right_click_position)
            time.sleep(settings.reply_delay_seconds)
            pyautogui.doubleClick(*settings.select_messages_option)
            time.sleep(settings.reply_delay_seconds)
            pyautogui.click()
            time.sleep(settings.reply_delay_seconds)
            pyautogui.hotkey("ctrl", "a")
            time.sleep(settings.reply_delay_seconds)
            pyautogui.hotkey("ctrl", "c")
            time.sleep(settings.reply_delay_seconds)

            chat_text = pyperclip.paste()
            if not chat_text.strip():
                print("No chat text was copied; retrying.")
                time.sleep(settings.reply_delay_seconds)
                continue

            if not is_last_message_from_sender(chat_text):
                time.sleep(settings.reply_delay_seconds)
                continue

            draft = chat_session.send_message(chat_text).text
            if not draft:
                print("Gemini returned an empty draft; skipping.")
                continue

            print(f"\nDraft reply:\n{draft}\n")
            if input("Send this reply? Type 'y' to approve: ").strip().casefold() != "y":
                print("Skipped.")
                continue

            pyperclip.copy(draft)
            pyautogui.click(*settings.reply_box)
            time.sleep(settings.reply_delay_seconds)
            pyautogui.hotkey("ctrl", "v")
            time.sleep(settings.reply_delay_seconds)
            pyautogui.press("enter")
            print("Approved reply sent.")

        except KeyboardInterrupt:
            print("Stopping bot.")
            break
        except Exception as exc:
            print(f"Error occurred: {exc}")
            time.sleep(5)
