import pygame as pg
from tkinter import *
from tkinter import messagebox


def format_time(sec):
    seconds = sec % 60
    minutes = sec // 60
    curr_time = str(minutes) + ":" + (str(seconds) if seconds > 9 else "0" + str(seconds))
    return curr_time


def get_key(key):
    switcher = {
        pg.K_1: 1,
        pg.K_2: 2,
        pg.K_3: 3,
        pg.K_4: 4,
        pg.K_5: 5,
        pg.K_6: 6,
        pg.K_7: 7,
        pg.K_8: 8,
        pg.K_9: 9,
    }
    return switcher.get(key, None)


def show_messagebox(title, body):
    Tk().wm_withdraw()
    messagebox.showinfo(title, body)
