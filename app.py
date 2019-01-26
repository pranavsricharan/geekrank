from tempfile import TemporaryDirectory
from zipfile import ZipFile

from flask import Flask, request
from flask_restplus import Resource, Api
import lib.executor as executor


app = Flask(__name__)
api = Api(app)


@api.route('/execute/<int:challenge_id>')
class ExecuteCode(Resource):
    def post(self, challenge_id):
        try:
            results = []

            # Create a temporary directory to store tests and scripts
            with TemporaryDirectory() as temp_dir:
                # Write submitted script to file
                script_file_path = temp_dir + '/script'
                with open(script_file_path, 'w') as f:
                    f.write(request.form['script'])

                # Extract test cases
                try:
                    challenge_tests_path = temp_dir + '/challenge'
                    challenge_file = ZipFile(request.files['tests'])
                    challenge_file.extractall(challenge_tests_path)
                except KeyError:
                    return {'error': 'Challenge test cases are required'}

                # Run the tests and generate response
                for k, v in executor.run_test_suite(challenge_tests_path, script_file_path).items():
                    result = {
                        'testCaseNumber': k,
                        'success': v == 'PASS'
                    }

                    if v != 'PASS':
                        result['errorMessage'] = v

                    results.append(result)
        except FileNotFoundError:
            return {'error': 'Invalid Challenge ID'}
        except KeyError:
            return {'error': 'User script is required'}

        return {'challengeResults': results}


if __name__ == '__main__':
    app.run(debug=True)
