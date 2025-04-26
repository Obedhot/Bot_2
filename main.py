import pyautogui
import time
import pyperclip
import google.generativeai as genai

# Configure API Key
genai.configure(api_key="AIzaSyCFwFmVKfpApeFw_DwnoMosOxsUFmMwoZ4")  # Replace with your actual API key

def is_last_message_from_sender(chatlog, sender_name="shahzaib"):
    messages = chatlog.strip().split("/2025] ")[-1]
    return sender_name in messages  # Simplified return statement

# Open WhatsApp Web
pyautogui.click(1134, 1036)  # Click on WhatsApp Web icon
time.sleep(5)  # Wait for WhatsApp Web to load

while True:
    try:
        # Step 1: Click on the latest chat message
        pyautogui.rightClick(639, 869)  # Click to open message menu
        time.sleep(1)  # Wait for menu to appear

        # Step 2: Move to "Select Messages" and click
        pyautogui.doubleClick(704, 716)  # Move to "Select Messages" option
        time.sleep(1)
        pyautogui.click()  # Click to activate selection mode
        time.sleep(1)  # Wait for selection mode to activate

        # Step 3: Select all messages and copy
        pyautogui.hotkey('ctrl', 'a')  # Select all
        time.sleep(1)
        pyautogui.hotkey('ctrl', 'c')  # Copy selected messages
        time.sleep(1)  # Ensure text is copied to clipboard

        # Step 4: Retrieve copied text
        text = pyperclip.paste()
        if not text.strip():
            print("Failed to copy text. Retrying...")
            continue  # Retry loop if no text is copied

        print("Copied Text:", text)

        if is_last_message_from_sender(text):
            # AI Chatbot Configuration
            generation_config = {
                "temperature": 0.7,
                "top_p": 0.9,
                "top_k": 40,
                "max_output_tokens": 1024,
                "response_mime_type": "text/plain",
            }

            # Initialize Chatbot Model
            model = genai.GenerativeModel(
                model_name="gemini-1.5-pro",
                generation_config=generation_config,
            )

            chat_session = model.start_chat(history=[
                {
                    "role": "user",
                    "parts": [{
                        "text": "You are a person named Mr.Knight who loves coding, science, and logic. "
                                "You talk in English and Roman Urdu, and your real name is Obed Nasir. "
                                "You love to joke and prefer Roman Urdu. Your answers are short and relevant "
                                "to the recent question in the chat. You are moody, short-tempered, and if someone abuses you, "
                                "you insult them back and teach them a lesson.be a real guy send real text message in chat message."
                    }]
                }
            ])

            # Get AI-generated response
            response = chat_session.send_message(text)
            response = response.text
            pyperclip.copy(response)

            # Step 5: Click on the reply box
            pyautogui.click(1039, 970)
            time.sleep(1)

            # Step 6: Paste response and send
            pyautogui.hotkey('ctrl', 'v')
            time.sleep(1)
            pyautogui.press('enter')

            print("Response sent successfully!")

    except Exception as e:
        print(f"Error occurred: {e}")
        time.sleep(5)  # Wait before retrying in case of an error
