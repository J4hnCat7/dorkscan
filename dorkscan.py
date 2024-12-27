import argparse
import requests
import os
from bs4 import BeautifulSoup
from colorama import Fore, init
import urllib.parse

init(autoreset=True)

def list_scripts():
    scripts_folder = 'scripts'
    
    if os.path.exists(scripts_folder) and os.path.isdir(scripts_folder):

        script_files = [f for f in os.listdir(scripts_folder) if os.path.isfile(os.path.join(scripts_folder, f))]
        
        if script_files:
            print(f"{Fore.GREEN}Scripts disponíveis:")
            for script in script_files:
                print(f"  {script}")
        else:
            print(f"{Fore.RED}Nenhum script encontrado na pasta 'scripts'.")
    else:
        print(f"{Fore.RED}A pasta 'scripts' não existe ou não foi encontrada.")

def fetch_results(query, show_all=False):
    """Função para buscar os resultados diretamente da pesquisa do Google e exibir de forma compacta."""
    url = f"https://www.google.com/search?q={query}"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        print(f"{Fore.RED}Erro ao realizar a busca. Tente novamente.")
        return
    
    soup = BeautifulSoup(response.text, "html.parser")
    
    if show_all:

        links = soup.find_all('a')
        if links:
            print(f"\n{Fore.GREEN}Todos os links encontrados:")
            for link_tag in links:
                link = link_tag.get('href')
                if link and link.startswith("/url?q="):

                    link = link[7:] 
                    link = link.split('&')[0]  
                    link = urllib.parse.unquote(link) 
                    print(f"{Fore.CYAN}{link}")
        else:
            print(f"{Fore.YELLOW}Nenhum link encontrado para a pesquisa.")
    else:

        results = soup.find_all('h3')
        if results:
            print(f"\n{Fore.GREEN}Resultados encontrados:")
            for result in results:
                link_tag = result.find_parent('a')
                link = link_tag['href']
                
                if link.startswith("/url?q="):

                    link = link[7:]  
                    link = link.split('&')[0] 
                    link = urllib.parse.unquote(link)  
                
                title = result.get_text()
                print(f"{Fore.YELLOW}{title}: {Fore.CYAN}{link}")
        else:
            print(f"{Fore.YELLOW}Nenhum resultado encontrado para a pesquisa.")

def execute_script(script_file, url, filetype=None, inurl=None, intitle=None, intext=None, show_all=False):
    scripts_folder = 'scripts'
    script_path = os.path.join(scripts_folder, script_file)
    
    with open(script_path, 'r') as file:
        script_content = file.read()
    
    if '{url}' in script_content:
        if not url:
            print(f"{Fore.RED}Erro: O script '{script_file}' requer o parâmetro --url.")
            return
        script_content = script_content.replace("{url}", url)
    
    if filetype:
        script_content += f" filetype:{filetype}"
    if inurl:
        script_content += f" inurl:{inurl}"
    if intitle:
        script_content += f" intitle:{intitle}"
    if intext:
        script_content += f" intext:{intext}"
    
    print(f"\n{Fore.YELLOW}Executando script: {script_file}\n{Fore.CYAN}{script_content}")
    
    headers = {"User-Agent": "Mozilla/5.0"}
    google_url = f"https://www.google.com/search?q={script_content}"
    response = requests.get(google_url, headers=headers)
    
    if response.status_code != 200:
        print(f"{Fore.RED}Erro ao realizar a busca. Tente novamente.")
        return
    
    soup = BeautifulSoup(response.text, "html.parser")
    fetch_results(script_content, show_all)

def main():
    parser = argparse.ArgumentParser(description="Dorkscan: uma ferramenta para buscas avançadas no Google usando dorks.")
    parser.add_argument("-F", "--file", type=str, help="Especifica o tipo de arquivo para a busca (ex.: pdf, php, etc.)")
    parser.add_argument("-u", "--url", type=str, help="Adiciona uma URL na pesquisa usando o formato site:{url}")
    parser.add_argument("--inurl", type=str, help="Especifica uma string que deve estar presente na URL (ex.: admin, login, etc.)")
    parser.add_argument("--intitle", type=str, help="Especifica uma string que deve estar no título da página")
    parser.add_argument("--intext", type=str, help="Especifica uma string que deve estar no conteúdo da página")
    parser.add_argument("--script", "-sC", type=str, help="Executa um script predefinido de busca (ex.: sql_injection_scan)")
    parser.add_argument("--list", "-l", action="store_true", help="Lista todos os scripts disponíveis")
    parser.add_argument("--all", "-a", action="store_true", help="Mostra todos os links encontrados na pesquisa")

    args = parser.parse_args()

    if args.list:
        list_scripts()
        return
        
    if args.script:
        execute_script(
            args.script,
            url=args.url,
            filetype=args.file,
            inurl=args.inurl,
            intitle=args.intitle,
            intext=args.intext,
            show_all=args.all
        )
        return
        
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

    print(f"{Fore.YELLOW}Iniciando busca com o dork: {query.strip()}\n")

    fetch_results(query.strip(), show_all=args.all)

if __name__ == "__main__":
    main()
