import requests
import json
import os
import time
import random
import threading
import websocket
import re
from collections import defaultdict

# ==================== OWNER CONFIGURATION ====================
OWNER_ID = "1520080799485919363"

# ==================== MULTI-TOKEN CONFIGURATION ====================
TOKENS = [
   "MTUyMzcxMzkxNzExMTc2Mjk4MQ.GNpc9-.CUftsn8uEGktR40rY_H0zeRRKz7vW23C26gvic",  # Replace with your actual token
   "token2",   # Replace with actual token 2
   "token3",   # Replace with actual token 3
   "token4",   # Replace with actual token 4
   "token5",   # Replace with actual token 5
   "token6",   # Replace with actual token 6
   "token7",   # Replace with actual token 7
   "token8",   # Replace with actual token 8
   "token9",   # Replace with actual token 9
   "token10"   # Replace with actual token 10
]

TOKENS = [t for t in TOKENS if t and t.strip() and not t.startswith('.')]
# ================================================================

# --- FILES & PATHS ---
SUDO_FILE = "sudo_users.json"

# --- FIXED PREFIX ---
PREFIX = "$"

# --- SYSTEM FLAGS ---
ACTIVE_NC_CHANNELS = {}            # Old $nc
ACTIVE_CUSTOM_NC_CHANNELS = {}     # Old $customnc
ACTIVE_NCMX_CHANNELS = {}          # NEW $ncmx
ACTIVE_SPAM_CHANNELS = {}
ACTIVE_SPAM2_CHANNELS = {}
ACTIVE_CUSTOM_SPAM_CHANNELS = {}
ACTIVE_PIC_SPAM_CHANNELS = {}

SPAM_STOP_EVENTS = {}
SPAM2_STOP_EVENTS = {}
CUSTOM_SPAM_STOP_EVENTS = {}
PIC_SPAM_STOP_EVENTS = {}

AUTOREPLY_TARGETS = {}
AUTOREACT_EMOJIS = {}

START_TIME = time.time()

# --- OLD NC LIST ---
NC_BASE_LIST = [
    "TMKX MEI -->-🌟🌵✨",
    "TMKX MEI -->-🌍💥✨",
    "TMKX MEI -->-🌿⚔️✨",
    "TMKX MEI -->-🥀🔥✨",
    "TMKX MEI -->-🌹💀✨",
    "TMKX MEI -->-🌺🖤✨",
    "TMKX MEI -->-🍷💀✨",
    "TMKX MEI -->-🌶️🔥✨",
    "TMKX MEI -->-🌙🔥✨",
    "TMKX MEI -->-🌹☠️✨"
]

# --- NEW NC MX PATTERNS (5 RGB Heart Variations) ---
NC_MX_PATTERNS = [
    "{custom_text}-𝙈𝘼𝘿𝘼𝙍𝘾𝙃⭕𝘿-𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫-💋",
    "{custom_text}-𝙈𝘼𝘿𝘼𝙍𝘾𝙃⭕𝘿-𒐫𒐫𒐫❤️𒐫𒐫𒐫❤️𒐫𒐫𒐫❤️𒐫𒐫𒐫❤️𒐫𒐫𒐫❤️𒐫𒐫𒐫❤️𒐫𒐫𒐫❤️𒐫𒐫𒐫❤️𒐫𒐫𒐫❤️𒐫𒐫𒐫❤️𒐫𒐫𒐫❤️𒐫𒐫𒐫❤️𒐫𒐫𒐫-💋",
    "{custom_text}-𝙈𝘼𝘿𝘼𝙍𝘾𝙃⭕𝘿-𒐫𒐫𒐫💜𒐫𒐫𒐫💜𒐫𒐫𒐫💜𒐫𒐫𒐫💜𒐫𒐫𒐫💜𒐫𒐫𒐫💜𒐫𒐫𒐫💜𒐫𒐫𒐫💜𒐫𒐫𒐫💜𒐫𒐫𒐫💜𒐫𒐫𒐫💜𒐫𒐫𒐫💜𒐫𒐫𒐫-💋",
    "{custom_text}-𝙈𝘼𝘿𝘼𝙍𝘾𝙃⭕𝘿-𒐫𒐫𒐫💙𒐫𒐫𒐫💙𒐫𒐫𒐫💙𒐫𒐫𒐫💙𒐫𒐫𒐫💙𒐫𒐫𒐫💙𒐫𒐫𒐫💙𒐫𒐫𒐫💙𒐫𒐫𒐫💙𒐫𒐫𒐫💙𒐫𒐫𒐫💙𒐫𒐫𒐫💙𒐫𒐫𒐫-💋",
    "{custom_text}-𝙈𝘼𝘿𝘼𝙍𝘾𝙃⭕𝘿-𒐫𒐫𒐫🧡𒐫𒐫𒐫🧡𒐫𒐫𒐫🧡𒐫𒐫𒐫🧡𒐫𒐫𒐫🧡𒐫𒐫𒐫🧡𒐫𒐫𒐫🧡𒐫𒐫𒐫🧡𒐫𒐫𒐫🧡𒐫𒐫𒐫🧡𒐫𒐫𒐫🧡𒐫𒐫𒐫🧡𒐫𒐫𒐫-💋"
]

# --- ZERO-WIDTH SPACE TO FIX DISCORD MARKDOWN HEADERS ---
ZWSP = "\u200B"

# --- RGB EMOJIS ---
RGB_EMOJIS = [
    "𓆰🔴𓆪",
    "𓆰🟢𓆪",
    "𓆰🔵𓆪",
    "𓆰🟡𓆪",
    "𓆰🟣𓆪"
]

