import tornado.ioloop
import tornado.tcpserver
import tornado.iostream
import socket
import processData
import Constants

class Session:
    def __init__(self, stream, address, proxy):
        self.proxy = proxy
        self.c2p_stream = stream
        self.c2p_address = address
        self.c2p_state = 'CONNECTED'
        self.c2s_queued_data = []
        self.s2c_queued_data = []

        self.c2p_stream.set_nodelay(True)
        self.c2p_stream.set_close_callback(self.on_c2p_close)

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
        self.p2s_stream = tornado.iostream.IOStream(s)
        self.p2s_stream.set_nodelay(True)
        self.p2s_stream.set_close_callback(self.on_p2s_close)
        self.p2s_state = 'CONNECTING'
        self.p2s_stream.connect((proxy.target_server, proxy.target_port), self.on_p2s_done_connect)
        self.c2p_start_read()

    def c2p_start_read(self):
        self.c2p_stream.read_until_close(lambda x: None, self.on_c2p_done_read)

    def p2s_start_read(self):
        self.p2s_stream.read_until_close(lambda x: None, self.on_p2s_done_read)

    def on_c2p_done_read(self, data):
        if processData.parseData(data):
            self.p2s_start_write(data)
        else:
            data = processData.prep_error_response("you are doing something mischievous")
            self.c2p_start_write(data)
            self.p2s_stream.close()

    def on_p2s_done_read(self, data):
        self.c2p_start_write(data)

    def c2p_start_write(self, data):
        self.c2p_stream.write(data, callback=self.on_c2p_done_write)

    def p2s_start_write(self, data):
        self.p2s_stream.write(data, callback=self.on_p2s_done_write)

    def on_c2p_done_write(self):
        pass

    def on_p2s_done_write(self):
        pass

    def on_c2p_close(self):
        self.c2p_state = 'CLOSED'
        if self.p2s_state == 'CLOSED':
            self.proxy.remove_session(self)
        else:
            self.p2s_stream.close()

    def on_p2s_close(self):
        self.p2s_state = 'CLOSED'
        if self.c2p_state == 'CLOSED':
            self.proxy.remove_session(self)
        else:
            self.c2p_stream.close()

    def on_p2s_done_connect(self):
        self.p2s_state = 'CONNECTED'
        self.p2s_start_read()

class ProxyServer(tornado.tcpserver.TCPServer):
    def __init__(self, target_server, target_port, *args, **kwargs):
        self.target_server = target_server
        self.target_port = target_port
        self.sessions = []
        super().__init__(*args, **kwargs)

    def handle_stream(self, stream, address):
        session = Session(stream, address, self)
        self.sessions.append(session)

    def remove_session(self, session):
        self.sessions.remove(session)

def main():
    server = ProxyServer(Constants.HOST_SERVER_IP, Constants.WEB_HOST_PORT)
    server.listen(Constants.RP_PORT)
    tornado.ioloop.IOLoop.current().start()

if __name__ == '__main__':
    main()