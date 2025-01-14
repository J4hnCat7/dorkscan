import requests
import argparse
import os
from multiprocessing import Pool, cpu_count
from bs4 import BeautifulSoup as bs
from functools import partial
import sys
import urllib.parse

class DorkScan:
    def __init__(self):
        self.args = self._parse_args()
        self.engine = self.args.engine
        self.url = self.args.url
        self.file_type = self.args.file
        self.inurl = self.args.inurl
        self.intitle = self.args.intitle
        self.intext = self.args.intext
        self.pages = self.args.pages
        self.script = self.args.script
        self.list_scripts_flag = self.args.list 

    def _parse_args(self):
        parser = argparse.ArgumentParser(description="DorkScan: A tool for advanced Google and Bing searches.")
        parser.add_argument('-u', '--url', help="site:{url}", default=None)
        parser.add_argument('-F', '--file', help="filetype", default=None)
        parser.add_argument('--inurl', help="inurl", default=None)
        parser.add_argument('--intitle', help="intitle", default=None)
        parser.add_argument('--intext', help="intext", default=None)
        parser.add_argument('-e', '--engine', help="Search engine to use (google or bing)")
        parser.add_argument('-p', '--pages', type=int, default=1, help="Number of pages to scrape")
        parser.add_argument('-s', '--script', help="Execute a script from the 'scripts' folder")
        parser.add_argument('-l', '--list', action='store_true', help="List all scripts in the 'scripts' folder")
        return parser.parse_args()

    def google(self, query, page):
        base_url = 'https://www.google.com/search'
        headers = { 'User-Agent': 'Mozilla/5.0' }
        params = { 'q': query, 'start': page * 10 }
        if self.url: params['q'] += f" site:{self.url}"
        if self.file_type: params['q'] += f" filetype:{self.file_type}"
        if self.inurl: params['q'] += f" inurl:{self.inurl}"
        if self.intitle: params['q'] += f" intitle:{self.intitle}"
        if self.intext: params['q'] += f" intext:{self.intext}"
        response = requests.get(base_url, params=params, headers=headers)
        if response.status_code != 200:
            print(f"Error: {response.status_code} - Google search failed.")
            return []
        soup = bs(response.text, 'html.parser')
        results = []
        for a in soup.find_all('a', href=True):
            link = a['href']
            if link.startswith('/url?q='):
                clean_link = link.split('q=')[1].split('&')[0]
                clean_link = urllib.parse.unquote(clean_link)
                if clean_link.startswith('https://') and not any(bad_url in clean_link for bad_url in ['support.google.com', 'accounts.google.com', '/search', 'maps.google.com']):
                    results.append(clean_link)
        return results

    def bing(self, query, page):
        base_url = 'https://www.bing.com/search'
        headers = { 'User-Agent': 'Mozilla/5.0' }
        params = { 'q': query, 'first': page * 10 + 1 }
        if self.url: params['q'] += f" site:{self.url}"
        if self.file_type: params['q'] += f" filetype:{self.file_type}"
        if self.inurl: params['q'] += f" inurl:{self.inurl}"
        if self.intitle: params['q'] += f" intitle:{self.intitle}"
        if self.intext: params['q'] += f" intext:{self.intext}"
        response = requests.get(base_url, params=params, headers=headers)
        if response.status_code != 200:
            print(f"Error: {response.status_code} - Bing search failed.")
            return []
        soup = bs(response.text, 'html.parser')
        return [a['href'] for a in soup.find_all('a', href=True) if 'href' in a.attrs and a.attrs['href'].startswith('http')]

    def get_results(self, query, engine, pages):
        if engine == "google":
            func = self.google
        elif engine == "bing":
            func = self.bing
        else:
            print("Unsupported engine!")
            return []

        with Pool(cpu_count()) as pool:
            results = pool.map(partial(self._search_page, func=func, query=query), range(pages))
        return results

    def _search_page(self, page, func, query):
        return func(query, page)

    def display_results(self, query, results):
        total = sum(len(page_results) for page_results in results)
        print('-' * 70)
        print(f"Results for: {query}")
        print('-' * 70)
        counter = 0
        for page_results in results:
            for url in page_results:
                print(f'[+] {url}')
                counter += 1
        print('-' * 70)
        print(f'Total: {counter} URLs found')
        print('-' * 70)

    def execute_script(self, script_name):
        script_path = os.path.join(os.getcwd(), 'scripts', script_name)
        if not os.path.exists(script_path):
            print(f"Script {script_name} not found!")
            return

        with open(script_path, 'r') as file:
            script_content = file.read()
        
        if self.url:
            script_content = script_content.replace("{url}", self.url)

        print(f"Executing script: {script_name}")
        results = self.get_results(script_content, self.engine, self.pages)
        self.display_results(script_content, results)

    def list_scripts(self):
        scripts_dir = os.path.join(os.getcwd(), 'scripts')
        if not os.path.exists(scripts_dir):
            print("No scripts folder found!")
            return

        scripts = [f for f in os.listdir(scripts_dir) if os.path.isfile(os.path.join(scripts_dir, f))]
        if scripts:
            print("Scripts available in 'scripts' folder:")
            for script in scripts:
                print(f" - {script}")
        else:
            print("No scripts found in 'scripts' folder.")

    def run(self):
        if self.list_scripts_flag:
            self.list_scripts()
        elif self.script:
            if not self.engine:
                print("Error: You must specify an engine (-e or --engine) to run the script.")
                return
            self.execute_script(self.script)
        else:
            query = ""
            if not self.engine:
                print("Error: You must specify an engine (-e or --engine) to perform a search.")
                return
            results = self.get_results(query, self.engine, self.pages)
            self.display_results(query, results)


if __name__ == '__main__':
    try:
        if sys.platform == "win32":
            from multiprocessing import freeze_support
            freeze_support()
        dork_scan = DorkScan()
        dork_scan.run()
    except KeyboardInterrupt:
        print('\nThank you!')
    except TimeoutError:
        print('\n[-] Too many requests. Please try again later.')
