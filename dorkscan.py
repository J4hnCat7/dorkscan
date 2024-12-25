import argparse
import requests
import os
from bs4 import BeautifulSoup
from colorama import Fore, init
import urllib.parse

# Inicializa a colorama
init(autoreset=True)

def list_scripts():
    scripts_folder = 'scripts'
    
    # Verifica se a pasta 'scripts' existe
    if os.path.exists(scripts_folder) and os.path.isdir(scripts_folder):
        # Lista todos os arquivos na pasta 'scripts'
        script_files = [f for f in os.listdir(scripts_folder) if os.path.isfile(os.path.join(scripts_folder, f))]
        
        if script_files:
            print(f"{Fore.GREEN}Scripts disponíveis:")
            for script in script_files:
                print(f"  {script}")
        else:
            print(f"{Fore.RED}Nenhum script encontrado na pasta 'scripts'.")
    else:
        print(f"{Fore.RED}A pasta 'scripts' não existe ou não foi encontrada.")

# Função para buscar resultados no Google
def fetch_results(query):
    """Função para buscar os resultados diretamente da pesquisa do Google e exibir de forma compacta."""
    url = f"https://www.google.com/search?q={query}"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        print(f"{Fore.RED}Erro ao realizar a busca. Tente novamente.")
        return
    
    soup = BeautifulSoup(response.text, "html.parser")
    results = soup.find_all('h3')

    # Exibindo os resultados de forma compacta
    if results:
        print(f"\n{Fore.GREEN}Resultados encontrados:")
        for result in results:
            link_tag = result.find_parent('a')
            link = link_tag['href']
            
            # Corrige o link para obter a URL real (sem parâmetros adicionais)
            if link.startswith("/url?q="):
                # Extrai o valor de q= e remove parâmetros extras após o primeiro '&'
                link = link[7:]  # Remove "/url?q="
                link = link.split('&')[0]  # Remove qualquer parâmetro após o primeiro "&"
            
            # Decodifica a URL para remover a codificação de caracteres especiais
            link = urllib.parse.unquote(link)
            
            title = result.get_text()
            print(f"{Fore.YELLOW}{title}: {Fore.CYAN}{link}")
    else:
        print(f"{Fore.YELLOW}Nenhum resultado encontrado para a pesquisa.")

# Função para executar o script de dork
def execute_script(script_file, url):
    scripts_folder = 'scripts'
    script_path = os.path.join(scripts_folder, script_file)
    
    # Lê o conteúdo do arquivo de script
    with open(script_path, 'r') as file:
        script_content = file.read()
    
    # Substitui o placeholder {url} pelo valor fornecido
    if '{url}' in script_content:
        if not url:
            print(f"{Fore.RED}Erro: O script '{script_file}' requer o parâmetro --url.")
            return
        script_content = script_content.replace("{url}", url)
    
    print(f"\n{Fore.YELLOW}Executando script: {script_file}\n{Fore.CYAN}{script_content}")
    
    # Realizando a busca no Google com o conteúdo do script
    headers = {"User-Agent": "Mozilla/5.0"}
    google_url = f"https://www.google.com/search?q={script_content}"
    response = requests.get(google_url, headers=headers)
    
    if response.status_code != 200:
        print(f"{Fore.RED}Erro ao realizar a busca. Tente novamente.")
        return
    
    soup = BeautifulSoup(response.text, "html.parser")
    results = soup.find_all('h3')

    # Exibindo os resultados de forma compacta
    if results:
        print(f"\n{Fore.GREEN}Resultados encontrados:")
        for result in results:
            link_tag = result.find_parent('a')
            link = link_tag['href']
            
            # Corrige o link para obter a URL real (sem parâmetros adicionais)
            if link.startswith("/url?q="):
                # Extrai o valor de q= e remove parâmetros extras após o primeiro '&'
                link = link[7:]  # Remove "/url?q="
                link = link.split('&')[0]  # Remove qualquer parâmetro após o primeiro "&"
            
            # Decodifica a URL para remover a codificação de caracteres especiais
            link = urllib.parse.unquote(link)
            
            title = result.get_text()
            print(f"{Fore.YELLOW}{title}: {Fore.CYAN}{link}")
    else:
        print(f"{Fore.YELLOW}Nenhum resultado encontrado para o dork.")

def main():
    parser = argparse.ArgumentParser(description="Dorkscan: uma ferramenta para buscas avançadas no Google usando dorks.")
    parser.add_argument("-F", "--file", type=str, help="Especifica o tipo de arquivo para a busca (ex.: pdf, php, etc.)")
    parser.add_argument("-u", "--url", type=str, help="Adiciona uma URL na pesquisa usando o formato site:{url}")
    parser.add_argument("--inurl", type=str, help="Especifica uma string que deve estar presente na URL (ex.: admin, login, etc.)")
    parser.add_argument("--intitle", type=str, help="Especifica uma string que deve estar no título da página")
    parser.add_argument("--intext", type=str, help="Especifica uma string que deve estar no conteúdo da página")
    parser.add_argument("--script", "-sC", type=str, help="Executa um script predefinido de scan")
    parser.add_argument("--list", "-l", action="store_true", help="Lista todos os scripts disponíveis")

    args = parser.parse_args()

    # Se o usuário deseja listar os scripts
    if args.list:
        list_scripts()
        return

    # Se o usuário especificar um script para executar
    if args.script:
        if args.url:
            execute_script(args.script, args.url)
        else:
            print(f"{Fore.RED}Erro: O script '{args.script}' requer o parâmetro --url.")
        return

    # Se a URL não for especificada, mostre um erro para buscas simples
    if not args.url and not args.list:
        print(f"{Fore.RED}Erro: A URL é obrigatória para buscas simples ou execução de scripts.")
        return

    query = f"site:{args.url} "

    if args.file:
        query += f"filetype:{args.file} "
    if args.inurl:
        query += f"inurl:{args.inurl} "
    if args.intitle:
        query += f"intitle:{args.intitle} "
    if args.intext:
        query += f"intext:{args.intext} "

    # Exibindo a consulta
    print(f"{Fore.YELLOW}Iniciando busca com o dork: {query.strip()}\n")

    # Buscar e exibir resultados
    fetch_results(query.strip())

if __name__ == "__main__":
    main()

