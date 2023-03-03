import hazelcast as hz
import threading
import time

# Hazelcast stuff
start_time = time.time()
Client = hz.HazelcastClient(cluster_members=["192.168.137.1:5701", "192.168.137.1:5702", "192.168.137.1:5703"])
hz_map = Client.get_map("my-map").blocking()
hz_map.set("key", value=0)
value = 0

# increments "key" value
def counter():
    for i in range(10000):
        hz_map.lock("key")
        try:
            hz_map.set("key",  hz_map.get("key") + 1)
        finally:
            hz_map.unlock("key")

# run threads
def threads_run():
    threads = []
    for i in range(10):
        thread = threading.Thread(target=counter)
        threads.append(thread)
        thread.start()
    for i in threads:
        i.join()
threads_run()

get = hz_map.get("key")
print(get)
print("--- %s seconds ---" % (time.time() - start_time))
