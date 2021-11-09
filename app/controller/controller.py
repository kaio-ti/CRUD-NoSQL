from flask import Flask, request
from flask.json import jsonify
from app.models.models import Post
from exceptions.exceptions import InvalidCreationDataError, InvalidIDError, InvalidUpdateDataError

def init_app(app: Flask):

    @app.get('/posts')
    def read_posts():
        return Post.get_posts()

    @app.get('/posts/<int:id>')
    def read_post_by_id(id):
        return Post.get_specific_post(id)
    
    @app.post('/posts')
    def create_new_post():
        data = request.json
        try:
            Post.data_validation(**data)
            post = Post(**data)
            save_post = post.create_post()
            return save_post, 201
        except InvalidCreationDataError:
            return {"message": "Informações erradas"}, 400

    @app.delete('/posts/<int:id>')
    def delete_post(id):
        try:
            post_list = Post.delete_post_id(id)
            return jsonify(post_list), 200
        except InvalidIDError:
            return {"message": "Id inválido"}, 404

    @app.patch('/posts/<int:id>')
    def update_post(id):
        data = request.json

        try:
            post = Post.update_post_id(id, **data)
            return jsonify(post), 200
        except InvalidIDError:
            return {"message": "Id inválido"}, 404
        except InvalidUpdateDataError:
            return {"message": "Dados inválidos, atualização falhou"}, 400