Tutorial from https://www.thepythoncode.com/article/building-network-scanner-using-scapy

Breakdown by ChatGPT: 

This script uses the Scapy library to perform an ARP scan on a target IP range (192.168.1.1/24 in this case) by broadcasting ARP requests on the network. It creates an ARP packet and an Ether broadcast packet, then combines them and sends them using the srp() function. The script waits for responses from devices on the network, and adds the IP and MAC addresses of responding devices to a list called "clients". The script then prints the IP and MAC addresses of all the clients found on the network. This script is useful for discovering all the devices that are currently connected to a network.

Additional notes (by me): 

To check the IP address of your router:
Open Command Prompt, type ipconfig. Look for "Default Gateway" under your Ethernet or Wireless adapter, that will give you the IP address of your router.