from flask import Flask


class Group:
    def __init__(self, id, number):
        self.id = id
        self.number = number


class Student:
    def __init__ (self, id, group_id, full_name):
        self.id = id
        self.group_id = group_id
        self.full_name = full_name


def setup_routes(app):
    @app.route('/')
    def index():
        return 'aboba'


if __name__ == '__main__':
    app = Flask(__name__)
    
    setup_routes(app)
    
    app.run(host='127.0.0.1', port=8080, debug=True)