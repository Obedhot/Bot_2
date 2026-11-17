import unittest

from whatsapp_bot import is_last_message_from_sender


class SenderDetectionTests(unittest.TestCase):
    def test_detects_sender_on_final_nonempty_line_case_insensitively(self):
        chat = "Earlier message\n[date] Shahzaib: hi\n"
        self.assertTrue(is_last_message_from_sender(chat, "shahzaib"))

    def test_rejects_sender_when_another_person_is_last(self):
        chat = "[date] shahzaib: hi\n[date] Other: hello"
        self.assertFalse(is_last_message_from_sender(chat, "shahzaib"))

    def test_empty_input_and_empty_sender_are_rejected(self):
        self.assertFalse(is_last_message_from_sender("", "shahzaib"))
        self.assertFalse(is_last_message_from_sender("some text", ""))


if __name__ == "__main__":
    unittest.main()
