import whois
import re
import requests
import socket
import dns.resolver
import time

# ============================
# Tela de banner inicial
# ============================
def banner():
    print(r"""
    =============================================
      _  _   ____  ____  _   _ _____ _____  
     | || | / ___||  _ \| | | |_   _| ____| 
     | || || |    | |_) | |_| | | | |  _|   
     |__   _| |___ |  __/|  _  | | | | |___  
        |_|  \____||_|   |_| |_| |_| |_____| 
    =============================================
         OSINT Tool - Cyber Intelligence
    """)
    print("\nBem-vindo à Ferramenta OSINT!")
    print("Escolha uma das opções abaixo:\n")
    print("1. OSINT Empresarial")
    print("2. OSINT Pessoa Física")
    print("3. Validação de Dados")
    print("4. Sair")

# ============================
# Medir tempo
# ============================
def medir_tempo(func):
    def wrapper(*args, **kwargs):
        inicio = time.time()
        resultado = func(*args, **kwargs)
        fim = time.time()
        print(f"\n[INFO] Tempo gasto em {func.__name__}: {fim - inicio:.2f} segundos.")
        return resultado
    return wrapper

# ============================
# WHOIS - OSINT Empresarial
# ============================
@medir_tempo
def get_whois(domain):
    try:
        w = whois.whois(domain)
        print("\n[ WHOIS Information ]")
        print(f"Domain: {w.domain_name}")
        print(f"Registrar: {w.registrar}")
        print(f"Creation Date: {w.creation_date}")
        print(f"Expiration Date: {w.expiration_date}")
        print(f"Emails: {w.emails}")
        print(f"Status: {w.status}")
        print(f"Country: {w.country}")

        try:
            ip_address = socket.gethostbyname(domain)
            print(f"\n[ IP Address ]")
            print(f"IP Address: {ip_address}")
            reverse_ip_lookup(ip_address)
        except Exception as e:
            print("Erro ao buscar o endereço IP: ", e)

        print("\n[ DNS Servers ]")
        if w.name_servers:
            for server in w.name_servers:
                print(f'DNS: {server}')
        else:
            print('Nenhum servidor DNS encontrado.')
    except Exception as e:
        print(f'Erro ao buscar dados WHOIS: {e}')

# =============================
# Reverse IP Lookup
# =============================
@medir_tempo
def reverse_ip_lookup(ip):
    try:
        print("\n[ Reverse IP Lookup ]")
        url = f"https://api.hackertarget.com/reverseiplookup/?q={ip}"
        response = requests.get(url, timeout=10)

        if response.status_code == 200:
            result = response.text.strip()
            if result:
                print(f"Domínios hospedados no IP {ip}:\n{result}")
            else:
                print(f"Nenhum domínio encontrado para o IP: {ip}")
        else:
            print("Falha no Reverse IP lookup. Verifique sua conexão ou API.")
    except Exception as e:
        print(f"Erro ao realizar reverse IP lookup: {e}")

# ============================
# Busca de Usuários
# ============================
@medir_tempo
def username_lookup(username):
    print(f"\nBuscando informações sobre o usuário: {username}")

    social_platforms = {
        "GitHub": f"https://github.com/{username}",
        "Twitter": f"https://twitter.com/{username}",
        "Instagram": f"https://www.instagram.com/{username}/",
        "Reddit": f"https://www.reddit.com/user/{username}",
        "TikTok": f"https://www.tiktok.com/@{username}",
        "Facebook": f"https://www.facebook.com/{username}",
        "LinkedIn": f"https://www.linkedin.com/in/{username}",
        "Pinterest": f"https://www.pinterest.com/{username}/",
        "YouTube": f"https://www.youtube.com/{username}",
        "Medium": f"https://medium.com/@{username}",
        "Vimeo": f"https://vimeo.com/{username}",
        "Tumblr": f"https://{username}.tumblr.com",
        "DeviantArt": f"https://www.deviantart.com/{username}",
        "SoundCloud": f"https://soundcloud.com/{username}",
        "Flickr": f"https://www.flickr.com/people/{username}/",
        "Snapchat": f"https://www.snapchat.com/add/{username}",
    }

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0 Safari/537.36',
    }

    total_start_time = time.time()  # Tempo inicial total
    results = []

    for platform, url in social_platforms.items():
        start_time = time.time()  # Tempo inicial por plataforma
        try:
            response = requests.get(url, headers=headers, timeout=5)
            elapsed_time = time.time() - start_time  # Tempo gasto na requisição
            if response.status_code == 200:
                results.append((platform, url, f"{elapsed_time:.2f}s"))
                print(f"[+] Encontrado no {platform}: {url} (Tempo: {elapsed_time:.2f}s)")
            elif response.status_code == 404:
                print(f"[-] Não encontrado no {platform} (Tempo: {elapsed_time:.2f}s)")
            else:
                print(f"[!] Status inesperado no {platform}: {response.status_code} (Tempo: {elapsed_time:.2f}s)")
        except requests.RequestException as e:
            elapsed_time = time.time() - start_time
            print(f"[!] Erro ao acessar {platform}: {e} (Tempo: {elapsed_time:.2f}s)")

    total_elapsed_time = time.time() - total_start_time  # Tempo total
    print(f"\nBusca concluída! Tempo total: {total_elapsed_time:.2f}s")
    print("\nResumo:")
    for platform, url, elapsed_time in results:
        print(f"[+] {platform}: {url} (Tempo: {elapsed_time})")



        
# ============================
# Menu OSINT Empresarial
# ============================
@medir_tempo
def osint_empresarial():
    domain = input("\nDigite o domínio para análise WHOIS: ")
    if domain:
        get_whois(domain)
    else:
        print("Nenhum domínio fornecido. Tente novamente.")

# ============================
# Menu OSINT Pessoa Física
# ============================
@medir_tempo
def osint_pessoa():
    username = input("\nDigite o nome de usuário para busca: ")
    if username:
        username_lookup(username)
    else:
        print("Nenhum nome de usuário fornecido. Tente novamente.")

# ============================
# Menu Principal
# ============================
def main():
    inicio = time.time()
    while True:
        banner()
        choice = input("\nEscolha uma opção: ")

        if choice == "1":
            print("\n--- OSINT Empresarial ---")
            osint_empresarial()
        elif choice == "2":
            print("\n--- OSINT Pessoa Física ---")
            osint_pessoa()
        elif choice == "3":
            print("\nFunção de validação em breve.")
        elif choice == "4":
            fim = time.time()
            print(f"\n[INFO] Tempo total de execução: {fim - inicio:.2f} segundos.")
            print("\nSaindo... Até mais!")
            break
        else:
            print("\nOpção inválida. Tente novamente!")

# ============================
# Inicialização do Programa
# ============================
if __name__ == "__main__":
    main()
