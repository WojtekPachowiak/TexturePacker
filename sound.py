import winsound
from threading import Thread

class Sound:
    def beep():
        duration = 300  # milliseconds
        freq = 440  # Hz
        Thread(
            target=lambda: winsound.Beep(freq, duration)
        ).start()
        
        