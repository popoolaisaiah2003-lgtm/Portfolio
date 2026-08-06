from flask import Blueprint, flash, redirect, render_template, url_for

from portfolio.forms import ContactForm
from portfolio.routes.project_data import PROJECTS
from portfolio.utils.mailer import EmailDeliveryError, send_contact_email


main_bp = Blueprint("main", __name__)


@main_bp.get("/")
def home():
    return render_template("index.html", projects=PROJECTS)


@main_bp.get("/about")
def about():
    return render_template("about.html")


@main_bp.route("/contact", methods=["GET", "POST"])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        try:
            send_contact_email(form)
        except EmailDeliveryError:
            flash("Your message could not be sent right now. Please email me directly.", "danger")
            return render_template("contact.html", form=form), 503

        flash("Thanks for reaching out. Your message has been sent successfully.", "success")
        return redirect(url_for("main.contact"))
    return render_template("contact.html", form=form)