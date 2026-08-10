
#imports

import subprocess
import psutil
import time
from datetime import timedelta

# global variables







# Functions

def collect_sysdata():
    uptime_seconds = int(time.time() - psutil.boot_time())
    days = uptime_seconds // 86400
    hours = (uptime_seconds % 86400) // 3600
    minutes = (uptime_seconds & 86400) // 60
    seconds = uptime_seconds % 60

    uptime = f"{days}d {hours}h {minutes}m {seconds}s"

    







    cpu = psutil.cpu_percent(interval=1)
    cpucore = psutil.cpu_count()
    ram = psutil.virtual_memory().percent
    ramavail = psutil.virtual_memory().available
    ramtot = psutil.virtual_memory().total
    diskuse = psutil.disk_usage("/").percent
    diskav = psutil.disk_usage("/").free
    disktot = psutil.disk_usage("/").total
    networkdat = psutil.net_io_counters()
    
    #temp = sensors_temperatures()

    ramgb = ramavail / 1024**3
    ramtotgb = ramtot / 1024**3

    diskavgb = diskav / 1000**3
    disktotgb = disktot /1000**3


    return {
        "cpu" : cpu,
        "cpu_cores": cpucore,
        "ram_percent": ram,
        "ram_available": ramgb,
        "ram_total": ramtotgb,
        "disk_percent": diskuse,
        "disk_available": diskavgb,
        "disk_total": disktotgb,
        "network": networkdat,
        "uptime": uptime
    }





def print_title():
    print("============================")
    print("\n Server Sweeper Starting..")
    print("\n============================")



def display_system_stats(sysdata):

    print("\n------------------")
    print("System information")
    print("------------------")

    print(f"CPU Usage: {sysdata['cpu']} %")
    print(f"CPU Cores: {sysdata['cpu_cores']}")
    print(f"RAM Usage: {sysdata['ram_percent']:.2f} %")
    print(f"RAM Available: {sysdata['ram_available']:.2f}/{sysdata['ram_total']:.2f} GB")
    print(f"Disk Usage: {sysdata['disk_percent']:.2f} %")
    print(f"Disk Available: {sysdata['disk_available']:.2f}/{sysdata['disk_total']:.2f} GB")
    #print(f"Network Data: {sysdata['network']}")
    print(f"Uptime: {sysdata['uptime']}")
    


def check_vpn_status():
    vpn_status = subprocess.run(["docker", "ps", "--filter", "name=qbittorrent-vpn", "--format", "Status: {{.Status}}"],
    capture_output=True,
    text=True)
    return(vpn_status)

























# Function calls

sysdata = collect_sysdata()
print_title()
display_system_stats(sysdata)
print(check_vpn_status().stdout)