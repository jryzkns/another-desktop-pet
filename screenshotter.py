from datetime import datetime as dt
from mss import mss
from os.path import join, exists
from os import mkdir

def take_screenie(path = "."):
    if not exists(path): mkdir(path)
    with mss() as sct:
        sct.shot(output=join(path, gen_fn_now()))

def gen_fn_now():
    return f'{dt.now().strftime("%m-%d-%Y-%H-%M-%S")}.png'
