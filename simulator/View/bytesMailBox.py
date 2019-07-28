import pickle
import socket
import sys

#40000 characeer limit for msg, probably could be up to 60k
PACKET_SIZE = 10000
PACKET_OVERHEAD = 250

"""Mailbox provides common methods for
sending and receiving requests and data."""
class BytesMailBox(object):
    """The socket that requests and data will be sent through and received"""
    sock = []
    
    """Initialize the mailbox"""
    def __init__(self, ip_and_port=None, sock=None):
        if sock:
            self.sock = sock
        elif ip_and_port:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.sock.bind(ip_and_port)
            self.ip_and_port = ip_and_port
        else:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            ip = socket.gethostbyname(socket.gethostname())
            found_port = False
            for port in range(5000,15000):
                try:
                    self.ip_and_port = (ip,port)
                    self.sock.bind((ip,port))
                    found_port = True
                    break
                except:
                    pass
            if not found_port:
                raise Exception("Could not find client port.")
        """Dictionary of msg_address : partially assembled messages"""
        self.read_packets = dict()
        return

    """Send the msg to the to_addr location. Pickle the request if it is not pickled."""
    def send(self, msg, to_addr):
      s = ''
      i = 0
      str_data = msg
      end = len(str_data)
      sent_count = 1
      while(i < end):
        packet_end = min(i + PACKET_SIZE, end)
        #print i, packet_end
        msg_snippet = str_data[i:packet_end]
        if packet_end == end:
          sent_count = -sent_count
        #add on order stamp and sender address
        #print(msg_snippet, type(msg_snippet))
        msg_with_len = bytearray((str(sent_count) + ':').encode())
        #print("Len", msg_with_len)
        #print(type(msg_snippet))
        msg_with_len += msg_snippet
        #msg_snippet = str(sent_count).encode + ':' + msg_snippet
        sent_count += 1
        #print("Sending:\n", msg_with_len, type(msg_with_len))
        self.sock.sendto(msg_with_len, to_addr)
        #s += msg_snippet
        i += PACKET_SIZE
      
      return
    
    """Receive data and reassemble packets."""
    def receive(self):
      #keep reading until a msg has been fully read and assembled
      while True:
        data, addr = self.sock.recvfrom(PACKET_SIZE + PACKET_OVERHEAD)
        #print("Got data", data )
        colon_idx = -1
        # get the byte value of ':'
        delim = ':'.encode()[0]
        minus_byte = '-'.encode()[0]
        for i in range(len(data)):
          if data[i] == delim:
            colon_idx = i
            break
        if colon_idx == -1:
          #print "Bad packet"
          raise Exception("Bad data packet format.")
        packet_info = data[colon_idx + 1:len(data)]
        if addr in self.read_packets:
          #add packet info to dictionary
          self.read_packets[addr] += packet_info
        else:
          self.read_packets[addr] = packet_info
        if data[0] == minus_byte:
          msg = self.read_packets[addr]
          self.read_packets[addr] = b''
          return msg, addr

    """Getter for (ip,port)"""
    def getAddress(self):
      return self.ip_and_port

    def getPort(self):
      return self.ip_and_port[1]
    
    def getIp(self):
      return self.ip_and_port[0]









"""

print("main")

m = MailBox()

m.sendBytes(b'\x01\x02\x03', m.getAddress())

print("GOT:", m.receiveBytes())
"""