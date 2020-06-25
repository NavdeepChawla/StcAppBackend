from flask import Flask, request, make_response, Blueprint
from database.model import User
from middlewear.middlewear import check_token
from flask_bcrypt import Bcrypt
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity


app = Flask(__name__)
bcrypt = Bcrypt(app)
user = Blueprint('user', __name__)


# User SignUp Route
@user.route('/signup', methods=['POST'])
def create_user():
    try:
        body = request.get_json()
        body['password'] = bcrypt.generate_password_hash(body['password'])
        User(**body).save()
        return make_response({"completed": "true"}, 200)
    except:
        return make_response({"error": "Bad Request"}, 400)


# User Login Route
@user.route('/login', methods=['POST'])
def sign_in_user():
    try:
        body = request.get_json()
        testUser = User.objects.get(email=body['email'])
        if bcrypt.check_password_hash(testUser.password, body['password']):
            access_token = create_access_token(identity=testUser.email)
            testUser.token.append(access_token)
            testUser.save()
            return make_response({"token": access_token}, 200)
        else:
            return make_response({"error": "Unauthorized"}, 401)
    except:
        return make_response({"error": "Bad Request"}, 400)


# User logout route
@user.route('/logout', methods=['POST'])
@jwt_required
def logout_user():
    try:
        userEmail = get_jwt_identity()
        token = request.headers['Authorization'].replace('Bearer ', '')
        tempUser = check_token(token, userEmail)
        if tempUser is None:
            return make_response({"error": "Forbidden"}, 403)
        else:
            tempUser.token.remove(token)
            tempUser.save()
            return make_response({"completed": "true"}, 200)
    except:
        return make_response({"error": "Bad Request"}, 400)


# User Delete Route
@user.route('/deleteUser', methods=['DELETE'])
def delete_user():
    try:
        body = request.get_json()
        tempUser = User.objects.get(email=body['email'])
        tempUser.delete()
        return make_response({"deleted": "true"}, 200)
    except:
        return make_response({"error": "Bad Request"}, 400)
