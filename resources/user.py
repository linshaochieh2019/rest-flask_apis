from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError
from passlib.hash import pbkdf2_sha256
from flask_jwt_extended import (
    create_access_token, 
    create_refresh_token, 
    get_jwt, 
    get_jwt_identity,
    jwt_required
)

from db import db
from models import UserModel, BlocklistModel
from schema import UserSchema

blp = Blueprint("Users", __name__, description="Operations on users")

@blp.route('/register')
class UserRegister(MethodView):
    
    @blp.arguments(UserSchema)
    def post(self, user_data):
        user = UserModel(
            username = user_data['username'],
            password = pbkdf2_sha256.hash(user_data['password'])
        )
        db.session.add(user)
        db.session.commit()
        return {"message": "A user was created."}, 201
    
@blp.route('/login')
class UserLogin(MethodView):
    @blp.arguments(UserSchema)
    def post(self, user_data):
        user = UserModel.query.filter(
            UserModel.username == user_data["username"]
            ).first()
        
        if user and pbkdf2_sha256.verify(user_data["password"], user.password):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(identity=user.id)
            return {
                "access_token": access_token,
                "refresh_toekn": refresh_token
            }
        
        abort(400, message="Invalid credentials.")
        
@blp.route('/refresh')
class UserRefresh(MethodView):
    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {"access_token": new_token}, 200


@blp.route('/logout')
class UserLogout(MethodView):
    @jwt_required()
    def delete(self):
        jti = get_jwt()["jti"]
        token_to_expire = BlocklistModel(jti=jti)
        try:
            db.session.add(token_to_expire)
            db.session.commit()
            return "", 204 #No content, successfully logged out
        except SQLAlchemyError as e:
            return {"message": "Access token failed to be stored."}


@blp.route('/user/<int:user_id>')
class User(MethodView):

    @blp.response(200, UserSchema)
    def get(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        return user
    
    def delete(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return {"message": "A user deleted."}, 200
    