#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
from src.crawler.core import qzone
from src.serve import Dao

import configparser


conf = configparser.ConfigParser()
conf.read("../resource/config.ini")

start = qzone
mongodb_address = conf.get("mongo", 'mongodb_address')
mongodb_db_name = conf.get("mongo", 'mongodb_db_name')
mongodb_table_name = conf.get("mongo", 'mongodb_table_name')
source_qzone_uin = conf.get("init", "source_qzone_uin")
source_qzone_password = conf.get("init", "source_qzone_password")
Dao.init_dao(mongodb_address, mongodb_db_name, mongodb_table_name)
start.get_login_info(source_qzone_uin, source_qzone_password)


app = Flask(__name__)
api = Api(app)

TODOS = {
    'todo1': {'task': 'build an API'},
    'todo2': {'task': '哈哈哈'},
    'todo3': {'task': 'profit!'},
}


def abort_if_todo_doesnt_exist(todo_id):
    if todo_id not in TODOS:
        abort(404, message="Todo {} doesn't exist".format(todo_id))


parser = reqparse.RequestParser()
parser.add_argument('task')


# Todo
# shows a single todo item and lets you delete a todo item
class Todo(Resource):
    def get(self, todo_id):
        abort_if_todo_doesnt_exist(todo_id)
        return TODOS[todo_id]

    def delete(self, todo_id):
        abort_if_todo_doesnt_exist(todo_id)
        del TODOS[todo_id]
        return '', 204

    def put(self, todo_id):
        args = parser.parse_args()
        task = {'task': args['task']}
        TODOS[todo_id] = task
        return task, 201


# TodoList
# shows a list of all todos, and lets you POST to add new tasks
class TodoList(Resource):
    def get(self):
        return TODOS

    def post(self):
        args = parser.parse_args()
        todo_id = int(max(TODOS.keys()).lstrip('todo')) + 1
        todo_id = 'todo%i' % todo_id
        TODOS[todo_id] = {'task': args['task']}
        return TODOS[todo_id], 201


class SrartCrawler(Resource):
    def get(self, qq_num):
        res = start.crawler_emotion(qq_num, 0, 10)
        Dao.store(res)
        return res


#
# Actually setup the Api resource routing here
#
api.add_resource(TodoList, '/todos')
api.add_resource(Todo, '/todos/<todo_id>')
api.add_resource(SrartCrawler, '/start/<qq_num>')

if __name__ == '__main__':
    # 将host设置为0.0.0.0，则外网用户也可以访问到这个服务
    app.run(host="0.0.0.0", port=8687, debug=True)
    # app.run(debug=True)