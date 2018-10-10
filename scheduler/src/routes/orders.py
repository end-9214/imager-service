from bson import ObjectId
from flask import Blueprint, request, jsonify, Response
from jsonschema import validate, ValidationError
from werkzeug.security import check_password_hash, generate_password_hash

from utils.mongo import Orders
from . import authenticate, bson_object_id, errors


blueprint = Blueprint("order", __name__, url_prefix="/orders")


@blueprint.route("/", methods=["GET", "POST"])
@authenticate
def collection(user: dict):
    """
    List or create orders
    """

    if request.method == "GET":
        # check user permission
        if not user.get("scope", {}).get("orders", {}).get("read", False):
            raise errors.NotEnoughPrivilege()

        # unpack url parameters
        skip = request.args.get("skip", default=0, type=int)
        limit = request.args.get("limit", default=20, type=int)
        skip = 0 if skip < 0 else skip
        limit = 20 if limit <= 0 else limit

        orders = [order for order in Orders().find({})]

        return jsonify({"meta": {"skip": skip, "limit": limit}, "items": orders})
    elif request.method == "POST":
        # check user permission
        if not user.get("scope", {}).get("orders", {}).get("create", False):
            raise errors.NotEnoughPrivilege()

        # validate request json
        schema = {
            "type": "object",
            "properties": {
                "username": {"type": "string", "minLength": 1},
                "password": {"type": "string", "minLength": 6},
                "email": {"type": ["string", "null"]},
                "scope": {"type": "object"},
            },
            "required": ["username", "password"],
            "additionalProperties": False,
        }
        try:
            request_json = request.get_json()
            validate(request_json, schema)
        except ValidationError as error:
            raise errors.BadRequest(error.message)

        if Orders().count({"username": request_json["username"]}):
            raise errors.BadRequest("Username is already taken.")

        if Orders().count({"email": request_json["email"]}):
            raise errors.BadRequest("Email is already registered.")

        order_id = Orders().insert_one(request_json).inserted_id
        return jsonify({"_id": order_id})


@blueprint.route("/<string:user_id>", methods=["GET", "DELETE"])
@authenticate
@bson_object_id(["user_id"])
def document(user_id: ObjectId, user: dict):
    """ fetch indiviual order info or cancel it """
    if request.method == "GET":
        # check user permission when not querying current user
        if not user_id == ObjectId(user["_id"]):
            if not user.get("scope", {}).get("users", {}).get("read", False):
                raise errors.NotEnoughPrivilege()

        user = Users().find_one({"_id": user_id}, {"password_hash": 0})
        if user is None:
            raise errors.NotFound()

        return jsonify(user)
    elif request.method == "DELETE":
        # check user permission when not deleting current user
        if not user_id == ObjectId(user["_id"]):
            if not user.get("scope", {}).get("users", {}).get("delete", False):
                raise errors.NotEnoughPrivilege()

        deleted_count = Users().delete_one({"_id": user_id}).deleted_count
        if deleted_count == 0:
            raise errors.NotFound()

        return Response()


@blueprint.route("/<string:user_id>/password", methods=["PATCH"])
@authenticate
@bson_object_id(["user_id"])
def change_password(user_id: ObjectId, user: dict):
    # check user permission when not updating current user
    if not user_id == ObjectId(user["_id"]):
        if not user.get("scope", {}).get("users", {}).get("update", False):
            raise errors.NotEnoughPrivilege()

    request_json = request.get_json()

    # TODO: use json schema to validate
    password_old = request_json.get("old", None)
    password_new = request_json.get("new", None)
    if password_new is None or password_old is None:
        raise errors.BadRequest()

    user = Users().find_one({"_id": user_id}, {"password_hash": 1})
    if user is None:
        raise errors.NotFound()

    valid = check_password_hash(user["password_hash"], password_old)
    if not valid:
        raise errors.Unauthorized()

    Users().update_one(
        {"_id": ObjectId(user_id)},
        {"$set": {"password_hash": generate_password_hash(password_new)}},
    )
    return Response()
