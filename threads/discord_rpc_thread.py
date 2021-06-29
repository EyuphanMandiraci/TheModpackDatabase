from PyQt5 import QtCore
import discord_rpc
import time


class DiscordRPCThread(QtCore.QThread):
    def __init__(self):
        super().__init__()
        self.any_signal = QtCore.pyqtSignal()

    def run(self):
        discord_rpc.initialize("4b0085422009992f152be2fdf328aac0fbde4dcc8e410f26fe44b4e97d974004")
        i = 0
        start = time.time()
        while i < 10000000:
            i += 1
            discord_rpc.update_presence(
                **{
                    'details': 'Iteration # {}'.format(i),
                    'start_timestamp': start,
                    'large_image_key': 'sa'
                }
            )
            discord_rpc.update_connection()
            time.sleep(2)
        self.any_signal.emit()

    def stop(self):
        print("Stopping")
        self.wait()