import socket, threading, time, ipaddress


from server.player import *
from server.unit import UnitTypes
from server.vmath import from_bytes
from random import randint as rd


class Host:
    playerNumber: int
    sock: socket.socket
    connections: list[socket.socket]
    game: Game
    PlayersneedUpdate: int

    def __init__(self, playerNumber: int = 1) -> None:
        self.playerNumber = playerNumber
        self.PlayersneedUpdate = 2**playerNumber - 1
    
    def initSockets(self) -> list:
        self.sock = socket.socket()
        self.connections = []
        self.recvthreads: list[threading.Thread] = []
        self.recvthreads_results: list[bytes] = [None] * self.playerNumber
        self.sendthreads: list[threading.Thread] = [] 
        hostname = socket.gethostname()
        IPaddr = socket.gethostbyname(hostname)
        if not self.validate_ip(IPaddr):
            print(f"IP address {IPaddr} is not valid.")
            IPaddr = input("Enter a valid IP address: ")
        
        try:
            self.sock.bind((IPaddr, 9090))
            self.sock.listen(self.playerNumber)
        except socket.error as e:
            print(f"Socket error: {e}")
            return []
        for i in range(self.playerNumber):
            conn, _ = self.sock.accept()
            self.connections.append(conn)
        for i in range(self.playerNumber):
            self.recvthreads.append(threading.Thread(target=self.recvData, args=[i]))
            self.recvthreads[i].start()
    
    def validate_ip(self, ip: str) -> bool:
        try:
            ipaddress.ip_address(ip)
            return True
        except ValueError:
            return False

    def initGame(self) -> None:
        self.game = Game("Game", self.playerNumber, Vector2d(30, 30))
        self.game.initTest()

    # Send data to player and wait untill getting verification that he recieved it
    def sendData(self, playerIndex: int) -> None:
        a = self.game.getPlayersData(playerIndex)
        self.connections[playerIndex].send(bytes(a))
        self.game.players[playerIndex].vision_updates = [[False for i in range(30)] for j in range(30)]

    # Wait untill getting data from player and then write it in recvthreads_results
    def recvData(self, playerIndex: int) -> None:
        data = self.connections[playerIndex].recv(1024)
        self.recvthreads_results[playerIndex] = data
        # programm stops waiting for recv()
        # that is why threading is used

    def playersControl(self):
        for i in range(self.playerNumber):
            if not self.recvthreads[i].is_alive():
                # TODO do something with self.recvthreads_results[i] in game
                # The thing here is just test version
                gotten = from_bytes(self.recvthreads_results[i])
                if gotten[0] != False:
                    for building in self.game.players[i].buildings:
                        if len(building.trainQueue) <= 1:
                            building.addToQueue(UnitTypes.ship)
                    for unit in self.game.players[i].units:
                        if len(unit.path) == 0:
                            unit.pathFinding(self.game.world, self.game.world.get((unit.pos + Vector2d(3, rd(-1, 1)))))
                
                if (self.PlayersneedUpdate // (2 ** i)) % 2:
                    self.sendData(i)
                else:
                    self.connections[i].send(to_bytes([False]))
                self.recvthreads[i] = threading.Thread(target=self.recvData, args=[i])
                self.recvthreads[i].start()
    
    def iteration(self) -> None:
        self.PlayersneedUpdate = self.game.iteration() 
        self.playersControl()
        time.sleep(0.05)
        
    def close(self):
        for conn in self.connections:
            conn.close()
        for thread in self.recvthreads:
            thread.join()
        self.sock.close()

a = Host(2)
a.initGame()
a.initSockets()
while True:
    a.iteration()



