import PyChromeDevTools

import ast
import time
import random
import string

import pyautogui as pg
##from pynput.keyboard import Key, Controller


def decode(s):
    x = []
    for i in range(len(s)):
        j = ord(s[i])
        if j >= 33 and j <= 126:
            x.append(chr(33 + ((j + 14) % 94)))
        else:
            x.append(s[i])
    return ''.join(x)[::-1]


chrome = PyChromeDevTools.ChromeInterface()
chrome.Network.enable()
chrome.Page.enable()

##keyboard = Controller()
counter = 0
rest = random.randint(200, 500)
nitroCount = 485

while True:
    chrome.Page.navigate(url="https://www.nitrotype.com/race")
    ##pg.typewrite("\n")
    event, messages = chrome.wait_event("Page.frameStoppedLoading", timeout=60)

    line = ""
    leave = False
    accuracy = random.randint(92, 98)

    while True:
        event, messages = chrome.wait_event("Page.frameStoppedLoading", timeout=60)
        for m in messages:
            if "method" in m and m["method"] == "Network.webSocketFrameReceived":
                try:
                    if ast.literal_eval(m["params"]["response"]["payloadData"][1:])["msg"] == "status":
                        ## Get the line to type
                        line = decode(ast.literal_eval(m["params"]["response"]["payloadData"][1:])["payload"]["l"])
                        counter = counter + 1
                    if ast.literal_eval(m["params"]["response"]["payloadData"][1:])["msg"] == "update":
                        leave = True
                        break
                except:
                    pass
        if leave:
            break

    print str(counter),line,accuracy,"\n"
    """
    ## Decrease accuracy for realistic effect
    for x in range(0, len(line)):
        if (random.randint(0, 100) > 94):
            line = line[:x] + chr(random.randint(97, 122)) + line[x:]
	"""
    nitros = 3

    for char in line:
        if (random.randint(0, 100) > accuracy):
            pg.typewrite(random.choice(string.ascii_letters))
            time.sleep(random.uniform(0.005, 0.01))  ## slightly longer pause after you mess up
        pg.typewrite(char)
        time.sleep(random.uniform(0.007, 0.015))
        if (random.randint(0, 100) > 95):  ## long pause
            time.sleep(random.uniform(0.1, 0.15))

    ## Wait until next race
    if counter % rest == 0:
        rest = random.randint(200, 500)
        time.sleep(random.randint(300, 900))
    time.sleep(random.randint(3, 10))
