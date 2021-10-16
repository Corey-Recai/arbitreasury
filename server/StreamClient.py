import websocket
import json

class StreamClient:
    def __init__(self, pair, channel):
        # "wss://stream.binance.com:9443/ws/bnbusdt@trade"
        base = 'wss://stream.binance.com:9443/ws/'
        self.url = f'{base}{pair[0]}{pair[1]}@{channel}'
        
    def __on_message(self, ws, message):
        print(json.loads(message))

    def __on_error(self, ws, error):
        print(error)

    def __on_close(self, ws):
        print("### closed ###")

    def __on_open(self, ws):
        print("### opened ###")


    def run(self):
        websocket.enableTrace(True)
        ws = websocket.WebSocketApp(self.url,
                                  on_message = self.__on_message,
                                  on_error = self.__on_error,
                                  on_close = self.__on_close)
        ws.on_open = self.__on_open
        ws.run_forever()