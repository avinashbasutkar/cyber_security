from scapy.all import ARP, Ether, srp 

# IP Address of the target computer/device
target_ip = "192.168.0.1/24"

# Create ARP packet
arp = ARP(pdst=target_ip)

# Create the Ether broadcast packet 
# ff:ff:ff:ff:ff:ff MAC Address indicates broadcasting
ether = Ether(dst="ff:ff:ff:ff:ff:ff")

# stack them
packet = ether/arp

# Send and recieve the packets at layer 2, we set the timeout to 3 so the script won't get stuck
result = srp(packet, timeout=3)[0]

# result will be a list of pairs that is of the format (sent_packet, received_packet)
# iterating over them

# list of clients - will be filling it in upcoming loop
clients = []

for sent, received in result:
    # for each response, append IP and MAC address to clients list
    clients.append({'ip': received.psrc, 'mac': received.hwsrc})

# print clients
print("Available devices in the network:")
print("IP" + " "*18+"MAC")

for client in clients:
    print("{:16}    {}".format(client['ip'], client['mac']))