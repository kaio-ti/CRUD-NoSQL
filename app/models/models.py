from datetime import datetime
from pymongo import MongoClient
from flask import jsonify

from exceptions.exceptions import InvalidCreationDataError, InvalidIDError, InvalidUpdateDataError, KeyMissingError

client = MongoClient('mongodb://localhost:27017/')
db = client['kenzie']
collection = db['posts']


class Post():

    def __init__(self, title, author, tags, content):
        self.title = title
        self.author = author
        self.tags = tags
        self.content = content
        self.updated_at = str(datetime.now().strftime('%d/%m/%y, %H:%M'))
        self.created_at = str(datetime.now().strftime('%d/%m/%y'))
        self.id = len(list(db.collection.find())) + 1
        

    @staticmethod
    def get_posts():
        post_list = list(db.collection.find())
        if len(post_list) > 0:
            for post in post_list:
                del post['_id']
            return {"data": post_list}, 200
        return {"data": []}, 200

    def get_specific_post(id):
        post_list = list(db.collection.find())
        for post in post_list:
            if post['id'] == id:
                del post['_id']
                return jsonify(post), 200
        return {"message": "Id não encontrado"}, 404

    def data_validation(**kwargs):

        validation = ['title', 'author', 'tags', 'content']

        for key in kwargs:
            if not key in validation:
                raise KeyMissingError(f'{key} inválido')
        for item in validation:
            if item not in (kwargs):
                raise   KeyMissingError(f'faltando a chave {key}')

        if type(kwargs['title']) != str or type(kwargs['author']) != str or type(kwargs['tags']) != list:
            raise InvalidCreationDataError

    def create_post(self):
        _id = db.collection.insert_one(self.__dict__).inserted_id
        if not _id:
            raise InvalidCreationDataError

        post = db.collection.find_one({'_id': _id})
        del post['_id']
        return post

    @staticmethod
    def delete_post_id(id):
        post_list = list(db.collection.find({"id": id}))
        if len(post_list) == 0:
            raise InvalidIDError
        
        db.collection.delete_one({"id": id})

        del post_list[0]['_id']

        return post_list

    @staticmethod
    def update_post_id(id, **kwargs):
        post_list = list(db.collection.find({"id": id}))
        validate = ['title', 'author', 'tags', 'content']

        if len(post_list) ==  0:
            raise InvalidIDError

        for key in kwargs:
            if not key in validate:
                raise InvalidUpdateDataError

        if type(kwargs['title']) != str or type(kwargs['author']) != str or type(kwargs['tags']) != list:
            raise InvalidUpdateDataError
        
        update = str(datetime.now().strftime('%d/%m/%y, %H:%M'))

        db.collection.update_one({"id": id}, {"$set": kwargs})
        db.collection.update_one({"id": id}, {"$set": {"updated_at": update}})

        new_list = list(db.collection.find({"id": id}))
        del new_list[0]['_id']
        return new_list
