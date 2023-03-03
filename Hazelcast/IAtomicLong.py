import hazelcast as hz
import threading
import time
# Hazelcast stuff
start_time = time.time()
Client = hz.HazelcastClient(cluster_members=["192.168.137.1:5701", "192.168.137.1:5702", "192.168.137.1:5703"])
# IAtomicLong
counter = Client.cp_subsystem.get_atomic_long("counter").blocking()
# increments value
value = 0
def count():
    global value
    for i in range(10000):
        value = counter.add_and_get(1)

# run threads

def threads_run():
    threads = []
    for i in range(10):
        thread = threading.Thread(target=count)
        threads.append(thread)
        thread.start()
    for i in threads:
        i.join()
threads_run()
print(value)
print("--- %s seconds ---" % (time.time() - start_time))
Client.shutdown()
