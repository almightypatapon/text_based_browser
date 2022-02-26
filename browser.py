from sys import argv
from os import mkdir, listdir, path
from collections import deque
import requests
from bs4 import BeautifulSoup
from colorama import init, Fore


def read_write(dir_, url_, mode_='r', response_=None):
    url = url_[:url_.index(".")] if "." in url_ else url_
    with open(f'./{dir_}/{url}', mode_, encoding='utf-8') as page_:
        if mode_ == 'r':
            print(page_.read())
        else:
            print(*response_, file=page_, sep='\n')
    return url


directory = argv[1]
stack = deque()
init(autoreset=True)

if not path.exists(directory):
    mkdir(directory)

while True:
    inp = input().replace('www.', '').replace('https://', '')
    if inp == 'exit':
        break
    elif inp == 'back':
        if len(stack) > 1:
            stack.pop()
            read_write(directory, stack.pop())
    elif inp in listdir(directory):
        stack.append(read_write(directory, inp))
    elif inp.count('.') == 0:
        print("Error: Incorrect URL")
    else:
        try:
            r = requests.get('https://' + inp)
            soup = BeautifulSoup(r.content, 'html.parser')
            for a in soup.find_all('a'):
                a.string = Fore.BLUE + a.text.strip() + Fore.RESET
            if r:
                print(*soup.stripped_strings)
                stack.append(read_write(directory, inp, 'w', soup.stripped_strings))
            else:
                print(f"{r.status_code} error")
        except requests.exceptions.ConnectionError:
            print("Connection Error")
