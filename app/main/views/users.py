from flask import Blueprint, render_template, request
from sqlalchemy.exc import OperationalError

from .. import cache
from ..models.user import User

users_view = Blueprint("users_view", __name__, template_folder="../../templates")
"""Users View"""


@cache.cached(timeout=60)
@users_view.route("/", methods=["GET"])
@users_view.route("/users", methods=["GET"])
@users_view.route("/users/page/<int:page>", methods=["GET"])
def get_users(page=1):
    try:
        pagination = int(request.args.get("pagination"))
        pagination = 25 if pagination < 1 else pagination
    except Exception:
        pagination = 25
    try:
        users = User.query.paginate(page, per_page=pagination)
    except OperationalError:
        users = None
    return render_template("index.html", users=users, pagination=pagination)
