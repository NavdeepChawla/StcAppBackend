from flask import request, make_response, Blueprint
from database.model import Resource
from middlewear.middlewear import check_token
from flask_jwt_extended import jwt_required, get_jwt_identity

resource = Blueprint('resource', __name__)


# Get all Resources
@resource.route('/getResource/<domain>', methods=['Get'])
def get_resources(domain):
    try:
        if domain is None:
            return make_response({"error": "Domain Not Found"}, 404)
        tempResource = Resource.objects(domain=domain).order_by('-id').to_json()
        return tempResource
    except:
        return make_response({"error": "Bad Request"}, 400)


# Post a Resource
@resource.route('/postResource', methods=['POST'])
@jwt_required
def post_resource():
    try:
        userEmail = get_jwt_identity()
        token = request.headers['Authorization'].replace('Bearer ', '')
        tempUser = check_token(token, userEmail)
        if tempUser is None:
            return make_response({"error": "Forbidden"}, 403)
        else:
            body = request.get_json()
            tempResource = Resource(**body)
            tempResource.save()
            return make_response({"completed": "true"}, 200)
    except:
        return make_response({"error": "Bad Request"}, 400)


# Delete a Resource
@resource.route('/deleteResource/<ID>', methods=['DELETE'])
@jwt_required
def delete_resource(ID):
    try:
        userEmail = get_jwt_identity()
        token = request.headers['Authorization'].replace('Bearer ', '')
        tempUser = check_token(token, userEmail)
        if tempUser is None:
            return make_response({"error": "Forbidden"}, 403)
        else:
            tempResource = Resource.objects.get(id=ID)
            tempResource.delete()
            return make_response({"deleted": "true"}, 200)
    except:
        return make_response({"error": "Bad Request"}, 400)
