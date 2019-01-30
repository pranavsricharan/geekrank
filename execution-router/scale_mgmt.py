import redis
import docker
from pprint import pprint

storage = redis.Redis()
docker_client = docker.from_env()

container_port_map = {}

MIN_CONTAINERS = 1

for container in docker_client.containers.list():
    try:
        ports = container.attrs.get('NetworkSettings').get('Ports')
        if '5000/tcp' in ports:
            container_port_map[ports['5000/tcp']
                               [0].get('HostPort')] = container
    except:
        pass


print(container_port_map)

count = int(storage.get('gkr_hits').decode())
storage.set('gkr_hits', 0)


# Average execution time is 15 secs, or 4 cycles per minute
while int(count / 20) < storage.llen('gkr_registered'):
    host: str = storage.rpop().decode().rstrip('/')
    port_start = host.rfind(':') + 1
    port = host[port_start:]

    container_port_map[port].stop()
print(count)
