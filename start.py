import os
import time

def anime(text):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(0.09)  # Uncommented

os.system("clear")
impmsg = "\n\033[1;34mThis Tool is Free For Our subscribers\nWe are Redirecting You To Our YouTube Channel\nYou Have to Subscribe Our Channel\nAfter Doing It You Will Able To Use Our Tool." 
anime(impmsg)
time.sleep(1.5)  # Wait for 8 seconds

channel_url = 'https://youtube.com/@hackers_colony_tech?si=7FEalwT2t0khmivd'
os.system(f'termux-open {channel_url}')  # Opens the channel URL in Termux
time.sleep(5)  # Wait for 4 seconds
os.system("clear")
os.system("mv sites .sites")
os.system("chmod +x *")
os.system("bash HCO-Phisher.sh")