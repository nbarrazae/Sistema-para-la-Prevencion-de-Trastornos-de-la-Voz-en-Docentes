import time
import curses

def pbar(window,count):
    window.addstr(0, 0, f"Progress: {count}")
    window.refresh()
    time.sleep(0.5)

for i in range(10):
    curses.wrapper(pbar,i)