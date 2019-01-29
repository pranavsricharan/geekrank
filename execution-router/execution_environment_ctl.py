import socket
import os

import redis

from execution_environment import ExecutionEnvironment


class ExecutionEnvironmentCtl:
    def __init__(self, redis_host='localhost', redis_port=6379):
        self.storage = redis.Redis(host=redis_host, port=redis_port)

    def _get_free_port(self):
        s = socket.socket()
        s.bind(('', 0))
        port = s.getsockname()[1]
        s.close()
        return port

    def execute(self, challenge_id, script, language='PYTHON'):
        print('executing')
        self.storage.incr('gkr_hits')  # Increase the hit counts for scaling

        if self.storage.llen('gkr_registered') == 0:
            env_port = self._get_free_port()
            print('found free port at {}'.format(env_port))
            os.system('sudo docker run -d -p {}:5000 geekrank'.format(env_port))
            print('created container')
            active_env = 'http://localhost:{}'.format(env_port)
        else:
            active_env = self.storage.lpop('gkr_registered').decode()

        print(active_env)
        result = ExecutionEnvironment(active_env).execute(
            challenge_id, script, language)
        print('Got result')
        print('result')
        print(result)
        self.storage.rpush('gkr_registered', active_env)  # End of the queue
        print('pushed back to redis')
        return result
