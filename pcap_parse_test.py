from typing import Dict, List
from scapy.layers.inet import IP
from scapy.all import *
from tqdm import tqdm
from collections import defaultdict

class NetFlow:
    def __init__(self, packet: scapy.layers.inet.IP):
        self.source_ip = packet.src
        self.destination_ip = packet.dst
        self.ip_protocol_version = packet.version
        self.icmp_type_code = (0, 0)
        self.type_of_service = packet.tos

        if packet.haslayer(scapy.layers.inet.TCP):
            self.source_port = packet[scapy.layers.inet.TCP].sport
            self.destination_port = packet[scapy.layers.inet.TCP].dport
        elif packet.haslayer(scapy.layers.inet.UDP):
            self.source_port = packet[scapy.layers.inet.UDP].sport
            self.destination_port = packet[scapy.layers.inet.UDP].dport
        else:
            self.source_port = 0
            self.destination_port = 0

        if packet.haslayer(scapy.layers.inet.ICMP):
            self.icmp_type_code = (packet[scapy.layers.inet.ICMP].type, packet[scapy.layers.inet.ICMP].code)

    def __hash__(self):
        return hash((self.source_ip, self.destination_ip, self.ip_protocol_version, self.type_of_service,
                     self.source_port, self.destination_port, self.icmp_type_code))

    def __eq__(self, other):
        if isinstance(other, NetFlow):
            return (self.source_ip, self.destination_ip, self.ip_protocol_version, self.type_of_service,
                    self.source_port, self.destination_port, self.icmp_type_code) \
                == (other.source_ip, other.destination_ip, other.ip_protocol_version, other.type_of_service,
                    other.source_port, other.destination_port, other.icmp_type_code)
        return False

    def __str__(self):
        if self.icmp_type_code != (0, 0):
            return f"ICMP (type - {self.icmp_type_code[0]}, code - {self.icmp_type_code[1]}) {self.source_ip} --- {self.destination_ip} (ToS - {self.type_of_service})"

        if self.destination_port == 0 and self.source_port == 0:
            return f"IPv{self.ip_protocol_version} {self.source_ip} --- {self.destination_ip} (ToS - {self.type_of_service})"

        return f"IPv{self.ip_protocol_version} {self.source_ip}[{self.source_port}] --- {self.destination_ip}[{self.destination_port}] (ToS - {self.type_of_service})"

def split_pcap_by_netflow_and_count(pcap_file: str, output_dir: str):
    netflows = {}
    num_packets = 0

    def process_packet(pkt):
        nonlocal num_packets
        num_packets += 1
        print(num_packets)
        if pkt.haslayer(IP):
            netflow = NetFlow(pkt[IP])
            if netflow not in netflows:
                netflows[netflow] = []
            netflows[netflow].append(bytes(pkt))

    sniff(offline=pcap_file, prn=process_packet, store=0)

    num_netflows = len(netflows)

    for netflow, packets in netflows.items():
        output_file = f"{output_dir}/{netflow}.pcap"
        wrpcap(output_file, packets)

    print(f"Number of packets: {num_packets}")
    print(f"Number of netflows: {num_netflows}")


pcap_file = "D:/Загрузки/Dec2019_00013_20191206131500.pcap"
output_dir = "D:/pcapTest/netflows/Attack2/13"
split_pcap_by_netflow_and_count(pcap_file, output_dir)