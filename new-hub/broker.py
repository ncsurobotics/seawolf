import time
from http.server import BaseHTTPRequestHandler, HTTPServer
from queue import Queue

HOST_NAME = 'localhost'

queue = Queue()

class RequestHandler(BaseHTTPRequestHandler):
	def do_HEAD(self):
		self.send_response(200)
		self.send_header('Content-type', 'application/json')
		self.end_headers()

	def do_GET(self):
		if self.path == '/screenshot':
			self.respond({'status': 200})
		else:
			self.respond({'status': 500})
		
	def do_POST(self):
		if self.path == '/command':
			self.respond({'status': 200})
		else:
			self.respond({'status': 500})

	def handle_http(self, status_code, path):
		self.send_response(status_code)
		self.send_header('Content-type', 'application/json')
		self.end_headers()
		content = ""
		if self.path == '/command':
			content = "command"
		elif self.path == '/screenshot':
			content = 'sc'
		queue.put('noo')
		print(queue.get())
		return bytes(content, 'UTF-8')

	def respond(self, opts):
		response = self.handle_http(opts['status'], self.path)
		self.wfile.write(response)

if __name__ == '__main__':
	connected = False
	for port in range(8000, 15000):
		try:
			httpd = HTTPServer((HOST_NAME, port), RequestHandler)
		except OSError as e:
			pass
		else:
			connected = True
			break
	if not connected:
		print('Could not find unused port!')
		exit()
	print(time.asctime(), 'Server Starts - %s:%s' % (HOST_NAME, port))
	try:
		httpd.serve_forever()
	except KeyboardInterrupt:
		pass
	httpd.server_close()
	print(time.asctime(), 'Server Stops - %s:%s' % (HOST_NAME, port))
