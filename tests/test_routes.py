import unittest
from unittest.mock import patch

from portfolio import create_app


class PortfolioRouteTests(unittest.TestCase):
    def setUp(self):
        self.app = create_app("testing")
        self.client = self.app.test_client()

    def test_public_pages_render(self):
        pages = (
            "/",
            "/about",
            "/projects/",
            "/projects/kayhomes",
            "/projects/knotique",
            "/projects/yan-zhen-peptides",
            "/contact",
        )

        for page in pages:
            with self.subTest(page=page):
                self.assertEqual(self.client.get(page).status_code, 200)

    def test_unknown_page_uses_custom_404(self):
        response = self.client.get("/not-a-page")
        self.assertEqual(response.status_code, 404)
        self.assertIn(b"Page Not Found", response.data)

    @patch("portfolio.routes.main.send_contact_email")
    def test_valid_contact_form_sends_email_and_redirects(self, send_email):
        response = self.client.post("/contact", data=self.valid_contact_data())
        self.assertEqual(response.status_code, 302)
        send_email.assert_called_once()

    @patch("portfolio.routes.main.send_contact_email")
    def test_delivery_failure_keeps_form_visible(self, send_email):
        from portfolio.utils.mailer import EmailDeliveryError

        send_email.side_effect = EmailDeliveryError("Delivery failed")
        response = self.client.post("/contact", data=self.valid_contact_data())
        self.assertEqual(response.status_code, 503)
        self.assertIn(b"could not be sent", response.data)

    def test_invalid_contact_form_shows_feedback(self):
        response = self.client.post(
            "/contact",
            data={
                "full_name": "Test User",
                "email": "invalid",
                "subject": "Project inquiry",
                "message": "This is a valid test message.",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Invalid email address", response.data)

    @staticmethod
    def valid_contact_data():
        return {
            "full_name": "Test User",
            "email": "test@example.com",
            "subject": "Project inquiry",
            "message": "This is a valid test message.",
        }


if __name__ == "__main__":
    unittest.main()