from flask import request, make_response, Blueprint
from database.model import Feed
from middlewear.middlewear import check_token
from flask_jwt_extended import jwt_required, get_jwt_identity
# import base64

feed = Blueprint('feed', __name__)


# Get Feed
@feed.route('/getFeed', methods=['GET'])
def get_feed():
    try:
        body = request.get_json()
        limit = 5
        start = body['skip']
        end = start+limit
        tempFeed = Feed.objects().order_by('-id')[start:end]
        return tempFeed.to_json()
    except:
        return make_response({"error": "Bad Request"}, 400)


# Post Feed
@feed.route('/postFeed', methods=['POST'])
@jwt_required
def post_feed():
    try:
        userEmail = get_jwt_identity()
        token = request.headers['Authorization'].replace('Bearer ', '')
        tempUser = check_token(token, userEmail)
        if tempUser is None:
            return make_response({"error": "Forbidden"}, 403)
        else:
            body = request.get_json()
            tempFeed = Feed(**body)
            tempFeed.save()
            return make_response({"completed": "true"}, 200)
    except:
        return make_response({"error": "Bad Request"}, 400)


# Delete a Feed
@feed.route('/deleteFeed/<ID>', methods=['DELETE'])
@jwt_required
def delete_feed(ID):
    try:
        userEmail = get_jwt_identity()
        token = request.headers['Authorization'].replace('Bearer ', '')
        tempUser = check_token(token, userEmail)
        if tempUser is None:
            return make_response({"error": "Forbidden"}, 403)
        else:
            tempFeed = Feed.objects.get(id=ID)
            tempFeed.delete()
            return make_response({"deleted": "true"}, 200)
    except:
        return make_response({"error": "Bad Request"}, 400)


# Post Feed Image
# @feed.route('/postFeedImage/<ID>', methods=['POST'])
# @jwt_required
# def post_feed_image(ID):
#     try:
#         userEmail = get_jwt_identity()
#         token = request.headers['Authorization'].replace('Bearer ', '')
#         tempUser = check_token(token, userEmail)
#         if tempUser is None:
#             return make_response({"error": "true"}, 400)
#         else:
#             file = request.files['image']
#             imageStr = str(base64.b64encode(file.read()))
#             imageStr = imageStr[2:]
#             imageStr = imageStr[:-1]
#             tempFeed = Feed.objects.get(id=ID)
#             tempFeed.image = imageStr
#             tempFeed.save()
#             return make_response({"completed": "true"}, 200)
#     except:
#         return make_response({"error": "true"}, 400)
