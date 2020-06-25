from flask import request, make_response, Blueprint
from database.model import Article
from middlewear.middlewear import check_token
from flask_jwt_extended import jwt_required, get_jwt_identity

article = Blueprint('article', __name__)


# Get all Articles
@article.route('/getArticle/<domain>', methods=['Get'])
def get_article(domain):
    try:
        if domain is None:
            return make_response({"error": "Domain Not Found"}, 404)
        tempArticle = Article.objects(domain=domain).order_by('-id').to_json()
        return tempArticle
    except:
        return make_response({"error": "Bad Request"}, 400)


# Post an Article
@article.route('/postArticle', methods=['POST'])
@jwt_required
def post_article():
    try:
        userEmail = get_jwt_identity()
        token = request.headers['Authorization'].replace('Bearer ', '')
        tempUser = check_token(token, userEmail)
        if tempUser is None:
            return make_response({"error": "Forbidden"}, 403)
        else:
            body = request.get_json()
            tempArticle = Article(**body)
            tempArticle.save()
            return make_response({"completed": "true"}, 200)
    except:
        return make_response({"error": "Bad Request"}, 400)


# Delete an Article
@article.route('/deleteArticle/<ID>', methods=['DELETE'])
@jwt_required
def delete_article(ID):
    try:
        userEmail = get_jwt_identity()
        token = request.headers['Authorization'].replace('Bearer ', '')
        tempUser = check_token(token, userEmail)
        if tempUser is None:
            return make_response({"error": "Forbidden"}, 403)
        else:
            tempArticle = Article.objects.get(id=ID)
            tempArticle.delete()
            return make_response({"deleted": "true"}, 200)
    except:
        return make_response({"error": "Bad Request"}, 400)
