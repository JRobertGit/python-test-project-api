from flask import Blueprint, jsonify, request
from sqlalchemy.exc import OperationalError

from .. import cache
from ..models.user import User

users_api = Blueprint("users_api", __name__)
"""Users API"""


@cache.cached(timeout=60)
@users_api.route("/api/users/profiles", methods=["GET"])
def get_users():
    page = 1
    pagination = 25
    username = ""
    order = "id"

    try:
        query = request.args
        if "page" in query:
            page = int(query["page"])

        if "pagination" in query:
            pagination = int(query["pagination"])

        if "username" in query:
            username = query["username"]

        if "order_by" in query:
            if query["order_by"] in ["id", "type"]:
                order = query["order_by"]
    except Exception:
        users = None
        return jsonify(users), 400

    try:
        users = (
            User.query.filter(User.username.like("%" + username + "%"))
            .order_by(order)
            .paginate(page, per_page=pagination)
        )
    except OperationalError:
        users = None

    response = {}
    response["has_prev"] = users.has_prev
    response["has_next"] = users.has_next
    response["prev_num"] = users.prev_num
    response["next_num"] = users.next_num
    response["users"] = [
        {
            "id": user.id,
            "username": user.username,
            "image_url": user.image_url,
            "type": user.type,
            "profile_url": user.profile_url,
        }
        for user in users.items
    ]

    return jsonify(response), 200