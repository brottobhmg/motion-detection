import bluetooth
import subprocess


target_mac_bt = "YOUR_MAC_DEVICE_BLUETOOTH"
target_mac = "YOUR_MAC_DEVICE_WIFI"

def scan_bluetooth(target_mac):
    if bluetooth.lookup_name(target_mac_bt, timeout=5)!=None:
        #print("Telefono rilevato tramite Bluetooth!")
        return True
    return False

def find_mac_in_arp(target_mac):
    result = subprocess.run(['arp', '-a'], capture_output=True, text=True)
    output = result.stdout
    if target_mac.lower() in output.lower():
        #print("Dispositivo trovato nella tabella ARP!")
        return True
    #print("Dispositivo non trovato nella tabella ARP.")
    return False

def detect_near_device():
    if find_mac_in_arp(target_mac) or scan_bluetooth(target_mac_bt):
        #print("Il telefono è nelle vicinanze.")
        return True
    else:
        #print("Il telefono non è nelle vicinanze.")
        return False


