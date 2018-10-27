import argparse

from flask import request, Flask, jsonify
from flask_apispec import FlaskApiSpec, use_kwargs

from argparseschema import parser_to_schema


def main():
    app = Flask('MySchemaApp')
    docs = FlaskApiSpec(app)

    parser = argparse.ArgumentParser()
    parser.add_argument('-x', dest='xvalue', type=str, help='the x value', default='hello')
    parser.add_argument('-y', dest='yvalue', type=int, help='the y value', default=10)

    MySchema = parser_to_schema(parser, 'MySchema')
    my_schema = MySchema()

    
    @docs.register
    @app.route('/api')
    @use_kwargs(MySchema, locations=['query'])
    def handler(**kwargs):
        obj = my_schema.load(kwargs)
        print('recv args: {}'.format(kwargs))
        print('recv obj: {}'.format(obj))
        return my_schema.dump(obj)

    return app

if __name__ == '__main__':
    app = main()
    app.run(debug=True, port=8080)
