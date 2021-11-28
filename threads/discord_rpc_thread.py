from PyQt5 import QtCore
import time
import rpc


class DiscordRPCThread(QtCore.QThread):
    any_signal = QtCore.pyqtSignal()

    def __init__(self):
        super(DiscordRPCThread, self).__init__(None)


    def run(self):
        client_id = "4b0085422009992f152be2fdf328aac0fbde4dcc8e410f26fe44b4e97d974004"
        rpc_obj = rpc.DiscordIpcClient.for_platform(client_id)
        print("RPC Connection Başarılı")
        time.sleep(5)
        start_time = time.mktime(time.localtime())
        while True:
            activity = {
                "state": "MPDB",
                "details": "ModpackDatabase",
                "timestamps": {"start": start_time},
                "assets": {
                    "small_text": "SA",
                    "small_image": "sa"
                }
            }
            rpc_obj.set_activity(activity)
            time.sleep(900)
        self.any_signal.emit()

    def stop(self):
        print("Stopping")
        self.wait()