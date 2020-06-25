from flask import request, make_response, Blueprint
from database.model import Github
from middlewear.middlewear import check_token
from flask_jwt_extended import jwt_required, get_jwt_identity

github = Blueprint('github', __name__)


# Get all Github links
@github.route('/getGithub', methods=['Get'])
def get_github():
    try:
        tempGithub = Github.objects().order_by('-id').to_json()
        return tempGithub
    except:
        return make_response({"error": "Bad Request"}, 400)


# Post a Github link
@github.route('/postGithub', methods=['POST'])
@jwt_required
def post_github():
    try:
        userEmail = get_jwt_identity()
        token = request.headers['Authorization'].replace('Bearer ', '')
        tempUser = check_token(token, userEmail)
        if tempUser is None:
            return make_response({"error": "Forbidden"}, 403)
        else:
            body = request.get_json()
            tempGithub = Github(**body)
            tempGithub.save()
            return make_response({"completed": "true"}, 400)
    except:
        return make_response({"error": "Bad Request"}, 400)


# Delete a Github link
@github.route('/deleteGithub/<ID>', methods=['DELETE'])
@jwt_required
def delete_github(ID):
    try:
        userEmail = get_jwt_identity()
        token = request.headers['Authorization'].replace('Bearer ', '')
        tempUser = check_token(token, userEmail)
        if tempUser is None:
            return make_response({"error": "Forbidden"}, 403)
        else:
            tempGithub = Github.objects.get(id=ID)
            tempGithub.delete()
            return make_response({"deleted": "true"}, 200)
    except:
        return make_response({"error": "Bad Request"}, 400)