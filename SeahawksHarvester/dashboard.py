import tkinter as tk
from tkinter import scrolledtext, messagebox
from tkinter import ttk
from harvester import scan_network
import json

last_scan_results = []  # Variable globale pour stocker les résultats du dernier scan
    
import os
import subprocess
from tkinter import messagebox

def update_from_github():
    try:
        # Lancer la commande git pull
        result = subprocess.run(["git", "pull"], cwd=os.getcwd(), capture_output=True, text=True)
        
        if "Already up to date." in result.stdout:
            messagebox.showinfo("Mise à jour", "L'application est déjà à jour.")
        else:
            messagebox.showinfo("Mise à jour réussie. Redémarrez l'application.")
    except Exception as e:
        messagebox.showerror("Erreur", f"Impossible de mettre à jour : {str(e)}")

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
        
        # Mise à jour de la barre de progression
        total_hosts = len(scan_results)
        progress_bar["maximum"] = total_hosts
        for i, host in enumerate(scan_results):
            results_text.insert(tk.END, f"Host: {host['host']}, State: {host['state']}\n")
            progress_bar["value"] = i + 1
            window.update()
        
        results_text.insert(tk.END, "Scan terminé.\n")
        last_scan_results = scan_results  # Stocker les résultats pour une éventuelle sauvegarde

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
        messagebox.showerror("Erreur", f"Impossible de sauvegarder les résultats : {str(e)}")

# Fenêtre principale
window = tk.Tk()
window.title("Seahawks Harvester - Interface Graphique")
window.geometry("600x600")

# Zone de texte pour afficher les résultats
results_text = scrolledtext.ScrolledText(window, width=70, height=20)
results_text.pack(pady=10)

# Champ de saisie pour la plage d’adresses IP
ip_label = tk.Label(window, text="Plage d'adresses IP :")
ip_label.pack()
ip_entry = tk.Entry(window, width=50)
ip_entry.insert(0, "192.168.1.0/24")
ip_entry.pack()

# Champ de saisie pour les ports
ports_label = tk.Label(window, text="Ports à scanner :")
ports_label.pack()
ports_entry = tk.Entry(window, width=50)
ports_entry.insert(0, "1-1024")
ports_entry.pack()

# Barre de progression
progress_bar = ttk.Progressbar(window, orient="horizontal", length=500, mode="determinate")
progress_bar.pack(pady=10)

# Bouton pour lancer le scan
scan_button = tk.Button(window, text="Lancer le scan", command=start_scan)
scan_button.pack(pady=10)

# Mettre à jour 
update_button = tk.Button(window, text="Mettre à jour l'application", command=update_from_github)
update_button.pack(pady=5)

# Bouton pour sauvegarder les résultats 
save_button = tk.Button(window, text="Sauvegarder les résultats", command=save_results)
save_button.pack(pady=5)

# Lancer la boucle principale de Tkinter
window.mainloop()