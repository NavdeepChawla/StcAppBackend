from database.model import User


def check_token(userToken, email):
    tempUser = User.objects.get(email=email)
    if userToken in tempUser.token:
        return tempUser
    else:
        return None