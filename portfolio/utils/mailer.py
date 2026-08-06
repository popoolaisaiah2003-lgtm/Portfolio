import smtplib
from email.message import EmailMessage

from flask import current_app


class EmailDeliveryError(RuntimeError):
    """Raised when a contact message cannot be delivered."""


def send_contact_email(form):
    username = current_app.config["MAIL_USERNAME"]
    password = current_app.config["MAIL_PASSWORD"]

    if not username or not password:
        raise EmailDeliveryError("Email delivery is not configured.")

    safe_subject = " ".join(form.subject.data.splitlines()).strip()
    message = EmailMessage()
    message["Subject"] = f"KayDev portfolio inquiry: {safe_subject}"
    message["From"] = current_app.config["MAIL_DEFAULT_SENDER"] or username
    message["To"] = current_app.config["MAIL_RECIPIENT"]
    message["Reply-To"] = form.email.data
    message.set_content(
        "New portfolio contact submission\n\n"
        f"Name: {form.full_name.data}\n"
        f"Email: {form.email.data}\n"
        f"Subject: {safe_subject}\n\n"
        f"Message:\n{form.message.data}"
    )

    try:
        with smtplib.SMTP(
            current_app.config["MAIL_SERVER"],
            current_app.config["MAIL_PORT"],
            timeout=current_app.config["MAIL_TIMEOUT"],
        ) as smtp:
            if current_app.config["MAIL_USE_TLS"]:
                smtp.starttls()
            smtp.login(username, password)
            smtp.send_message(message)
    except (OSError, smtplib.SMTPException) as error:
        current_app.logger.exception("Contact email delivery failed")
        raise EmailDeliveryError("The message could not be delivered.") from error