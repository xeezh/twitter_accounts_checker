import requests
import threading
import os
import json
from time import sleep
from loguru import logger

finally_good = []
checked_count = 0

def check(username: str):
    headers = {
        'authority': 'shadowban-api.yuzurisa.com:444',
        'accept': '*/*',
        'accept-language': 'ru-RU,ru;q=0.5',
        'origin': 'https://shadowban.yuzurisa.com',
        'referer': 'https://shadowban.yuzurisa.com/',
        'sec-ch-ua': '"Brave";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'sec-gpc': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
    }

    response = json.loads(requests.get(f'https://shadowban-api.yuzurisa.com:444/{username}', headers=headers).text)
    try:
        if response['tests']['typeahead']:
            return 1
    except:
        return 0
    return 0


def check_thread(usernames: list):
    global finally_good, checked_count
    good = []
    for un in usernames:
        if check(un) == 1:
            logger.success(f'{un} - good')
            good.append(un)
        else:
            logger.error(f'{un} - bad')
        checked_count += 1
    finally_good += good


def main(accs_list: list, th: int):
    arr = [[] for _ in range(th)]

    for i in range(len(accs_list)):
        arr[i % th].append(accs_list[i])

    for sub_arr in arr:
        x = threading.Thread(target=check_thread, args=(sub_arr,))
        x.start()

    while not checked_count == len(accs_list):
        sleep(1)



if __name__ == "__main__":
    threads = int(input("Введите кол-во потоков >> "))

    files = os.listdir('raw/')
    raw_accs = []
    for file in files:
        with open(f'raw/{file}') as f:
            raw_accs = raw_accs + f.readlines()

    accs = []
    for ac in raw_accs:
        accs.append(ac.split(':')[0])

    main(accs, threads)

    good = []
    bad = []
    for ac in raw_accs:
        if ac.split(':')[0] in finally_good:
            good.append(ac)
        else:
            bad.append(ac)

    with open('checked/good.txt', 'a') as f:
        f.writelines(good)
        f.close()
    with open('checked/bad.txt', 'a') as f:
        f.writelines(bad)
        f.close()


    print('\n\n\n\n\n')
    logger.success('All accounts checked')
    input()