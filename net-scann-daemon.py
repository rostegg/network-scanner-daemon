#!/usr/bin/env python3
import argparse
import scapy.all as scapy
from scapy import sniff, ARP
import sys
from enum import Enum
import subprocess
import os
import requests
import csv
import datetime

arp_table = {}
cached_devices_list = {}
oui_cache = {}
arp_history = list()

oui_path = '/tmp/oui.csv'

def arp_monitor(packet):
    if packet[ARP].op == 2:
        if arp_table.get(packet[ARP].psrc) == None:
            print ("Register new device %s:%s"%(packet[ARP].hwsrc,packet[ARP].psrc))
            arp_table[packet[ARP].psrc] = packet[ARP].hwsrc
        elif arp_table.get(packet[ARP].psrc) and arp_table[packet[ARP].psrc] != packet[ARP].hwsrc:
            arp_history_obj = {
                "old_ip" : arp_table[packet[ARP].psrc],
                "new_ip" : packet[ARP].psrc,
                "date" : datetime.datetime.now().strftime("%H:%M:%S on %d.%m.%Y"),
                "mac" : packet[ARP].hwsrc
            }
            arp_history.append(arp_history_obj)
            #print("Detected spoofing, %s change his IP from %s to %s"%(packet[ARP].hwsrc, arp_table[packet[ARP].psrc], packet[ARP].psrc))
            arp_table[packet[ARP].psrc] = packet[ARP].hwsrc

def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--target", dest="target",
                        help="Target IP Range")
    parser.add_argument("-u", "--update-time", dest="update_time",
        help="Interval for scannig network")
    parser.add_argument("-a", "--arp-monitor", dest="enable_arp_monitor",
        help="Enable arp monitor mode")    
    options = parser.parse_args()
    return options

def vendor_by_mac(mac):
    return oui_cache[mac.replace(':','')[0:6].upper()]

def scan(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]  
    clients_list = []
    for element in answered_list:
        client_dict = {"ip": element[1].psrc, "mac": element[1].hwsrc, "vendor": vendor_by_mac(element[1].hwsrc)}
        clients_list.append(client_dict)
    return clients_list


def print_result(results_list):
    response = ""
    response += ("IP\t\t\tMAC Address\t\t\tVendor\n")
    response += ("%s\n"%("-"*90))
    for client in results_list:
        response += (("%s\t\t%s\t\t%s\n")%(client["ip"], client["mac"], client["vendor"]))
    response += ("%s"%("-"*90))
    return response


def update_oui():
    url = 'http://standards-oui.ieee.org/oui/oui.csv'
    response = requests.get(url)
    with open(oui_path, 'wb') as f:
        f.write(response.content)

def load_oui_data():
    if (not os.path.isfile(oui_path)):
        update_oui()
    with open(oui_path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count is not 0:
                oui_cache[row[1]] = row[2]
            line_count += 1


def main():
    load_oui_data()
    pass
# for choosing interface to sniff set: iface="iface_name"
print("Start sniff")
sniff(prn=arp_monitor,filter="arp",store=0)

print("Im here")
#load_oui_data()
#options = get_arguments()
#scan_result = scan(options.target)
#print(print_result(scan_result))
