import logging
import socketserver
import struct
import threading
import time

log = logging.getLogger("movienightserver")


class SyncHandler(socketserver.BaseRequestHandler):
    def handle(self):
        try:
            if self not in self.server.clients:
                with self.server.lock:
                    self.server.clients.append(self)
                    log.debug("Added a new client: %s", self.client_address)
                    log.debug("Total clients: %i", len(self.server.clients))

            while True:
                data = self.request.recv(1024)
                log.debug("%s: %s", self.client_address[0], data)
                setting, playing, time, heartbeat = struct.unpack(">??I?", data)

                if heartbeat:
                    log.debug("Heartbeat received")
                    continue

                if not setting:
                    log.debug("Getting")
                    with self.server.lock:
                        self.request.sendall(struct.pack(">?I?", self.server.playing, self.server.time, False))
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
                            client.request.sendall(struct.pack(">?I?", self.server.playing, self.server.time, False))
        except ConnectionError:
            pass
        finally:
            with self.server.lock:
                self.server.clients.remove(self)
                log.debug("Removed a client: %s", self.client_address)
                log.debug("Total clients: %i", len(self.server.clients))


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    allow_reuse_address = True

    def __init__(self, *args, **kwargs):
        super(ThreadedTCPServer, self).__init__(*args, **kwargs)
        self.lock = threading.Lock()
        self.time = 0
        self.playing = False
        self.clients = []
        self.heartbeat_thread = threading.Thread(target=self.heartbeat)
        self.heartbeat_thread.daemon = True
        self.heartbeat_thread.start()

    def heartbeat(self):
        log.debug("Heartbeat thread started.")
        while True:
            if self.clients:
                with self.lock:
                    log.debug("Sending heartbeat...")
                    for client in self.clients:
                        client.request.sendall(struct.pack(">?I?", self.playing, self.time, True))
                    log.debug("Heartbeat sent!")
            time.sleep(60)


def main():
    with ThreadedTCPServer(("0.0.0.0", 9512), SyncHandler) as server:
        server_thread = threading.Thread(target=server.serve_forever)
        server_thread.daemon = True
        server_thread.start()
        server_thread.join()


if __name__ == "__main__":
    main()
