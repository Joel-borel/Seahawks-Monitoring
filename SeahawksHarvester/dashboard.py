import tkinter as tk
from tkinter import scrolledtext, messagebox
from tkinter import ttk
from harvester import scan_network
import json
import socket
import os
import subprocess

last_scan_results = []  # Stockage des résultats de scan

def update_from_github():
    try:
        result = subprocess.run(["git", "pull"], cwd=os.getcwd(), capture_output=True, text=True)
        if "Already up to date." in result.stdout:
            results_text.insert(tk.END, "L'application est déjà à jour.\n")
        else:
            results_text.insert(tk.END, "Mise à jour réussie. Redémarrez l'application.\n")
    except Exception as e:
        results_text.insert(tk.END, f"Erreur : Impossible de mettre à jour : {str(e)}\n")

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = "127.0.0.1"
    finally:
        s.close()
    return ip

def start_scan():
    global last_scan_results
    results_text.delete(1.0, tk.END)
    ip_range = ip_entry.get()
    ports = ports_entry.get()

    results_text.insert(tk.END, f"Début du scan sur {ip_range} (ports {ports})...\n")
    window.update()

    try:
        scan_results = scan_network(network=ip_range, ports=ports)
        if not scan_results:
            results_text.insert(tk.END, "Aucun hôte trouvé.\n")
            return

        progress_bar["maximum"] = len(scan_results)
        for i, host in enumerate(scan_results):
            results_text.insert(tk.END, f"Host: {host['host']}, State: {host['state']}\n")
            progress_bar["value"] = i + 1
            window.update()

        results_text.insert(tk.END, "Scan terminé.\n")
        last_scan_results = scan_results
    except Exception as e:
        results_text.insert(tk.END, f"Erreur : {str(e)}\n")

def save_results():
    if not last_scan_results:
        messagebox.showwarning("Attention", "Aucun résultat à sauvegarder.")
        return
    try:
        with open("scan_results.json", "w") as f:
            json.dump(last_scan_results, f, indent=4)
        messagebox.showinfo("Succès", "Résultats sauvegardés dans scan_results.json.")
    except Exception as e:
        messagebox.showerror("Erreur", f"Erreur lors de la sauvegarde : {str(e)}")

# --- Interface Graphique ---
window = tk.Tk()
window.title("Seahawks Harvester - Interface Graphique")
window.geometry("600x620")

# Résultats
results_text = scrolledtext.ScrolledText(window, width=70, height=20)
results_text.pack(pady=10)

# IP automatique
tk.Label(window, text="Plage d'adresses IP :").pack()
ip_entry = tk.Entry(window, width=50)
local_ip = get_local_ip()
network_prefix = ".".join(local_ip.split(".")[:3]) + ".0/24"
ip_entry.insert(0, network_prefix)
ip_entry.pack()

# Ports
tk.Label(window, text="Ports à scanner :").pack()
ports_entry = tk.Entry(window, width=50)
ports_entry.insert(0, "1-1024")
ports_entry.pack()

# Barre de progression
progress_bar = ttk.Progressbar(window, orient="horizontal", length=500, mode="determinate")
progress_bar.pack(pady=10)

# Boutons
tk.Button(window, text="Lancer le scan", command=start_scan).pack(pady=5)
tk.Button(window, text="Mettre à jour l'application", command=update_from_github).pack(pady=5)
tk.Button(window, text="Sauvegarder les résultats", command=save_results).pack(pady=5)
window.mainloop()