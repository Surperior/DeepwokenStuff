import cv2
import numpy as np
import mss
import vlc

current_zone = 1

def get_hp():
    with mss.mss() as sct:
        region = {
            "left": 978,
            "top": 1249,
            "width": 604,
            "height": 82
        }
        img = np.array(sct.grab(region))

        bar = img

        hsv = cv2.cvtColor(bar, cv2.COLOR_BGR2HSV)

        lower = np.array([5, 50, 50])
        upper = np.array([30, 255, 255])

        mask = cv2.inRange(hsv, lower, upper)

        columns = np.sum(mask > 0, axis=0)

        filled = np.where(columns > 5)[0]

        if len(filled):
            fill_width = filled.max()
            hp_percent = (fill_width / mask.shape[1] * 100) -0.4
            print(f"{hp_percent:.1f}%")
            return hp_percent

def get_zone(hp):
    if hp == None:
        return current_zone
    if hp >= 70:
        return 1
    elif hp >= 40:
        return 2
    elif hp < 40:
        return 3

player = vlc.MediaPlayer("Keter.mp3")
player.audio_set_volume(45)
player.play()

zones = {
    1: (0, 38450),
    2: (38450, 72350),
    3: (72350, 117551)
}

def switch_music(zone):
    start, end = zones[zone]
    sfx = vlc.MediaPlayer("Snap.mp3")
    sfx.audio_set_volume(60)
    sfx.play()
    player.set_time(start)
    

while True:
    hp = get_hp()

    start, end = zones[current_zone]

    if player.get_time() >= end:
        player.set_time(start)

    new_zone = get_zone(hp)

    if new_zone != current_zone:
        current_zone = new_zone
        switch_music(new_zone)