# --- BASE SPAM MESSAGES ---
BASE_SPAM_MESSAGES = [
    ("# {target} {rbg} #" + ZWSP + " 𝗥ɴ𝗗l⃠𝗖ᴇ #" + ZWSP + " 𝗟ᴀ𝗗ᴄ𝗘 #" + ZWSP + " ɪ𝗦 #" + ZWSP + " s𝗘 #" + ZWSP + " 𝗧ᴇ𝗭 #" + ZWSP + " 𝗧ᴏ #" + ZWSP + " 𝗧ᴇ𝗥ɪ #" + ZWSP + " 𝗔ᴍ𝗠ᴀ #" + ZWSP + " 𝗖ʜ𝗨ᴅ𝗧ɪ #" + ZWSP + " 𝗛ᴀ𝗜I⃠ {rbg}"
     "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
     "# {target} {rbg} #" + ZWSP + " 𝗥ɴ𝗗l⃠𝗖ᴇ #" + ZWSP + " 𝗟ᴀ𝗗ᴄ𝗘 #" + ZWSP + " ɪ𝗦 #" + ZWSP + " s𝗘 #" + ZWSP + " 𝗧ᴇ𝗭 #" + ZWSP + " 𝗧ᴏ #" + ZWSP + " 𝗧ᴇ𝗥ɪ #" + ZWSP + " 𝗔ᴍ𝗠ᴀ #" + ZWSP + " 𝗖ʜ𝗨ᴅ𝗧ɪ #" + ZWSP + " 𝗛ᴀ𝗜I⃠ {rbg}"
     "# {target} {rbg} #" + ZWSP + " 𝗥ɴ𝗗l⃠𝗖ᴇ #" + ZWSP + " 𝗟ᴀ𝗗ᴄ𝗘 #" + ZWSP + " ɪ𝗦 #" + ZWSP + " s𝗘 #" + ZWSP + " 𝗧ᴇ𝗭 #" + ZWSP + " 𝗧ᴏ #" + ZWSP + " 𝗧ᴇ𝗥ɪ #" + ZWSP + " 𝗔ᴍ𝗠ᴀ #" + ZWSP + " 𝗖ʜ𝗨ᴅ𝗧ɪ #" + ZWSP + " 𝗛ᴀ𝗜I⃠ {rbg}"
     "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
     "# {target} {rbg} #" + ZWSP + " 𝗥ɴ𝗗l⃠𝗖ᴇ #" + ZWSP + " 𝗟ᴀ𝗗ᴄ𝗘 #" + ZWSP + " ɪ𝗦 #" + ZWSP + " s𝗘 #" + ZWSP + " 𝗧ᴇ𝗭 #" + ZWSP + " 𝗧ᴏ #" + ZWSP + " 𝗧ᴇ𝗥ɪ #" + ZWSP + " 𝗔ᴍ𝗠ᴀ #" + ZWSP + " 𝗖ʜ𝗨ᴅ𝗧ɪ #" + ZWSP + " 𝗛ᴀ𝗜I⃠ {rbg}"
     "# {target} {rbg} #" + ZWSP + " 𝗥ɴ𝗗l⃠𝗖ᴇ #" + ZWSP + " 𝗟ᴀ𝗗ᴄ𝗘 #" + ZWSP + " ɪ𝗦 #" + ZWSP + " s𝗘 #" + ZWSP + " 𝗧ᴇ𝗭 #" + ZWSP + " 𝗧ᴏ #" + ZWSP + " 𝗧ᴇ𝗥ɪ #" + ZWSP + " 𝗔ᴍ𝗠ᴀ #" + ZWSP + " 𝗖ʜ𝗨ᴅ𝗧ɪ #" + ZWSP + " 𝗛ᴀ𝗜I⃠ {rbg}"
     "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
     "# {target} {rbg} #" + ZWSP + " 𝗥ɴ𝗗l⃠𝗖ᴇ #" + ZWSP + " 𝗟ᴀ𝗗ᴄ𝗘 #" + ZWSP + " ɪ𝗦 #" + ZWSP + " s𝗘 #" + ZWSP + " 𝗧ᴇ𝗭 #" + ZWSP + " 𝗧ᴏ #" + ZWSP + " 𝗧ᴇ𝗥ɪ #" + ZWSP + " 𝗔ᴍ𝗠ᴀ #" + ZWSP + " 𝗖ʜ𝗨ᴅ𝗧ɪ #" + ZWSP + " 𝗛ᴀ𝗜I⃠ {rbg}"
     "# {target} {rbg} #" + ZWSP + " 𝗥ɴ𝗗l⃠𝗖ᴇ #" + ZWSP + " 𝗟ᴀ𝗗ᴄ𝗘 #" + ZWSP + " ɪ𝗦 #" + ZWSP + " s𝗘 #" + ZWSP + " 𝗧ᴇ𝗭 #" + ZWSP + " 𝗧ᴏ #" + ZWSP + " 𝗧ᴇ𝗥ɪ #" + ZWSP + " 𝗔ᴍ𝗠ᴀ #" + ZWSP + " 𝗖ʜ𝗨ᴅ𝗧ɪ #" + ZWSP + " 𝗛ᴀ𝗜I⃠ {rbg}"
     "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
     "# {target} {rbg} #" + ZWSP + " 𝗥ɴ𝗗l⃠𝗖ᴇ #" + ZWSP + " 𝗟ᴀ𝗗ᴄ𝗘 #" + ZWSP + " ɪ𝗦 #" + ZWSP + " s𝗘 #" + ZWSP + " 𝗧ᴇ𝗭 #" + ZWSP + " 𝗧ᴏ #" + ZWSP + " 𝗧ᴇ𝗥ɪ #" + ZWSP + " 𝗔ᴍ𝗠ᴀ #" + ZWSP + " 𝗖ʜ𝗨ᴅ𝗧ɪ #" + ZWSP + " 𝗛ᴀ𝗜I⃠ {rbg}")
]

# --- Generate long spam messages ---
SPAM_MESSAGES = [msg * 4 for msg in BASE_SPAM_MESSAGES]

# --- SPAM2 MESSAGES ---
SPAM2_MESSAGES = [
    "# {target} {rbg} CUDDKAD RDNYCE {rbg} {rbg} CUDDKAD RDNYCE {rbg} {rbg} CUDDKAD RDNYCE {rbg} {rbg} CUDDKAD RDNYCE {rbg} {rbg} CUDDKAD RDNYCE {rbg}",
    "# {target} {rbg} CUDDKAD RDNYCE {rbg} {rbg} CUDDKAD RDNYCE {rbg} {rbg} CUDDKAD RDNYCE {rbg} {rbg} CUDDKAD RDNYCE {rbg} {rbg} CUDDKAD RDNYCE {rbg}",
    "# {target} {rbg} CUDDKAD RDNYCE {rbg} {rbg} CUDDKAD RDNYCE {rbg} {rbg} CUDDKAD RDNYCE {rbg} {rbg} CUDDKAD RDNYCE {rbg} {rbg} CUDDKAD RDNYCE {rbg}",
    "# {target} {rbg} CUDDKAD RDNYCE {rbg} {rbg} CUDDKAD RDNYCE {rbg} {rbg} CUDDKAD RDNYCE {rbg} {rbg} CUDDKAD RDNYCE {rbg} {rbg} CUDDKAD RDNYCE {rbg}",
    "# {target} {rbg} CUDDKAD RDNYCE {rbg} {rbg} CUDDKAD RDNYCE {rbg} {rbg} CUDDKAD RDNYCE {rbg} {rbg} CUDDKAD RDNYCE {rbg} {rbg} CUDDKAD RDNYCE {rbg}"
]

