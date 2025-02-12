import nmap
import json

def scan_network(network='192.168.1.0/24', ports='1-1024'):
    scanner = nmap.PortScanner()
    print(f"Scanning {network} on ports {ports}...")
    result = scanner.scan(hosts=network, arguments=f'-p {ports}')
    
    hosts = []
    for host in result['scan']:
        state = result['scan'][host]['status']['state']
        hosts.append({"host": host, "state": state})
    
    return hosts

    # Sauvegarder les résultats dans un fichier JSON
    with open("scan_results.json", "w") as f:
        json.dump(hosts, f, indent=4)
    print("Résultats sauvegardés dans scan_results.json")

def main():
    print("Seahawks Harvester - Scan réseau démarré")
    scan_network()

if __name__ == "__main__":
    main()# ce commentaire est ajouté depuis Github
    
    
