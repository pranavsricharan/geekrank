import os

from flask import Flask, request, jsonify
from flask_restplus import Api, Resource, cors

from execution_environment_ctl import ExecutionEnvironmentCtl


app = Flask(__name__)
api = Api(app)


@api.route('/execute/<int:challenge_id>')
class Execute(Resource):
    @cors.crossdomain('*')
    def post(self, challenge_id: int):
        if os.path.exists(os.path.join(os.path.dirname(__file__), 'challenges/{}.zip'.format(challenge_id))):
            execution_ctl = ExecutionEnvironmentCtl()
            return jsonify(execution_ctl.execute(challenge_id, request.form.get('script'), request.form.get('language')))
        else:
            return {'error': 'Invalid challenge ID'}, 404


# @app.after_request
# def after_request(response):
#     print(response)
#     print('-------')
#     print(response.headers)
#     print(type(response.headers))
#     print(response.headers.__dict__)
#     response.headers._list.append(('Access-Control-Allow-Origin', '*'))
#     # response.headers.add('Access-Control-Allow-Origin', '*')


if __name__ == '__main__':
    app.run(debug=True, port=8030)