# --- STYLIZED ROASTS ---
ROASTS = [
    "𝐋ᴜ𝐍 𝐓ᴇ 𝐕ᴀ𝐉 𝐎ʏ𝐘 🍫",
    "𝐀𝐏𝐍𝐀 𝐁𝐇𝐎𝐒𝐃𝐀 𝐃𝐄𝐊𝐇 🖕",
    "𝐂𝐇𝐔𝐏 𝐊𝐀𝐑 𝐁𝐄𝐇𝐄𝐍 𝐊𝐈 𝐋𝐔𝐍𝐃 🔥",
    "𝐓𝐄𝐑𝐈 𝐌𝐀𝐀 𝐊𝐈 𝐂𝐇𝐔𝐓 𝐌𝐄 𝐌𝐄𝐑𝐀 𝐋𝐔𝐍𝐃 🍆",
    "𝐁𝐇𝐄𝐍𝐂𝐇𝐎𝐃 𝐀𝐏𝐍𝐈 𝐀𝐔𝐊𝐀𝐓 𝐌𝐄 𝐑𝐄𝐇 🤡",
    "𝐓𝐄𝐑𝐈 𝐁𝐄𝐇𝐄𝐍 𝐊𝐀 𝐁𝐇𝐎𝐒𝐃𝐀 🗑️",
    "𝐑𝐀𝐍𝐃𝐈 𝐊𝐀 𝐏𝐈𝐋𝐋𝐀 𝐇𝐀𝐈 𝐓𝐔 🐕",
    "𝐓𝐄𝐑𝐈 𝐌𝐀𝐀 𝐊𝐎 𝐁𝐀𝐙𝐀𝐀𝐑 𝐌𝐄 𝐂𝐇𝐎𝐃𝐔𝐍𝐆𝐀 🌃",
    "𝐌𝐀𝐃𝐀𝐑𝐂𝐇𝐎𝐃 𝐓𝐄𝐑𝐈 𝐁𝐄𝐇𝐄𝐍 𝐌𝐄𝐑𝐈 𝐑𝐀𝐍𝐃𝐈 💋",
    "𝐓𝐄𝐑𝐈 𝐌𝐀𝐀 𝐊𝐈 𝐂𝐇𝐔𝐓 𝐌𝐄 𝐆𝐀𝐑𝐀𝐌 𝐓𝐄𝐋 🌡️",
    "𝐀𝐏𝐍𝐈 𝐀𝐔𝐊𝐀𝐓 𝐃𝐄𝐊𝐇 𝐊𝐔𝐓𝐓𝐄 🐕😂",
    "𝐂𝐇𝐔𝐏 𝐊𝐀𝐑 𝐌𝐀𝐃𝐀𝐑𝐂𝐇𝐎𝐃 🤫💀",
    "𝐓𝐄𝐑𝐈 𝐁𝐄𝐇𝐄𝐍 𝐊𝐈 𝐒𝐇𝐀𝐃𝐈 𝐌𝐄 𝐌𝐄𝐑𝐀 𝐋𝐔𝐍𝐃 😈",
    "𝐌𝐀𝐃𝐀𝐑𝐂𝐇𝐎𝐃 𝐀𝐏𝐍𝐈 𝐌𝐀𝐀 𝐌𝐀𝐓 𝐂𝐇𝐔𝐃𝐀 🖕🏻"
]

# --- DELAYS ---
NC_DELAY = 0.01
NCMX_DELAY = 0.1
SPAM_DELAY = 0.1
SPAM2_DELAY = 0.1
CUSTOM_SPAM_DELAY = 0.1
CUSTOM_NC_DELAY = 0.1
PIC_SPAM_DELAY = 0.1
MULTI_SPAM_DELAY = 0.05  # ULTRA-FAST

# --- SUDO USERS ---
def load_sudo():
    if os.path.exists(SUDO_FILE):
        try:
            with open(SUDO_FILE, "r") as f:
                return json.load(f)
        except:
            return []
    return []

def save_sudo(users):
    with open(SUDO_FILE, "w") as f:
        json.dump(users, f)

SUDO_USERS = load_sudo()

# --- HELPERS ---
def send_msg(c_id, text, reply_to=None, token=None):
    if not token:
        return None
    headers = {"Authorization": token, "Content-Type": "application/json"}
    payload = {"content": text}
    if reply_to:
        payload["message_reference"] = {"channel_id": c_id, "message_id": reply_to}
    try:
        r = requests.post(f"https://discord.com/api/v9/channels/{c_id}/messages",
                         headers=headers, json=payload)
        if r.status_code == 429:
            retry_after = r.json().get("retry_after", 1.0)
            time.sleep(retry_after)
            return None
        return r
    except Exception as e:
        print(f"send_msg error: {e}")
        return None

def send_file(c_id, file_path, token=None):
    if not token or not os.path.exists(file_path):
        return None
    headers = {"Authorization": token}
    try:
        with open(file_path, 'rb') as f:
            r = requests.post(f"https://discord.com/api/v9/channels/{c_id}/messages",
                              headers=headers, files={"file": f})
        if r.status_code == 429:
            time.sleep(r.json().get("retry_after", 1.0))
            return None
        return r
    except Exception as e:
        print(f"send_file error: {e}")
        return None

def download_image(url):
    try:
        r = requests.get(url, stream=True, timeout=10)
        if r.status_code == 200:
            path = f"temp_{random.randint(1000,9999)}.jpg"
            with open(path, 'wb') as f:
                for chunk in r.iter_content(1024):
                    f.write(chunk)
            return path
        return None
    except Exception as e:
        print(f"Download image error: {e}")
        return None

def change_gc_name(g_id, name, token=None):
    if not token:
        return None
    headers = {"Authorization": token, "Content-Type": "application/json"}
    try:
        r = requests.patch(f"https://discord.com/api/v9/channels/{g_id}",
                           headers=headers, json={"name": name})
        if r.status_code == 429:
            retry_after = r.json().get("retry_after", 1.0)
            time.sleep(retry_after)
        return r
    except Exception as e:
        print(f"change_gc_name error: {e}")
        return None

def add_reaction(c_id, m_id, emoji, token=None):
    if not token:
        return
    encoded_emoji = requests.utils.quote(emoji)
    url = f"https://discord.com/api/v9/channels/{c_id}/messages/{m_id}/reactions/{encoded_emoji}/@me"
    try:
        r = requests.put(url, headers={"Authorization": token})
        if r.status_code == 429:
            time.sleep(r.json().get("retry_after", 1.0))
    except:
        pass

def verify_owner_id(token):
    try:
        r = requests.get("https://discord.com/api/v9/users/@me",
                         headers={"Authorization": token}, timeout=10)
        if r.status_code == 200:
            data = r.json()
            return data.get('id')
    except:
        pass
    return None

def get_user_info(user_id, token):
    try:
        r = requests.get(f"https://discord.com/api/v9/users/{user_id}",
                         headers={"Authorization": token}, timeout=10)
        if r.status_code == 200:
            data = r.json()
            return data.get('username')
    except:
        pass
    return None

def extract_user_id_from_mention(mention):
    if mention.startswith('<@') and mention.endswith('>'):
        mention = mention[2:-1]
        if mention.startswith('!'):
            mention = mention[1:]
    else:
        if mention.startswith('@'):
            mention = mention[1:]
    match = re.search(r'\d+', mention)
    if match:
        return match.group()
    return None

