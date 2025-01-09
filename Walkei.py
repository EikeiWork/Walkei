import os
import secrets
import requests
from eth_keys import keys
from colorama import init, Fore
import ctypes  # Importer ctypes pour changer le titre de la fenêtre

# Initialiser colorama
init(autoreset=True)

# Fonction pour générer une clé privée Ethereum valide
def generate_valid_ethereum_private_key(existing_keys):
    while True:
        private_key = secrets.token_hex(32)  # 32 bytes = 64 hex chars
        private_key_int = int(private_key, 16)

        if 0 < private_key_int < 2**256:
            if private_key not in existing_keys:
                existing_keys.add(private_key)
                return private_key

# Fonction pour vérifier le solde
def check_balance(address):
    etherscan_api_key = 'YOUR_API_KEY_ETHERSCAN'  # Remplacez par votre clé API Etherscan
    url = f"https://api.etherscan.io/api?module=account&action=balance&address={address}&tag=latest&apikey={etherscan_api_key}"
    
    response = requests.get(url)
    data = response.json()

    if data['status'] == '1':
        balance_wei = int(data['result'])
        balance_eth = balance_wei / 10**18  # Conversion de Wei à ETH
        return balance_eth
    else:
        return None

# Chemin du fichier de travail
work_file_path = r'ENTER THE FOLDER TO  - work.txt'

# Utilisation des générateurs
if __name__ == "__main__":
    existing_keys = set()  # Ensemble pour garder les clés privées uniques
    attempt_count = 0  # Compteur de tentatives

    # Générer et afficher des clés privées, publiques et leur solde à l'infini
    try:
        while True:
            eth_private_key = generate_valid_ethereum_private_key(existing_keys)
            private_key_hex = f"0x{eth_private_key}"  # Clé privée avec le préfixe

            # Créer un objet clé privée
            private_key = keys.PrivateKey(bytes.fromhex(eth_private_key))

            # Dériver la clé publique
            public_key = private_key.public_key
            public_key_hex = f"0x{public_key.to_hex()}"  # Clé publique avec le préfixe

            # Vérifier le solde
            balance = check_balance(public_key_hex)

            # Incrémenter le compteur de tentatives
            attempt_count += 1

            # Mettre à jour le titre de la fenêtre cmd
            ctypes.windll.kernel32.SetConsoleTitleW(f'Tentative | [ {attempt_count} ]')

            # Afficher les clés et le solde
            print(f"[PRIVATE] CLE: {private_key_hex}")
            print(f"[PUBLIC] CLE: {public_key_hex}")
            if balance is not None:
                if balance > 0:
                    # Afficher en vert si le solde est supérieur à 0
                    print(f"{Fore.GREEN}[BALANCE] SOLDE: {balance} ETH\n")
                    # Écrire dans le fichier si le solde est supérieur à 0
                    with open(work_file_path, 'a') as work_file:
                        work_file.write(f"{private_key_hex}, {public_key_hex}, {balance} ETH\n")
                else:
                    # Afficher en rouge si le solde est 0
                    print(f"[BALANCE] SOLDE: {balance} ETH\n")
            else:
                print("[BALANCE] Erreur lors de la récupération du solde.\n")
    except KeyboardInterrupt:
        print("\nArrêt de la génération.")