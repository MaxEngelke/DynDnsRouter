from cmath import log
import subprocess
import psutil
import time
import logging

def get_socat_pids():
    socat_pids = []
    for p in psutil.process_iter():
        if p.name().find('socat') != -1 and p.status() != psutil.STATUS_ZOMBIE:
            socat_pids.append(p.pid)

    return socat_pids


def start_socat_process_ip_to_ipv6_tunnel(protocol, portIn, destIp, portOut):
    protocolIn = protocol.upper() + '-LISTEN'
    source = portIn + ",fork,reuseaddr"
    protocolOut = protocol.upper() + '6'
    dest = '[{0}]:{1}'.format(destIp, portOut)
    return start_socat_process_tunnel(protocolIn, source, protocolOut, dest)


def start_socat_process_ipv4_to_ipv6_tunnel(protocol, portIn, destIp, portOut):
    protocolIn = protocol.upper() + '4-LISTEN'
    source = portIn + ",fork,reuseaddr"
    protocolOut = protocol.upper() + '6'
    dest = '[{0}]:{1}'.format(destIp, portOut)
    logging.info(f"Start socat with ${protocolIn} from ${source} to ${dest} with ${protocolOut}")
    return start_socat_process_tunnel(protocolIn, source, protocolOut, dest)


def start_socat_process_ipv6_to_ipv6_tunnel(protocol, portIn, destIp, portOut):
    protocolIn = protocol.upper() + '6-LISTEN'
    source = portIn + ",fork,reuseaddr"
    protocolOut = protocol.upper() + '6'
    dest = '[{0}]:{1}'.format(destIp, portOut)
    logging.info(f"Start socat with ${protocolIn} from ${source} to ${dest} with ${protocolOut}")
    return start_socat_process_tunnel(protocolIn, source, protocolOut, dest)


def start_socat_process_tunnel(protocolIn, source, protocolOut, destination):
    p = subprocess.Popen(['/usr/bin/socat', '{0}:{1}'.format(protocolIn.upper(), source), '{0}:{1}'.format(protocolOut, destination)])
    time.sleep(0.2)
    err = p.poll()
    return (p.pid, err)


def kill_all_socat_processes():
    for p in psutil.process_iter():
        if p.name().find('socat') != -1:
            p.terminate()


def terminate_process(pid):
    try:
        p = psutil.Process(pid)
        p.terminate()
        time.sleep(0.2)
    except:
        pass


def is_socat_process_running(pid):
    try:
        p = psutil.Process(pid)
        print(p.status())
        z = p.status() == psutil.STATUS_ZOMBIE
        d = p.status() == psutil.STATUS_DEAD
        return p.is_running() and p.status() != psutil.STATUS_ZOMBIE and p.status() != psutil.STATUS_DEAD
    except:
        return False