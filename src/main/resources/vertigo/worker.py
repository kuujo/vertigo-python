# Copyright 2013 the original author or authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import org.vertx.java.core.Handler
import org.vertx.java.core.AsyncResultHandler
import org.vertx.java.core.json.JsonObject
from message import Message
from core.javautils import map_from_java, map_to_java

class BasicWorker(object):
  """A basic worker."""
  def __init__(self, worker):
    self._worker = worker

  def message_handler(self, handler):
    """Sets the worker message handler.

    Keyword arguments:
    @param handler: a handler to be called when a message is received.

    @return: the added handler.
    """
    self._worker.messageHandler(MessageHandler(handler, self))
    return handler

  def start(self, handler=None):
    """Starts the worker.

    Keyword arguments:
    @param handler: an optional handler to be called when the worker is started.

    @return: self
    """
    if handler is not None:
      self._worker.start(StartHandler(handler, self))
    else:
      self._worker.start()
    return self

  def emit(self, data, parent=None, tag=None):
    """Emits data to all output streams.

    Keyword arguments:
    @param data: the data to emit.
    @param parent: an optional message parent. If a parent message is provided
           then the emitted message will become a child of this parent.
    @param tag: a tag to apply to the output message.

    @return: the unique emitted message identifier.
    """
    if parent is not None:
      if tag is not None:
        return self._worker.emit(self._convert_data(data), tag, parent._message)
      else:
        return self._worker.emit(self._convert_data(data), parent._message)
    else:
      if tag is not None:
        return self._worker.emit(self._convert_data(data), tag)
      else:
        return self._worker.emit(self._convert_data(data))

  def ack(self, message):
    """Acknowledges a message.

    Keyword arguments:
    @param message: the message to ack.

    @return: self
    """
    self._worker.ack(message._message)
    return self

  def fail(self, message):
    """Fails a message.

    Keyword arguments:
    @param message: the message to fail.

    @return: self
    """
    self._worker.fail(message._message)
    return self

  def _convert_data(self, data):
    return org.vertx.java.core.json.JsonObject(map_to_java(data))

class StartHandler(org.vertx.java.core.AsyncResultHandler):
  """A worker start handler."""
  def __init__(self, handler, worker):
    self.handler = handler
    self.worker = worker

  def handle(self, result):
    if result.failed():
      self.handler(result.cause(), self.worker)
    else:
      self.handler(None, self.worker)

class MessageHandler(org.vertx.java.core.Handler):
  """A message handler wrapper."""
  def __init__(self, handler, worker):
    self.handler = handler
    self.worker = worker

  def handle(self, message):
    self.handler(Message(message), self.worker)
