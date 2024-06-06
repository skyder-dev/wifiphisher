import subprocess
import os

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
        print("\033[91mErreur lors de la récupération des réseaux WiFi.\033[0m")
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
            print("\033[92m[+]\033[0m Nom du SSID:", ssid)
            print("\033[92m[+]\033[0m Contenu de la clé:", key_content + "\033[0m")
        else:
            print("\033[91mInformations manquantes pour le réseau '{}'.\033[0m".format(network_name))
    except subprocess.CalledProcessError:
        print(f"\033[91mImpossible de trouver des informations pour le réseau '{network_name}'.\033[0m")

if __name__ == "__main__":
    clear_screen()
    logo = """
\033[34m
                                               ╦ ╦╦╔═╗╦╔═╗╦ ╦╦╔═╗╦ ╦╔═╗╦═╗
                                               ║║║║╠╣ ║╠═╝╠═╣║╚═╗╠═╣║╣ ╠╦╝
                                               ╚╩╝╩╚  ╩╩  ╩ ╩╩╚═╝╩ ╩╚═╝╩╚═

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
        print("\033[93mAucun réseau WiFi enregistré trouvé.\033[0m")
    else:
        print("\033[92mRéseaux WiFi enregistrés :\033[0m")
        clear_screen()
        print(logo)
        for index, network in enumerate(saved_networks, start=1):
            print(f"\033[94m{index}. {network}\033[0m")

        choice = input("\033[95mEntrez le numéro du réseau que vous souhaitez consulter : \033[0m")
        try:
            choice_index = int(choice)
            if choice_index < 1 or choice_index > len(saved_networks):
                raise ValueError
            selected_network = saved_networks[choice_index - 1]
            print("\033[92mVous avez choisi le réseau :\033[0m", selected_network)
            clear_screen()
            print(logo)
            show_network_info(selected_network)
        except (ValueError, IndexError):
            print("\033[91mChoix invalide.\033[0m")
            clear_screen()
            print(logo)
