import re
import time
import random
import requests
import urllib.parse


def Capture(string, first, last):
    try:
        start = string.index(first) + len(first)
        end = string.index(last, start)
        return re.sub(r'/\s\s+/', '', re.compile(r'<[^>]+>').sub('', string[start:end])).strip()
    except Exception:
        return 'Error in capture !!'


def str_shuffle(string):
    str = string.split(' ')
    text = ''
    for string in str:
        created_list = list(string)
        random.shuffle(created_list)
        text += ''.join(created_list).capitalize() + ' '
    return text[:-1]


today = ''
next_billing = ''

test = True
while test:
    if today == next_billing:
        try:
            today = int(time.time())

            result_raw = requests.get(url='https://gmat.magoosh.com/subscribe/1-week')
            result = result_raw.text
            cookie_jar = result_raw.cookies.get_dict()

            csrf = urllib.parse.quote_plus(Capture(result, '"csrf-token" content="', '"'))

            email = str_shuffle('williamherman') + str(random.randint(1111, 9999)) + '%40gmail.com'

            sign_in_result_raw = requests.post(url='https://gmat.magoosh.com/subscribe/1-week', headers={
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Language': 'en-US,en;q=0.9',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Host': 'gmat.magoosh.com',
            'Origin': 'https://gmat.magoosh.com',
            'Referer': 'https://gmat.magoosh.com/subscribe/1-week',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'
            }, data=f'utf8=%E2%9C%93&authenticity_token={csrf}&subscription%5Bemail%5D={email}&subscription%5Bpassword%5D=William_german%404321&subscription%5Bpassword_confirmation%5D=William_german%404321&accept_terms=1', cookies=cookie_jar, allow_redirects=False)

            cookie_jar = cookie_jar | sign_in_result_raw.cookies.get_dict()

            sign_in_result = sign_in_result_raw.text

            next_link = Capture(sign_in_result, 'You are being <a href="', '"')

            result_raw_welcome = requests.get(url=next_link, cookies=cookie_jar).text


            ready_result = requests.post(url='https://gmat.magoosh.com/welcome_update', headers={
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Language': 'en-US,en;q=0.9',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Host': 'gmat.magoosh.com',
            'Origin': 'https://gmat.magoosh.com',
            'Referer': 'https://gmat.magoosh.com/welcome?paid=false',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'
            }, data=f'utf8=%E2%9C%93&_method=patch&authenticity_token={csrf}&user%5Bfirst_name%5D={str_shuffle("william")}&user%5Blast_name%5D={str_shuffle("german")}&user%5Btest_date%282i%29%5D=&user%5Btest_date%283i%29%5D=&user%5Btest_date%281i%29%5D=&user%5Btarget_score%5D=&user%5Bactual_score%5D=&user%5Bdiagnostic_score%5D=&user%5Bheard_from%5D=&user%5Bphone_number%5D=&user%5Bexam_interest_groups%5D%5B%5D=&user%5Bhas_watched_youtube%5D=false&commit=Next', cookies=cookie_jar).text

            if '<p><a class="btn btn-secondary" href="/dashboard">Start Studying</a></p>' in ready_result:
                message = urllib.parse.quote_plus(f'<b>✅ New Account</b>\n<b>Email:</b> <code>{urllib.parse.unquote_plus(email)}</code>\n<b>Password:</b> <code>William_german@4321</code>')
                requests.get(f"https://api.telegram.org/bot1913895229:AAE1Mdye54kHmg3C9XXebXARa3boujrjVlA/sendMessage?chat_id=868689764&text={message}&parse_mode=HTML").json()
                next_billing = today + 604800

        except:
            requests.get(f"https://api.telegram.org/bot1913895229:AAE1Mdye54kHmg3C9XXebXARa3boujrjVlA/sendMessage?chat_id=868689764&text=Error+in+creating+account&parse_mode=HTML").json()
            pass

    today = int(time.time())
