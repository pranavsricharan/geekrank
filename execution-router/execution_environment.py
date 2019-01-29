import os
import time

import requests


class ExecutionEnvironment:
    def __init__(self, url):
        self.url = url

    def execute(self, challenge_id, script, language='PYTHON'):
        print(script)
        attempts = 0
        while attempts < 3:
            time.sleep(attempts+1)
            try:
                print('executing! attempt:', attempts + 1)
                open(os.path.dirname(__file__) +
                     '/challenges/{}.zip'.format(challenge_id))
                data = requests.post(self.url + '/execute', data={
                    'language': language,
                    'script': script,
                }, files={
                    'tests': open(os.path.dirname(__file__) + '/challenges/{}.zip'.format(challenge_id), 'rb')
                }).json()
                print('returning')
                return data
            except:
                attempts += 1
