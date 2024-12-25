# Dorkscan

Dorkscan is an advanced Google scanning tool that uses dorks to find specific information and potential security vulnerabilities. Ideal for security professionals, pentesters and enthusiasts in the field, it allows you to customize searches and execute predefined scripts to automate tasks.

## Main Features
- **Custom Search**: Use filters such as `site:`, `filetype:`, `inurl:`, `intitle:`, among others.
- **Script Execution**: Automate specific searches with predefined scripts (e.g.: SQL Injection, XSS).
- **Script List**: Display all available scripts in the `scripts` folder.
- **Compact Results**: Displays links in an organized and clean way.

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/dorkscan.git
cd dorkscan
```

2. Install the requirements:
```bash
pip install -r requirements.txt
```

## Usage

### Basic Commands

- **Help**:
```bash
python dorkscan.py -h
```

- **Simple Search**:
```bash
python dorkscan.py -u example.com --file pdf --inurl admin
```
This will search for PDFs on the site `example.com` containing "admin" in the URL.

- **List Available Scripts**:
```bash
python dorkscan.py --list
```

- **Run Predefined Script**:
```bash
python dorkscan.py -u example.com --script sql_injection_scan
```

## Script Structure

Scripts are located in the `scripts` folder and must be in text format containing dorks. For example:

`sql_injection_scan.txt`:
```text
site:{url} inurl:".php?" inurl:"=" -site:php.net -site:phpmyadmin.net
```

Placeholders such as `{url}` will be automatically replaced by the parameters provided.

## Usage Example

1. List available scripts:
```bash
python dorkscan.py --list
```

2. Run a script with URL:
```bash
python dorkscan.py -u example.com --script sql_injection_scan
```

3. Advanced custom search:
```bash
python dorkscan.py -u example.com --file pdf --intitle "Report" --inurl admin
```