def extract_target_info(mention, token):
    if mention.startswith('<@') and mention.endswith('>'):
        user_id = mention[2:-1]
        if user_id.startswith('!'):
            user_id = user_id[1:]
        username = get_user_info(user_id, token)
        if username:
            return username
        else:
            return user_id
    else:
        return mention

def pad_to_length(text, max_len):
    if len(text) >= max_len:
        return text[:max_len]
    padded = text
    while len(padded) < max_len:
        remaining = max_len - len(padded) - 1
        if remaining <= 0:
            padded += ' '
            break
        padded += ' ' + text[:remaining]
    return padded[:max_len]

# --- WORKERS ---
def multi_spam_worker_per_token(c_id, target_name, token, stop_event, delay=MULTI_SPAM_DELAY):
    while not stop_event.is_set():
        msg_template = random.choice(SPAM_MESSAGES)
        msg = msg_template.replace("{target}", target_name)
        msg = msg.replace("{rbg}", random.choice(RGB_EMOJIS))
        if len(msg) > 2000:
            msg = msg[:2000]
        send_msg(c_id, msg, token=token)
        for _ in range(int(delay * 10)):
            if stop_event.is_set():
                return
            time.sleep(0.1)

def nc_worker(g_id, target_name, token=None):
    key = f"{g_id}_{token[:10] if token else ''}"
    while ACTIVE_NC_CHANNELS.get(key, False):
        base_line = random.choice(NC_BASE_LIST)
        final_name = f"{target_name} {base_line}"
        if len(final_name) >= 100:
            final_name = final_name[:100]
        else:
            final_name = pad_to_length(final_name, 100)
        change_gc_name(g_id, final_name, token)
        time.sleep(NC_DELAY)

def ncmx_worker(g_id, custom_text, token=None):
    """New NC MX Worker"""
    key = f"{g_id}_{token[:10] if token else ''}"
    while ACTIVE_NCMX_CHANNELS.get(key, False):
        pattern = random.choice(NC_MX_PATTERNS)
        new_name = pattern.replace("{custom_text}", custom_text)
        if len(new_name) >= 100:
            new_name = new_name[:100]
        else:
            new_name = pad_to_length(new_name, 100)
        change_gc_name(g_id, new_name, token)
        time.sleep(NCMX_DELAY)

def custom_nc_worker(g_id, custom_text, token=None):
    key = f"{g_id}_{token[:10] if token else ''}"
    while ACTIVE_CUSTOM_NC_CHANNELS.get(key, False):
        if len(custom_text) >= 100:
            final_name = custom_text[:100]
        else:
            final_name = pad_to_length(custom_text, 100)
        change_gc_name(g_id, final_name, token)
        time.sleep(CUSTOM_NC_DELAY)

def spam_worker(c_id, target_name, token=None):
    key = f"{c_id}_{token[:10] if token else ''}"
    while ACTIVE_SPAM_CHANNELS.get(key, False):
        for msg_template in SPAM_MESSAGES:
            if not ACTIVE_SPAM_CHANNELS.get(key, False):
                break
            msg = msg_template.replace("{target}", target_name)
            msg = msg.replace("{rbg}", random.choice(RGB_EMOJIS))
            if len(msg) > 2000:
                msg = msg[:2000]
            send_msg(c_id, msg, token=token)
            time.sleep(SPAM_DELAY)

def spam2_worker(c_id, target_name, token=None):
    key = f"{c_id}_{token[:10] if token else ''}"
    while ACTIVE_SPAM2_CHANNELS.get(key, False):
        for msg_template in SPAM2_MESSAGES:
            if not ACTIVE_SPAM2_CHANNELS.get(key, False):
                break
            msg = msg_template.replace("{target}", target_name)
            msg = msg.replace("{rbg}", random.choice(RGB_EMOJIS))
            msg = pad_to_length(msg, 2000)
            send_msg(c_id, msg, token=token)
            time.sleep(SPAM2_DELAY)

def custom_spam_worker(c_id, text, token=None):
    key = f"{c_id}_{token[:10] if token else ''}"
    while ACTIVE_CUSTOM_SPAM_CHANNELS.get(key, False):
        if len(text) > 2000:
            text = text[:2000]
        send_msg(c_id, text, token=token)
        time.sleep(CUSTOM_SPAM_DELAY)

def pic_spam_worker(c_id, file_path, token=None):
    key = f"{c_id}_{token[:10] if token else ''}"
    while ACTIVE_PIC_SPAM_CHANNELS.get(key, False):
        send_file(c_id, file_path, token)
        time.sleep(PIC_SPAM_DELAY)

def join_server(invite_code, token):
    try:
        r = requests.post(f"https://discord.com/api/v9/invites/{invite_code}",
                          headers={"Authorization": token})
        return r.status_code == 200
    except:
        return False

