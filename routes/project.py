from flask import request, make_response, Blueprint
from database.model import Project
from middlewear.middlewear import check_token
from flask_jwt_extended import jwt_required, get_jwt_identity

project = Blueprint('project', __name__)


# Get all Projects
@project.route('/getProject', methods=['Get'])
def get_project():
    try:
        tempProject = Project.objects().order_by('-id').to_json()
        return tempProject
    except:
        return make_response({"error": "Bad Request"}, 400)


# Post a Project
@project.route('/postProject', methods=['POST'])
@jwt_required
def post_project():
    try:
        userEmail = get_jwt_identity()
        token = request.headers['Authorization'].replace('Bearer ', '')
        tempUser = check_token(token, userEmail)
        if tempUser is None:
            return make_response({"error": "Forbidden"}, 403)
        else:
            body = request.get_json()
            tempProject = Project(**body)
            tempProject.save()
            return make_response({"completed": "true"}, 400)
    except:
        return make_response({"error": "Bad Request"}, 400)


# Delete a Project
@project.route('/deleteProject/<ID>', methods=['DELETE'])
@jwt_required
def delete_project(ID):
    try:
        userEmail = get_jwt_identity()
        token = request.headers['Authorization'].replace('Bearer ', '')
        tempUser = check_token(token, userEmail)
        if tempUser is None:
            return make_response({"error": "Forbidden"}, 403)
        else:
            tempProject = Project.objects.get(id=ID)
            tempProject.delete()
            return make_response({"deleted": "true"}, 200)
    except:
        return make_response({"error": "Bad Request"}, 400)
