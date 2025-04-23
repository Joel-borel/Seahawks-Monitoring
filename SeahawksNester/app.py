import requests
from flask import Flask, render_template 

app = Flask(__name__)  # Correction ici : __name_ au lieu de name


@app.route('/')
def dashboard():
    try:
        response = requests.get("http://nester_api:8000/sondes")
        response.raise_for_status()
        scan_results = response.json()
    except Exception as e:
        print(f"Erreur API : {e}")
        scan_results = []

    return render_template("dashboard.html", results=scan_results)


# === NOUVELLE ROUTE : rapport de scan d'une sonde ===
@app.route('/scan/<int:sonde_id>')
def rapport_scan(sonde_id):
    try:
        response = requests.get(f"http://nester_api:8000/sondes/{sonde_id}/dernier-scan")
        response.raise_for_status()
        rapport = response.json()
    except Exception as e:
        print(f"Erreur lors de la récupération du scan : {e}")
        rapport = None

    return render_template("rapport_scan.html", rapport=rapport)


if __name__ == "__main__":  # Correction ici aussi
    app.run(host="0.0.0.0",port=5000)