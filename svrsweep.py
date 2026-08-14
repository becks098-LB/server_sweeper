
#imports

import subprocess
import psutil
import time
from datetime import timedelta
import json

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

    try:
        diskavmnt1 = psutil.disk_usage("/mnt/storage").free
        diskavmnt1gb = diskavmnt1 / 1000**3
    except:
        diskavmnt1gb = None



    try:
        disktotmnt1 = psutil.disk_usage("/mnt/storage").total
        disktotmnt1gb = disktotmnt1 / 1000**3
    except:
        disktotmnt1gb = None



    
    

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
        #"network": networkdat,
        "uptime": uptime,
        "mntdisk1_available": diskavmnt1gb,
        "mntdisk1_total": disktotmnt1gb
    }





def print_title():
    print("============================")
    print("\n Server Sweeper Starting..")
    print("\n============================")



def display_system_stats(sysdata):

    print("\n------------------")
    print("System Status")
    print("------------------")
    print("")

    print(f"CPU Usage: {sysdata['cpu']} %")
    print(f"CPU Cores: {sysdata['cpu_cores']}")
    print(f"RAM Usage: {sysdata['ram_percent']:.2f} %")
    print(f"RAM Available: {sysdata['ram_available']:.2f}/{sysdata['ram_total']:.2f} GB")
    print(f"Local Disk Usage: {sysdata['disk_percent']:.2f} %")
    print(f"Server Uptime: {sysdata['uptime']}")
    #print(f"Local Disk Available: {sysdata['disk_available']:.2f}/{sysdata['disk_total']:.2f} GB")
    #print(f"Network Data: {sysdata['network']}")
    
    print("")
    print(f"Local Disk Available: {sysdata['disk_available']:.2f}/{sysdata['disk_total']:.2f} GB")
    if sysdata['mntdisk1_available'] is None:
        print("HDD 1 Not Mounted")
    else:
        print(f"HDD1: Available: {sysdata['mntdisk1_available']:.2f}/{sysdata['mntdisk1_total']:.2f} GB")

    


def check_vpn_status():
    print("\n--------------------")
    print("VPN Status (Torrent)")
    print("--------------------")
    print("                    ")

    vpn_status = subprocess.run(["docker", "ps", "--filter", "name=qbittorrent-vpn", "--format", "VPN Status: {{.Status}}"],
    capture_output=True,
    text=True)
   


    
    return(vpn_status)



def vpn_ip():

    public_ip = subprocess.run(["curl", "https://api.ipify.org"],
    capture_output=True,
    text=True)

    
    mullvad_ip = subprocess.run(["docker", "exec", "qbittorrent-vpn", "wget", "-qO-","https://api.ipify.org"],
    capture_output=True,
    text=True)

    public_ip = public_ip.stdout.strip()
    mullvad_ip = mullvad_ip.stdout.strip()



    if mullvad_ip == "":
        print("TORRENT VPN INACTIVE ❌")
    elif mullvad_ip == public_ip:
        print("TORRENT VPN INACTIVE ❌")
    else:
        print("TORRENT VPN ACTIVE ✅")


    print(f"public_ip: {public_ip}")
    print(f"mullvad_ip: {mullvad_ip}")

    return{
        "public_ip": public_ip,
        "mullvad_ip": mullvad_ip,
        "vpn_active": mullvad_ip != "" and mullvad_ip != public_ip
    }
    











def docker_overview():
    print("")
    print("-------------")
    print("Docker Status")
    print("-------------")
    print("")


def pihole_overview():
    print("")
    print("----------------")
    print("Adblocker Status")
    print("----------------")
    print("")
    pihole_status = subprocess.run(["docker", "ps", "-a", "--filter", "name=pihole","--format", "{{.Status}}"],
    capture_output=True,
    text=True)

    pihole_status = pihole_status.stdout.strip()

    return (pihole_status)








#the status_update json must be the final function

def status_update(sysdata, vpn_data):

    status_data = {
        "system": sysdata,
        "vpn_data": vpn_data
    }

    with open("status_database.json", "w") as file:
        json.dump(status_data, file, indent=4)



# Function calls and program run

sysdata = collect_sysdata()
print_title()
display_system_stats(sysdata)


print(check_vpn_status().stdout)
vpn_data = vpn_ip()

#pihole_overview = pihole_overview()
print(pihole_overview())



docker_overview = docker_overview()










status_update(sysdata, vpn_data)