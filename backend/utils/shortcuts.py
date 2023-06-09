import os
import re
import datetime
import random
from base64 import b64encode
from io import BytesIO

from django.utils.crypto import get_random_string
from envelopes import Envelope

def ffff(id):
    file_name = id+".txt"
    DIR = os.path.dirname(os.path.dirname(__file__))
    COMPILE_RESULT__DIR = f"{DIR}/profileResult/results"
    path = os.path.join(COMPILE_RESULT__DIR, file_name)
    f = open(path, 'r')
    for i in range(0, 10):
        f.readline()
    lines = f.readlines()
    line = []
    hits = []
    time = []
    per_time = []
    for l in lines:
        arr = l.split()
        if len(arr)<2: continue
        if arr[1].isdigit():
            line.append(int(arr[0])-2)
            hits.append(int(arr[1]))
            time.append(float(arr[2]))
            per_time.append(float(arr[4]))
    f.close()
    return line, hits, time, per_time

def fffm(id):
    file_name = id+"m.txt"
    DIR = os.path.dirname(os.path.dirname(__file__))
    COMPILE_RESULT__DIR = f"{DIR}/profileResult/results"
    path = os.path.join(COMPILE_RESULT__DIR, file_name)
    f = open(path, 'r')
    for i in range(0, 10):
        f.readline()
    lines = f.readlines()
    line_m = []
    increment = []
    for l in lines:
        arr = l.split()
        if len(arr)<2: continue
        if arr[1].isdigit():
            line_m.append(int(arr[0])-2)
            increment.append(float(arr[4]))
    f.close()
    return line_m, increment

def file_func(t1, code):
            str_arr = code.split('\n')
            for i in range(0, len(str_arr)):
                s = '\t' + str_arr[i] + '\n'
                t1.write(s)

def rand_str(length=32, type="lower_hex"):
    """
    Generate random strings or numbers of specified length, which can be used in security scenarios such as keys
    :param length: length of string or number
    :param type: str represents a random string, num represents a random number
    :return: string
    """
    if type == "str":
        return get_random_string(length, allowed_chars="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789")
    elif type == "lower_str":
        return get_random_string(length, allowed_chars="abcdefghijklmnopqrstuvwxyz0123456789")
    elif type == "lower_hex":
        return random.choice("123456789abcdef") + get_random_string(length - 1, allowed_chars="0123456789abcdef")
    else:
        return random.choice("123456789") + get_random_string(length - 1, allowed_chars="0123456789")


def build_query_string(kv_data, ignore_none=True):
    # {"a": 1, "b": "test"} -> "?a=1&b=test"
    query_string = ""
    for k, v in kv_data.items():
        if ignore_none is True and kv_data[k] is None:
            continue
        if query_string != "":
            query_string += "&"
        else:
            query_string = "?"
        query_string += (k + "=" + str(v))
    return query_string


def img2base64(img):
    with BytesIO() as buf:
        img.save(buf, "gif")
        buf_str = buf.getvalue()
    img_prefix = "data:image/png;base64,"
    b64_str = img_prefix + b64encode(buf_str).decode("utf-8")
    return b64_str


def datetime2str(value, format="iso-8601"):
    if format.lower() == "iso-8601":
        value = value.isoformat()
        if value.endswith("+00:00"):
            value = value[:-6] + "Z"
        return value
    return value.strftime(format)


def timestamp2utcstr(value):
    return datetime.datetime.utcfromtimestamp(value).isoformat()


def natural_sort_key(s, _nsre=re.compile(r"(\d+)")):
    return [int(text) if text.isdigit() else text.lower()
            for text in re.split(_nsre, s)]


def send_email(smtp_config, from_name, to_email, to_name, subject, content):
    envelope = Envelope(from_addr=(smtp_config["email"], from_name),
                        to_addr=(to_email, to_name),
                        subject=subject,
                        html_body=content)
    return envelope.send(smtp_config["server"],
                         login=smtp_config["email"],
                         password=smtp_config["password"],
                         port=smtp_config["port"],
                         tls=smtp_config["tls"])


def get_env(name, default=""):
    return os.environ.get(name, default)


def DRAMATIQ_WORKER_ARGS(time_limit=3600_000, max_retries=0, max_age=7200_000):
    return {"max_retries": max_retries, "time_limit": time_limit, "max_age": max_age}


def check_is_id(value):
    try:
        return int(value) > 0
    except Exception:
        return False

def file_func(t1, code):
            t1.write('@profile\n')
            t1.write('def main():\n')
            lines = code.split('\n')
            for i, line in enumerate(lines):
                if 'import' in line:
                    continue
                t1.write('\t' + line + '\n')
            t1.write('main()\n')

def skip_import(t1, code):
    lines = code.split('\n')
    for i, line in enumerate(lines):
        if 'import' not in line:
            break
        else:
            t1.write(line+'\n')
            continue
