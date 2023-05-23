from flask import Blueprint, request

from application.extensions import db
from application.services.user_service import UserService


user_controller = Blueprint("user_controller", __name__)
user_service = UserService(db)


@user_controller.route("/users", methods=["GET"])
def get_users():
    sorting = request.args.get("sortby")
    return user_service.user_list(sorting)


@user_controller.route("/users/<int:uid>", methods=["GET"])
def get_user(uid):
    return user_service.user_by_id(uid)


@user_controller.route("/users", methods=["POST"])
def create_users():
    data = request.get_json()
    return user_service.create_user(data)


@user_controller.route("/users/<int:uid>/delete", methods=["POST"])
def delete_user(uid):
    return user_service.delete_user(uid)


@user_controller.route("/users/<int:uid>/modify", methods=["PUT"])
def modify_user(uid):
    data = request.get_json()
    return user_service.modify_user(uid, data)
