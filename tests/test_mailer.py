import unittest
from types import SimpleNamespace
from unittest.mock import patch

from portfolio import create_app
from portfolio.utils.mailer import EmailDeliveryError, send_contact_email


class ContactMailerTests(unittest.TestCase):
    def setUp(self):
        self.app = create_app("testing")
        self.app.config.update(
            MAIL_USERNAME="popoolaisaiah2003@gmail.com",
            MAIL_PASSWORD="test-app-password",
            MAIL_DEFAULT_SENDER="popoolaisaiah2003@gmail.com",
            MAIL_RECIPIENT="popoolaisaiah2003@gmail.com",
        )
        self.form = SimpleNamespace(
            full_name=SimpleNamespace(data="Test User"),
            email=SimpleNamespace(data="visitor@example.com"),
            subject=SimpleNamespace(data="Website project"),
            message=SimpleNamespace(data="I would like to discuss a project."),
        )

    @patch("portfolio.utils.mailer.smtplib.SMTP")
    def test_message_uses_recipient_and_visitor_reply_to(self, smtp_class):
        smtp = smtp_class.return_value.__enter__.return_value

        with self.app.app_context():
            send_contact_email(self.form)

        smtp.starttls.assert_called_once_with()
        smtp.login.assert_called_once_with(
            "popoolaisaiah2003@gmail.com", "test-app-password"
        )
        message = smtp.send_message.call_args.args[0]
        self.assertEqual(message["To"], "popoolaisaiah2003@gmail.com")
        self.assertEqual(message["Reply-To"], "visitor@example.com")
        self.assertIn("I would like to discuss a project.", message.get_content())

    def test_missing_credentials_are_rejected(self):
        self.app.config["MAIL_PASSWORD"] = ""

        with self.app.app_context(), self.assertRaises(EmailDeliveryError):
            send_contact_email(self.form)


if __name__ == "__main__":
    unittest.main()