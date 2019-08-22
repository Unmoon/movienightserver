import logging
import socketserver
import struct
import threading
from time import sleep

log = logging.getLogger(__name__)


class SyncHandler(socketserver.BaseRequestHandler):
    def handle(self):
        try:
            if self not in self.server.clients:
                with self.server.lock:
                    self.server.clients.append(self)
                    log.debug("Added a new client: %s", self)
                    log.debug("Total clients: %i", len(self.server.clients))

            while True:
                data = self.request.recv(1024)
                log.debug("%s: %s", self.client_address[0], data)
                setting, playing, time = struct.unpack(">??I", data)

                if not setting:
                    log.debug("Getting")
                    with self.server.lock:
                        self.request.sendall(
                            struct.pack(">?I", self.server.playing, self.server.time)
                        )
                else:
                    with self.server.lock:
                        self.server.time = time
                        self.server.playing = playing
                        log.debug(
                            "%s %i",
                            "Playing from" if playing else "Pausing at",
                            self.server.time,
                        )
                        for client in self.server.clients:
                            if self == client:
                                continue
                            client.request.sendall(
                                struct.pack(
                                    ">?I", self.server.playing, self.server.time
                                )
                            )
        finally:
            with self.server.lock:
                self.server.clients.remove(self)
                log.debug("Removed a client: %s", self)
                log.debug("Total clients: %i", len(self.server.clients))


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    def __init__(self, *args, **kwargs):
        super(ThreadedTCPServer, self).__init__(*args, **kwargs)
        self.lock = threading.Lock()
        self.time = 0
        self.playing = False
        self.clients = []


def main():
    with ThreadedTCPServer(("localhost", 9512), SyncHandler) as server:
        server_thread = threading.Thread(target=server.serve_forever)
        server_thread.daemon = True
        server_thread.start()
        while True:
            sleep(1)
