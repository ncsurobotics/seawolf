import uuid
import pika

# Remote Procedure Call
class RpcCaller:
  # From_queue is where RPC responses are sent
  def __init__(self, from_queue, rabbit):
    rabbit.create_queue(from_queue)
    self.from_queue = from_queue
    self.rabbit = rabbit
    self.rabbit.create_consumer(from_queue, self.on_response)

  def on_response(self, ch, method, props, body):
    if self.corr_id == props.correlation_id:
      self.response = body

  def call(self, to_queue, msg):
    self.response = None
    self.corr_id = str(uuid.uuid4())
    props = pika.BasicProperties(
      reply_to=self.from_queue,
      correlation_id=self.corr_id
      )
    self.rabbit.send(queue=to_queue, message=msg, prop=props)
    while self.response is None:
      self.rabbit.connection.process_data_events()
    return self.response