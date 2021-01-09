from datetime import datetime as dt
from mss import mss
from os.path import join

def take_screenie(path = "."):
    with mss() as sct:
        sct.shot(output=join(path,gen_fn_now()))

def gen_fn_now():
    return f'{dt.now().strftime("%m-%d-%Y-%H-%M-%S")}.png'
