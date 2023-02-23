import os
import random
import subprocess
from bs4 import BeautifulSoup
from translate import Translator

def download_website(url, download_dir):
    """
    Download a website using HTTrack.
    :param url: the URL of the website to download.
    :param download_dir: the directory to save the downloaded files.
    """
    cmd = ['httrack', url, '-O', download_dir]
    subprocess.call(cmd)

def translate_html_files(html_dir, target_lang='hi'):
    """
    Translate text in HTML files using Google Translate.
    :param html_dir: the directory containing the HTML files to translate.
    :param target_lang: the target language for translation. Default is Hindi.
    """
    translator = Translator(to_lang=target_lang)
    for root, dirs, files in os.walk(html_dir):
        for file_name in files:
            if not file_name.endswith('.html'):
                continue
            file_path = os.path.join(root, file_name)
            with open(file_path, 'r', encoding='UTF-8') as f:
                print(file_path)
                soup = BeautifulSoup(f, 'lxml')
                elements = soup.find_all(lambda tag: tag.name not in ['script', 'style'] and (tag.string is not None and len(tag.string.strip()) > 0))
            for element in elements:
                text = element.string.strip()
                translated_text = translator.translate(text)
                element.string = translated_text
            with open(file_path, 'w', encoding='UTF-8') as f:
                f.write(soup.prettify())

if __name__ == '__main__':
    # Download the website
    website_url = 'https://subslikescript.com/movies'
    download_dir = './downloaded'
    download_website(website_url, download_dir)
    
    # Translate the HTML files
    html_dir = os.path.join(download_dir, 'subslikescript.com')
    target_lang = 'hi'
    translate_html_files(html_dir, target_lang)

