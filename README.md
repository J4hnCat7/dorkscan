# DorkScan

DorkScan is an advanced tool for searching using Google and Bing dorks. With DorkScan, you can perform complex searches that include specific filters such as `site:`, `filetype:`, `inurl:`, `intitle:`, and `intext:`, among others. The tool allows you to execute predefined search queries from scripts stored in the `scripts` folder, list available scripts, and run searches across multiple pages efficiently using multithreading.

## What Does DorkScan Do?

- **Advanced Search**: Perform complex Google and Bing searches with various filters such as `site:`, `filetype:`, `inurl:`, `intitle:`, and `intext:`.
- **Multithreaded**: It uses Python's `multiprocessing` library to perform searches efficiently across multiple pages.
- **Script Execution**: You can execute predefined queries stored as scripts in the `scripts` folder.
- **List Available Scripts**: View all scripts available in the `scripts` folder for easy execution.
- **Search Results**: Display the results of your search query in a readable format with links to relevant URLs.

## Installation

To install DorkScan, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/J4hnCat7/Dorkscan.git
   cd dorkscan
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Ensure you have Python 3.x installed.

## Usage

To use DorkScan, run the script with the desired parameters. You can choose the search engine, add filters, execute scripts, and more.

### Help

To display the help message and see all available options:
```bash
python dorkscan.py -h
```

### Example Commands

Here are some example commands you can use:

#### Basic Search Example

To perform a basic Google search for PDF files on `example.com`:
```bash
python dorkscan.py -e google -u example.com -F pdf
```

#### Search with Multiple Filters

To search Bing for pages with the word "login" in the URL and "admin" in the title:
```bash
python dorkscan.py -e bing -u example.com --inurl login --intitle admin
```

#### Execute a Script

To execute a predefined script (e.g., `script_name.txt`) from the `scripts` folder:
```bash
python dorkscan.py -e google -s script_name.txt
```

#### List Available Scripts

To list all available scripts in the `scripts` folder:
```bash
python dorkscan.py -l
```

### Available Options

- `-u URL` or `--url`: Specify a URL to restrict the search to that site (e.g., `site:example.com`).
- `-F FILE` or `--file`: Specify the file type (e.g., `filetype:pdf`).
- `--inurl`: Search for keywords in the URL.
- `--intitle`: Search for keywords in the title of the page.
- `--intext`: Search for keywords in the page content.
- `-e ENGINE` or `--engine`: Specify the search engine (`google` or `bing`).
- `-p PAGES` or `--pages`: Specify the number of pages to scrape.
- `-s SCRIPT` or `--script`: Execute a script from the `scripts` folder.
- `-l` or `--list`: List all available scripts in the `scripts` folder.

## Folder Structure

The `scripts` folder contains predefined scripts that can be executed using the `-s` or `--script` flag. Each script should contain a valid search query.

### Example Script Content

An example script inside the `scripts` folder (e.g., `example_script`) could contain:
```
site:example.com filetype:pdf
```

## Example Script Execution

1. Create a script inside the `scripts` folder (e.g., `example_script`) with a search query.
2. Run the script with the `-s` flag:
   ```bash
   python dorkscan.py -e google -s example_script
   ```

## Requirements

- Python 3.x
- Required Python libraries: `requests`, `beautifulsoup4`, `argparse`

To install the dependencies:
```bash
pip install -r requirements.txt
```
