import pika
import uuid
import time
import sys

sys.path.append('../simulator/View')
from renderCom import Messages, Message

class Rabbit:
  def __init__(self):
    self.url = 'localhost'
    self.connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    self.channel = self.connection.channel()

  def close(self):
    self.connection.close()
  
  def create_queue(self, name):
    return self.channel.queue_declare(queue=name)

  def create_consumer(self, name, callback):
    return self.channel.basic_consume(queue=name, auto_ack=True, on_message_callback=callback)
  
  def send(self, queue, message, prop=None):
    if prop != None:
      self.channel.basic_publish(exchange='', routing_key=queue, body=message, properties=prop)
    else:
      self.channel.basic_publish(exchange='', routing_key=queue, body=message)

  def start_consuming(self):
    self.channel.start_consuming()
  
  def reply(self, req_props, response):
    props = pika.BasicProperties(correlation_id = req_props.correlation_id)
    self.send(req_props.reply_to, response, prop=props)
  
  def get(self, queue_name):
    method_frame, header_frame, body = self.channel.basic_get(queue = queue_name)        
    if method_frame == None:
      return {'empty' : True}
    self.channel.basic_ack(delivery_tag=method_frame.delivery_tag)
    return {'method_frame' : method_frame, 'header_frame' : header_frame, 'body' : body, 'empty' : False}
