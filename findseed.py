import os
import requests
import json
from multiprocessing import Process, Queue
import subprocess
import signal

import socket

old_getaddrinfo = socket.getaddrinfo
Q = Queue()

def new_getaddrinfo(args, *kwargs):
    resps = old_getaddrinfo(args, *kwargs)
    return [resp for resp in resps if resp[0] == socket.AF_INET]

socket.getaddrinfo = new_getaddrinfo

def display_seed(verif_data, seed):
    print(f"Seed Found({verif_data['iso']}): {seed}")
    print(f"Temp Token: {verif_data}\n")

def run_seed(filter):
    seed = ""
    while seed == "":
        resp = requests.get(
            f"https://fsg.opalstacked.com/?filter={filter}")
        res_json = resp.json()
        sseed = res_json.get("struct")
        sclass = res_json.get("class")
        randbiome = res_json.get("randbiome")
        pref = res_json.get("pref")  # village and/or shipwreck preference
        cmd = f'./bh {sseed} {sclass} {randbiome} {pref}'
        seed = os.popen(cmd).read().strip()
    display_seed(res_json, seed)
    Q.put(seed)


def run():
    print("[+] Started Seed Generation")

    with open('settings.json') as filter_json:
        read_json = json.load(filter_json)
        filter = read_json["filter"]
        num_processes = read_json["thread_count"]
    processes = []
    for i in range(num_processes):
        processes.append(Process(target=run_seed, args=(filter,)))
        processes[-1].start()
        
    i = 0
    while True:
        for j in range(len(processes)):
          
            if not processes[j].is_alive():
                for k in range(len(processes)):
                    processes[k].kill()
                    p = subprocess.Popen(['ps', '-A'], stdout=subprocess.PIPE)
                    out, err = p.communicate()
                    for line in out.splitlines():
                        if b'bh' in line:
                            pid = int(line.split(None, 1)[0])
                            os.kill(pid, signal.SIGKILL)
            
                return(Q.get())
        i = (i + 1) % num_processes
    
