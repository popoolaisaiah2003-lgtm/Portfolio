from flask import Blueprint, abort, render_template

from portfolio.routes.project_data import PROJECTS


projects_bp = Blueprint("projects", __name__, url_prefix="/projects")


@projects_bp.get("/")
def index():
    return render_template("projects/index.html", projects=PROJECTS)


@projects_bp.get("/<slug>")
def detail(slug):
    project = PROJECTS.get(slug)
    if project is None:
        abort(404)
    return render_template("projects/detail.html", project=project, slug=slug)