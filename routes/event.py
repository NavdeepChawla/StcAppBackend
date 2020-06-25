from flask import request, make_response, Blueprint
from database.model import Event
from middlewear.middlewear import check_token
from flask_jwt_extended import jwt_required, get_jwt_identity
# import base64

event = Blueprint('event', __name__)


# Get Events
@event.route('/getEvent', methods=['GET'])
def get_event():
    try:
        tempEvent = Event.objects().order_by('-id')
        return tempEvent.to_json()
    except:
        return make_response({"error": "Bad Request"}, 400)


# Post Event
@event.route('/postEvent', methods=['POST'])
@jwt_required
def post_event():
    try:
        userEmail = get_jwt_identity()
        token = request.headers['Authorization'].replace('Bearer ', '')
        tempUser = check_token(token, userEmail)
        if tempUser is None:
            return make_response({"error": "Forbidden"}, 403)
        else:
            body = request.get_json()
            tempEvent = Event(**body)
            tempEvent.save()
            return make_response({"completed": "true"}, 200)
    except:
        return make_response({"error": "Bad request"}, 400)


# Delete a Feed
@event.route('/deleteEvent/<ID>', methods=['DELETE'])
@jwt_required
def delete_event(ID):
    try:
        userEmail = get_jwt_identity()
        token = request.headers['Authorization'].replace('Bearer ', '')
        tempUser = check_token(token, userEmail)
        if tempUser is None:
            return make_response({"error": "Forbidden"}, 403)
        else:
            tempEvent = Event.objects.get(id=ID)
            tempEvent.delete()
            return make_response({"deleted": "true"}, 200)
    except:
        return make_response({"error": "Bad request"}, 400)


# Post Event Image
#@event.route('/postFeedImage/<ID>', methods=['POST'])
#jwt_required
#def post_event_image(ID):
#    try:
#       userEmail = get_jwt_identity()
#        token = request.headers['Authorization'].replace('Bearer ', '')
#        tempUser = check_token(token, userEmail)
#        if tempUser is None:
#            return make_response({"error": "true"}, 400)
#        else:
#            file = request.files['image']
#            imageStr = str(base64.b64encode(file.read()))
#            imageStr = imageStr[2:]
#            imageStr = imageStr[:-1]
#            tempEvent = Event.objects.get(id=ID)
#            tempEvent.image = imageStr
#            tempEvent.save()
#            return make_response({"completed": "true"}, 200)
#    except:
#        return make_response({"error": "true"}, 400)