# --- BOT CLIENT ---
class DiscordSelfBot:
    def __init__(self, token, bot_index):
        self.token = token
        self.bot_index = bot_index
        self.ws = None
        self.running = True
        self.user_id = None

    def on_message(self, ws, message):
        global ACTIVE_NC_CHANNELS, ACTIVE_CUSTOM_NC_CHANNELS, ACTIVE_NCMX_CHANNELS
        global ACTIVE_SPAM_CHANNELS, ACTIVE_SPAM2_CHANNELS, ACTIVE_CUSTOM_SPAM_CHANNELS, ACTIVE_PIC_SPAM_CHANNELS
        global SPAM_STOP_EVENTS, SPAM2_STOP_EVENTS, CUSTOM_SPAM_STOP_EVENTS, PIC_SPAM_STOP_EVENTS
        global AUTOREPLY_TARGETS, AUTOREACT_EMOJIS, START_TIME, SUDO_USERS, TOKENS
        try:
            data = json.loads(message)
        except:
            return

        if data.get("op") == 10:
            heartbeat_interval = data["d"]["heartbeat_interval"] / 1000
            def heartbeat():
                while self.running:
                    time.sleep(heartbeat_interval)
                    try:
                        ws.send(json.dumps({"op": 1, "d": None}))
                    except:
                        break
            threading.Thread(target=heartbeat, daemon=True).start()
            ws.send(json.dumps({
                "op": 2,
                "d": {
                    "token": self.token,
                    "properties": {"$os": "windows", "$browser": "chrome", "$device": "pc"}
                }
            }))
            r = requests.get("https://discord.com/api/v9/users/@me", headers={"Authorization": self.token})
            if r.status_code == 200:
                self.user_id = r.json().get('id')
            print(f"\033[92m[✓] Bot {self.bot_index + 1} Connected (Token: ...{self.token[-8:]})\033[0m")

        if data.get("t") == "MESSAGE_CREATE":
            msg = data["d"]
            auth_id = msg["author"]["id"]
            content = msg["content"].strip()
            c_id = msg["channel_id"]
            m_id = msg["id"]
            key_suffix = f"{c_id}_{self.token[:10]}"

            # --- AUTOREPLY ---
            if c_id in AUTOREPLY_TARGETS:
                if auth_id in AUTOREPLY_TARGETS[c_id]:
                    if self.user_id and auth_id != self.user_id:
                        reply_text = random.choice(ROASTS)
                        send_msg(c_id, reply_text, reply_to=m_id, token=self.token)

            # --- AUTOREACT ---
            if c_id in AUTOREACT_EMOJIS:
                emoji = AUTOREACT_EMOJIS[c_id]
                if self.user_id and auth_id != self.user_id:
                    threading.Thread(target=add_reaction, args=(c_id, m_id, emoji, self.token), daemon=True).start()

            # --- COMMAND HANDLING ---
            if auth_id != OWNER_ID and auth_id not in SUDO_USERS:
                return

            if not content.startswith(PREFIX):
                return

            cmd_part = content[len(PREFIX):].strip()
            cmd_lower = cmd_part.lower()

            # ---------- $help ----------
            if cmd_lower == "help":
                help_msg = (
                    "```\n"
                    "    ╔═══════════════════════════════════════════════╗\n"
                    "    ║   🔥 MULTI-TOKEN SELF-BOT HELP MENU 🔥        ║\n"
                    "    ║   ⚡ ULTRA-FAST 0.05s SPAM ACTIVE ⚡           ║\n"
                    "    ╚═══════════════════════════════════════════════╝\n\n"
                    "  🛠️  COMMANDS:\n"
                    "  ───────────────────────────────────────────────\n"
                    "  $nc @user          → Old Name Change spam\n"
                    "  $stopnc            → Stop old NC\n"
                    "  $customnc <text>   → Custom name change spam\n"
                    "  $stopcustomnc      → Stop custom NC\n"
                    "  $ncmx <text>       → NEW NC MX (RGB Heart patterns)\n"
                    "  $stopncmx          → Stop new NC MX\n"
                    "  $spam @user        → Multi-token spam (0.05s delay!)\n"
                    "  $stopspam          → Stop multi-token spam\n"
                    "  $spam2 <target>    → Spam2 (CUDDKAD RDNYCE)\n"
                    "  $stopspam2         → Stop spam2\n"
                    "  $customspam <text> → Spam your own text\n"
                    "  $stopcustomspam    → Stop custom spam\n"
                    "  $picspam <url>     → Spam an image\n"
                    "  $stoppicspam       → Stop pic spam\n"
                    "  $join <invite>     → Join a server\n"
                    "  $autoreply @user   → Add autoreply targets\n"
                    "  $removeautoreply @user → Remove target\n"
                    "  $stopautoreply     → Clear all autoreply\n"
                    "  $autoreact <emoji> → Auto-react\n"
                    "  $stopautoreact     → Stop auto-react\n"
                    "  $leavegc           → Leave current group chat\n"
                    "  $rgb               → RGB Emoji Flash Spam!\n"
                    "  $hug @user         → Send a huge hug!\n"
                    "  $ping              → Check latency\n"
                    "  $status            → Show bot status\n"
                    "  $showusers         → List access users\n"
                    "  $access @user      → Grant access (owner only)\n"
                    "  $removeaccess @user → Revoke access\n"
                    "  $stopall           → Kills everything at once\n"
                    "  ───────────────────────────────────────────────\n"
                    "  🏷️  Prefix: `$`  |  🔐 Owner: {OWNER_ID}\n"
                    "  💀  Made by v1rlance / Orion self py panel\n"
                    "  ⚡ {num_tokens} tokens active!\n"
                    "```".format(OWNER_ID=OWNER_ID, num_tokens=len(TOKENS))
                )
                send_msg(c_id, help_msg, token=self.token)
                return

            # ---------- $leavegc ----------
            if cmd_lower == "leavegc":
                send_msg(c_id, "✅ leaving gc in 5 seconds", token=self.token)
                time.sleep(5)
                try:
                    r = requests.delete(f"https://discord.com/api/v9/channels/{c_id}", headers={"Authorization": self.token})
                    if r.status_code not in (200, 204):
                        send_msg(c_id, "❌ can't leave right now", token=self.token)
                except Exception:
                    send_msg(c_id, "❌ can't leave right now", token=self.token)
                return

            # ---------- $nc ----------
            if cmd_lower.startswith("nc "):
                parts = cmd_part.split()
                if len(parts) < 2:
                    send_msg(c_id, "❌ Usage: $nc @user", token=self.token)
                    return
                mention = parts[1]
                target_name = extract_target_info(mention, self.token)
                ACTIVE_NC_CHANNELS[key_suffix] = True
                threading.Thread(target=nc_worker, args=(c_id, target_name, self.token), daemon=True).start()
                send_msg(c_id, f"✅ NC started for {target_name}", token=self.token)
                return

            # ---------- $stopnc ----------
            if cmd_lower == "stopnc":
                ACTIVE_NC_CHANNELS[key_suffix] = False
                send_msg(c_id, "✅ NC stopped", token=self.token)
                return

            # ---------- $customnc ----------
            if cmd_lower.startswith("customnc "):
                parts = cmd_part.split(maxsplit=1)
                if len(parts) < 2:
                    send_msg(c_id, "❌ Usage: $customnc <text>", token=self.token)
                    return
                custom_text = parts[1]
                ACTIVE_CUSTOM_NC_CHANNELS[key_suffix] = True
                threading.Thread(target=custom_nc_worker, args=(c_id, custom_text, self.token), daemon=True).start()
                send_msg(c_id, f"✅ Custom NC started: {custom_text[:30]}...", token=self.token)
                return

            # ---------- $stopcustomnc ----------
            if cmd_lower == "stopcustomnc":
                ACTIVE_CUSTOM_NC_CHANNELS[key_suffix] = False
                send_msg(c_id, "✅ Custom NC stopped", token=self.token)
                return

            # ---------- $ncmx ----------
            if cmd_lower.startswith("ncmx "):
                parts = cmd_part.split(maxsplit=1)
                if len(parts) < 2:
                    send_msg(c_id, "❌ Usage: $ncmx <custom_text>", token=self.token)
                    return
                custom_text = parts[1]
                ACTIVE_NCMX_CHANNELS[key_suffix] = True
                threading.Thread(target=ncmx_worker, args=(c_id, custom_text, self.token), daemon=True).start()
                send_msg(c_id, f"✅ NC MX started: {custom_text[:30]}...", token=self.token)
                return

            # ---------- $stopncmx ----------
            if cmd_lower == "stopncmx":
                ACTIVE_NCMX_CHANNELS[key_suffix] = False
                send_msg(c_id, "✅ NC MX stopped", token=self.token)
                return

            # ---------- $spam ----------
            if cmd_lower.startswith("spam "):
                parts = cmd_part.split()
                if len(parts) < 2:
                    send_msg(c_id, "❌ Usage: $spam @user", token=self.token)
                    return
                mention = parts[1]
                target_name = extract_target_info(mention, self.token)

                if c_id not in SPAM_STOP_EVENTS:
                    SPAM_STOP_EVENTS[c_id] = threading.Event()
                else:
                    SPAM_STOP_EVENTS[c_id].set()
                    SPAM_STOP_EVENTS[c_id] = threading.Event()
                stop_event = SPAM_STOP_EVENTS[c_id]

                valid_tokens = [t for t in TOKENS if t and t.strip()]
                launched = 0
                for token in valid_tokens:
                    threading.Thread(
                        target=multi_spam_worker_per_token,
                        args=(c_id, target_name, token, stop_event, MULTI_SPAM_DELAY),
                        daemon=True
                    ).start()
                    launched += 1

                send_msg(
                    c_id,
                    f"✅ **MULTI-TOKEN SPAM** started for {target_name} using **{launched}** tokens!\n"
                    f"⚡ Speed: {MULTI_SPAM_DELAY}s per token (ULTRA-FAST!)",
                    token=self.token
                )
                return

            # ---------- $stopspam ----------
            if cmd_lower == "stopspam":
                if c_id in SPAM_STOP_EVENTS:
                    SPAM_STOP_EVENTS[c_id].set()
                    del SPAM_STOP_EVENTS[c_id]
                    send_msg(c_id, f"✅ All multi-token spam threads stopped", token=self.token)
                else:
                    send_msg(c_id, "ℹ️ No active spam", token=self.token)
                return

            # ---------- $spam2 ----------
            if cmd_lower.startswith("spam2 "):
                parts = cmd_part.split()
                if len(parts) < 2:
                    send_msg(c_id, "❌ Usage: $spam2 <target>", token=self.token)
                    return
                target_str = parts[1]
                target_name = extract_target_info(target_str, self.token)
                if c_id not in SPAM2_STOP_EVENTS:
                    SPAM2_STOP_EVENTS[c_id] = threading.Event()
                else:
                    SPAM2_STOP_EVENTS[c_id].set()
                    SPAM2_STOP_EVENTS[c_id] = threading.Event()
                ACTIVE_SPAM2_CHANNELS[key_suffix] = True
                threading.Thread(target=spam2_worker, args=(c_id, target_name, self.token), daemon=True).start()
                send_msg(c_id, f"✅ Spam2 started for {target_name}", token=self.token)
                return

            # ---------- $stopspam2 ----------
            if cmd_lower == "stopspam2":
                if c_id in SPAM2_STOP_EVENTS:
                    SPAM2_STOP_EVENTS[c_id].set()
                    ACTIVE_SPAM2_CHANNELS[key_suffix] = False
                    send_msg(c_id, "✅ Spam2 stopped", token=self.token)
                else:
                    send_msg(c_id, "ℹ️ No active spam2", token=self.token)
                return

            # ---------- $customspam ----------
            if cmd_lower.startswith("customspam "):
                parts = cmd_part.split(maxsplit=1)
                if len(parts) < 2:
                    send_msg(c_id, "❌ Usage: $customspam <text>", token=self.token)
                    return
                custom_text = parts[1]
                if c_id not in CUSTOM_SPAM_STOP_EVENTS:
                    CUSTOM_SPAM_STOP_EVENTS[c_id] = threading.Event()
                else:
                    CUSTOM_SPAM_STOP_EVENTS[c_id].set()
                    CUSTOM_SPAM_STOP_EVENTS[c_id] = threading.Event()
                ACTIVE_CUSTOM_SPAM_CHANNELS[key_suffix] = True
                threading.Thread(target=custom_spam_worker, args=(c_id, custom_text, self.token), daemon=True).start()
                send_msg(c_id, f"✅ Custom spam started for: `{custom_text[:30]}...`", token=self.token)
                return

            # ---------- $stopcustomspam ----------
            if cmd_lower == "stopcustomspam":
                if c_id in CUSTOM_SPAM_STOP_EVENTS:
                    CUSTOM_SPAM_STOP_EVENTS[c_id].set()
                    ACTIVE_CUSTOM_SPAM_CHANNELS[key_suffix] = False
                    send_msg(c_id, "✅ Custom spam stopped", token=self.token)
                else:
                    send_msg(c_id, "ℹ️ No active custom spam", token=self.token)
                return

            # ---------- $picspam ----------
            if cmd_lower.startswith("picspam "):
                parts = cmd_part.split(maxsplit=1)
                if len(parts) < 2:
                    send_msg(c_id, "❌ Usage: $picspam <image_url>", token=self.token)
                    return
                url = parts[1]
                file_path = download_image(url)
                if not file_path:
                    send_msg(c_id, "❌ Failed to download image from URL", token=self.token)
                    return
                if c_id not in PIC_SPAM_STOP_EVENTS:
                    PIC_SPAM_STOP_EVENTS[c_id] = threading.Event()
                else:
                    PIC_SPAM_STOP_EVENTS[c_id].set()
                    PIC_SPAM_STOP_EVENTS[c_id] = threading.Event()
                ACTIVE_PIC_SPAM_CHANNELS[key_suffix] = True
                threading.Thread(target=pic_spam_worker, args=(c_id, file_path, self.token), daemon=True).start()
                send_msg(c_id, f"✅ Pic spam started (image: {os.path.basename(file_path)})", token=self.token)
                return

            # ---------- $stoppicspam ----------
            if cmd_lower == "stoppicspam":
                if c_id in PIC_SPAM_STOP_EVENTS:
                    PIC_SPAM_STOP_EVENTS[c_id].set()
                    ACTIVE_PIC_SPAM_CHANNELS[key_suffix] = False
                    send_msg(c_id, "✅ Pic spam stopped", token=self.token)
                else:
                    send_msg(c_id, "ℹ️ No active pic spam", token=self.token)
                return

            # ---------- $join ----------
            if cmd_lower.startswith("join "):
                parts = cmd_part.split()
                if len(parts) < 2:
                    send_msg(c_id, "❌ Usage: $join <invite_code>", token=self.token)
                    return
                invite = parts[1].strip()
                if '/' in invite:
                    invite = invite.split('/')[-1]
                success = join_server(invite, self.token)
                if success:
                    send_msg(c_id, f"✅ Joined server using invite `{invite}`", token=self.token)
                else:
                    send_msg(c_id, f"❌ Failed to join server", token=self.token)
                return

            # ---------- $autoreply ----------
            if cmd_lower.startswith("autoreply "):
                parts = cmd_part.split()
                if len(parts) < 2:
                    send_msg(c_id, "❌ Usage: $autoreply @user1 @user2 ...", token=self.token)
                    return
                user_ids = []
                for mention in parts[1:]:
                    uid = extract_user_id_from_mention(mention)
                    if uid:
                        user_ids.append(uid)
                if not user_ids:
                    send_msg(c_id, "❌ No valid user mentions", token=self.token)
                    return
                if c_id not in AUTOREPLY_TARGETS:
                    AUTOREPLY_TARGETS[c_id] = []
                for uid in user_ids:
                    if uid not in AUTOREPLY_TARGETS[c_id]:
                        AUTOREPLY_TARGETS[c_id].append(uid)
                send_msg(c_id, f"✅ Autoreply targets added: {len(user_ids)} user(s)", token=self.token)
                return

            # ---------- $removeautoreply ----------
            if cmd_lower.startswith("removeautoreply "):
                parts = cmd_part.split()
                if len(parts) < 2:
                    send_msg(c_id, "❌ Usage: $removeautoreply @user", token=self.token)
                    return
                mention = parts[1]
                uid = extract_user_id_from_mention(mention)
                if not uid:
                    send_msg(c_id, "❌ Invalid mention", token=self.token)
                    return
                if c_id in AUTOREPLY_TARGETS and uid in AUTOREPLY_TARGETS[c_id]:
                    AUTOREPLY_TARGETS[c_id].remove(uid)
                    if not AUTOREPLY_TARGETS[c_id]:
                        del AUTOREPLY_TARGETS[c_id]
                    send_msg(c_id, f"✅ Removed {mention}", token=self.token)
                else:
                    send_msg(c_id, f"ℹ️ {mention} not in list", token=self.token)
                return

            # ---------- $stopautoreply ----------
            if cmd_lower == "stopautoreply":
                if c_id in AUTOREPLY_TARGETS:
                    del AUTOREPLY_TARGETS[c_id]
                    send_msg(c_id, "✅ Cleared all targets", token=self.token)
                else:
                    send_msg(c_id, "ℹ️ No active targets", token=self.token)
                return

            # ---------- $autoreact ----------
            if cmd_lower.startswith("autoreact "):
                parts = cmd_part.split()
                if len(parts) < 2:
                    send_msg(c_id, "❌ Usage: $autoreact <emoji>", token=self.token)
                    return
                emoji = parts[1]
                AUTOREACT_EMOJIS[c_id] = emoji
                send_msg(c_id, f"✅ Autoreact set to {emoji}", token=self.token)
                return

            # ---------- $stopautoreact ----------
            if cmd_lower == "stopautoreact":
                if c_id in AUTOREACT_EMOJIS:
                    del AUTOREACT_EMOJIS[c_id]
                    send_msg(c_id, "✅ Stopped", token=self.token)
                else:
                    send_msg(c_id, "ℹ️ Not active", token=self.token)
                return

            # ---------- $rgb ----------
            if cmd_lower == "rgb":
                for _ in range(25):
                    for emoji in RGB_EMOJIS:
                        send_msg(c_id, emoji, token=self.token)
                return

            # ---------- $hug ----------
            if cmd_lower.startswith("hug "):
                parts = cmd_part.split()
                if len(parts) < 2:
                    send_msg(c_id, "❌ Usage: $hug @user", token=self.token)
                    return
                mention = parts[1]
                target_name = extract_target_info(mention, self.token)
                hug_msg = (
                    f"🤗 **{target_name}** 🤗\n\n"
                    "⊱ ────── {.⋅ ✯ ⋅.} ────── ⊰\n"
                    "    𝐘𝐨𝐮 𝐚𝐫𝐞 𝐬𝐨 𝐥𝐨𝐯𝐞𝐝! 𝐇𝐞𝐫𝐞'𝐬 𝐚 𝐡𝐮𝐠!\n"
                    "    ʚ♡ɞ  ♡  ʚ♡ɞ  ♡  ʚ♡ɞ  ♡  ʚ♡ɞ\n"
                    "    ₊˚.༄  𝗛𝗨𝗚𝗚𝗚𝗚𝗚𝗚𝗦!  ༄.˚₊\n"
                    "    ʚ♡ɞ  ♡  ʚ♡ɞ  ♡  ʚ♡ɞ  ♡  ʚ♡ɞ\n"
                    "⊱ ────── {.⋅ ✯ ⋅.} ────── ⊰"
                )
                send_msg(c_id, hug_msg, token=self.token)
                return

            # ---------- $ping ----------
            if cmd_lower == "ping":
                start = time.time()
                requests.get("https://discord.com/api/v9/users/@me", headers={"Authorization": self.token})
                latency = round((time.time() - start) * 1000, 2)
                send_msg(c_id, f"🏓 Pong! {latency}ms", token=self.token)
                return

            # ---------- $status ----------
            if cmd_lower == "status":
                uptime = round(time.time() - START_TIME, 1)
                status_msg = (
                    "```\n"
                    f"📊 BOT STATUS\n"
                    f"Uptime: {uptime}s\n"
                    f"NC Active: {'Yes' if ACTIVE_NC_CHANNELS.get(key_suffix) else 'No'}\n"
                    f"Custom NC Active: {'Yes' if ACTIVE_CUSTOM_NC_CHANNELS.get(key_suffix) else 'No'}\n"
                    f"NC MX Active: {'Yes' if ACTIVE_NCMX_CHANNELS.get(key_suffix) else 'No'}\n"
                    f"Multi-Token Spam: {'Yes' if c_id in SPAM_STOP_EVENTS else 'No'}\n"
                    f"Spam2 Active: {'Yes' if ACTIVE_SPAM2_CHANNELS.get(key_suffix) else 'No'}\n"
                    f"Custom Spam Active: {'Yes' if ACTIVE_CUSTOM_SPAM_CHANNELS.get(key_suffix) else 'No'}\n"
                    f"Pic Spam Active: {'Yes' if ACTIVE_PIC_SPAM_CHANNELS.get(key_suffix) else 'No'}\n"
                    f"Total Tokens: {len(TOKENS)}\n"
                    f"Autoreply: {AUTOREPLY_TARGETS.get(c_id, [])}\n"
                    f"Autoreact: {AUTOREACT_EMOJIS.get(c_id, 'None')}\n"
                    f"Owner: {OWNER_ID}\n"
                    f"Access Users: {len(SUDO_USERS)}\n"
                    "```"
                )
                send_msg(c_id, status_msg, token=self.token)
                return

            # ---------- $showusers ----------
            if cmd_lower == "showusers":
                if not SUDO_USERS:
                    send_msg(c_id, "ℹ️ No access users added yet.", token=self.token)
                    return
                user_list = "\n".join([f"<@{uid}>" for uid in SUDO_USERS])
                send_msg(c_id, f"📋 **Access Users:**\n{user_list}", token=self.token)
                return

            # ---------- $access ----------
            if cmd_lower.startswith("access "):
                if auth_id != OWNER_ID:
                    send_msg(c_id, "❌ Only the owner can grant access.", token=self.token)
                    return
                parts = cmd_part.split()
                if len(parts) < 2:
                    send_msg(c_id, "❌ Usage: $access @user", token=self.token)
                    return
                mention = parts[1]
                user_id = extract_user_id_from_mention(mention)
                if not user_id:
                    send_msg(c_id, "❌ Invalid mention", token=self.token)
                    return
                if user_id in SUDO_USERS:
                    send_msg(c_id, "ℹ️ Already has access", token=self.token)
                else:
                    SUDO_USERS.append(user_id)
                    save_sudo(SUDO_USERS)
                    send_msg(c_id, f"✅ Granted access to {mention}", token=self.token)
                return

            # ---------- $removeaccess ----------
            if cmd_lower.startswith("removeaccess "):
                if auth_id != OWNER_ID:
                    send_msg(c_id, "❌ Only the owner can revoke access.", token=self.token)
                    return
                parts = cmd_part.split()
                if len(parts) < 2:
                    send_msg(c_id, "❌ Usage: $removeaccess @user", token=self.token)
                    return
                mention = parts[1]
                user_id = extract_user_id_from_mention(mention)
                if not user_id:
                    send_msg(c_id, "❌ Invalid mention", token=self.token)
                    return
                if user_id in SUDO_USERS:
                    SUDO_USERS.remove(user_id)
                    save_sudo(SUDO_USERS)
                    send_msg(c_id, f"✅ Removed access from {mention}", token=self.token)
                else:
                    send_msg(c_id, "ℹ️ User doesn't have access", token=self.token)
                return

            # ---------- $stopall ----------
            if cmd_lower == "stopall":
                nc_active = ACTIVE_NC_CHANNELS.get(key_suffix) or ACTIVE_CUSTOM_NC_CHANNELS.get(key_suffix) or ACTIVE_NCMX_CHANNELS.get(key_suffix)
                spam_active = c_id in SPAM_STOP_EVENTS
                spam2_active = ACTIVE_SPAM2_CHANNELS.get(key_suffix)
                custom_spam_active = ACTIVE_CUSTOM_SPAM_CHANNELS.get(key_suffix)
                pic_active = ACTIVE_PIC_SPAM_CHANNELS.get(key_suffix)
                autoreply_active = c_id in AUTOREPLY_TARGETS
                autoreact_active = c_id in AUTOREACT_EMOJIS

                if not any([nc_active, spam_active, spam2_active, custom_spam_active, pic_active, autoreply_active, autoreact_active]):
                    send_msg(c_id, "❌ All operations can't be stopped ❌ (Nothing was active!)", token=self.token)
                    return

                ACTIVE_NC_CHANNELS[key_suffix] = False
                ACTIVE_CUSTOM_NC_CHANNELS[key_suffix] = False
                ACTIVE_NCMX_CHANNELS[key_suffix] = False

                if c_id in SPAM_STOP_EVENTS:
                    SPAM_STOP_EVENTS[c_id].set()
                    del SPAM_STOP_EVENTS[c_id]

                ACTIVE_SPAM2_CHANNELS[key_suffix] = False
                ACTIVE_CUSTOM_SPAM_CHANNELS[key_suffix] = False
                ACTIVE_PIC_SPAM_CHANNELS[key_suffix] = False

                if c_id in AUTOREPLY_TARGETS:
                    del AUTOREPLY_TARGETS[c_id]
                if c_id in AUTOREACT_EMOJIS:
                    del AUTOREACT_EMOJIS[c_id]

                send_msg(c_id, "✅ All operations stopped successfully ✅", token=self.token)
                return

    def run(self):
        while self.running:
            try:
                self.ws = websocket.WebSocketApp("wss://gateway.discord.gg/?v=9&encoding=json",
                                                  on_message=self.on_message)
                self.ws.run_forever()
            except Exception as e:
                print(f"\033[91m[!] Bot {self.bot_index + 1} error: {e}\033[0m")
                time.sleep(5)

# --- LAUNCH ALL BOTS ---
def run_all_bots():
    global TOKENS

    print("\033[95m" + "=" * 55)
    print("      🔥 ULTRA-FAST MULTI-TOKEN BOT 🔥")
    print("=" * 55 + "\033[0m")

    if not TOKENS:
        print("\033[91m[!] No tokens configured!\033[0m")
        return

    clean_tokens = [t.strip() for t in TOKENS if t and t.strip() and not t.startswith('.')]

    print(f"\033[93m[!] Owner ID: {OWNER_ID}\033[0m")
    print(f"\033[93m[!] Total tokens loaded: {len(clean_tokens)}\033[0m")
    print("\033[93m[!] Verifying tokens...\033[0m")

    valid_tokens = []
    for i, token in enumerate(clean_tokens):
        print(f"\033[93m[~] Checking bot {i+1}...\033[0m")
        user_id = verify_owner_id(token)
        if user_id:
            print(f"\033[92m[✓] Bot {i+1} verified (User ID: {user_id})\033[0m")
            valid_tokens.append(token)
        else:
            print(f"\033[91m[✗] Bot {i+1} - INVALID or EXPIRED token!\033[0m")

    if not valid_tokens:
        print("\033[91m[!] No valid tokens found. Exiting...\033[0m")
        return

    TOKENS = valid_tokens

    print(f"\n\033[92m[✓] {len(valid_tokens)} valid tokens found!\033[0m")
    print("\n\033[93m[!] Starting bot instances...\033[0m\n")

    bots = []
    for i, token in enumerate(valid_tokens):
        bot = DiscordSelfBot(token, i)
        thread = threading.Thread(target=bot.run, daemon=True)
        thread.start()
        bots.append(bot)
        time.sleep(2)

    print("\033[92m[✓] All bots are now running!\033[0m")
    print("\033[93m[!] Commands:\n"
          "  $nc @user | $stopnc\n"
          "  $customnc <text> | $stopcustomnc\n"
          "  $ncmx <text> | $stopncmx (NEW RGB MX NC!)\n"
          "  $spam @user | $stopspam  (⚡ 0.05s ULTRA-FAST SPAM)\n"
          "  $spam2 <target> | $stopspam2\n"
          "  $customspam <text> | $stopcustomspam\n"
          "  $picspam <url> | $stoppicspam\n"
          "  $join <invite> | $autoreply ...\n"
          "  $leavegc | $rgb | $hug @user (Fun Commands!)\n"
          "  $ping | $status | $showusers\n"
          "  $access @user | $removeaccess @user (owner only)\n"
          "  $stopall (Kills everything at once)\n"
          "  $help\033[0m")
    print(f"\033[93m[!] Ultra-Fast mode: {len(valid_tokens)} tokens active!\033[0m")
    print("\033[93m[!] Press Ctrl+C to stop all bots\033[0m")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\033[91m[!] Shutting down all bots...\033[0m")
        for bot in bots:
            bot.running = False
        print("\033[92m[✓] All bots stopped.\033[0m")

if __name__ == "__main__":
    run_all_bots()
