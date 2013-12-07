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
from .message import Message
from ._component import Component
from core.javautils import map_to_java

class Worker(Component):
    """A worker component."""
    type = 'worker'

    def __init__(self, worker):
        super(Worker, self).__init__(worker)
        self._worker = worker

    def message_handler(self, handler):
        """Sets the worker message handler.
    
        Keyword arguments:
        @param handler: a handler to be called when a message is received.
    
        @return: the added handler.
        """
        self._worker.messageHandler(_MessageHandler(handler))
        return handler
    
    def _convert_data(self, data):
        return org.vertx.java.core.json.JsonObject(map_to_java(data))

    def emit(self, data, stream=None, parent=None):
        """Emits data to all output streams.
    
        Keyword arguments:
        @param data: The data to emit.
        @param stream: The stream to which to emit the message. If no stream is
        provided then the default stream will be used.
        @param parent: An optional message parent. If a parent message is provided
               then the emitted message will become a child of this parent.
    
        @return: The unique emitted message identifier.
        """
        if parent is not None:
            if stream is not None:
                return self._worker.emit(stream, self._convert_data(data), parent._message)
            else:
                return self._worker.emit(self._convert_data(data), parent._message)
        else:
            if stream is not None:
                return self._worker.emit(stream, self._convert_data(data))
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

class _MessageHandler(org.vertx.java.core.Handler):
  """A message handler wrapper."""
  def __init__(self, handler):
    self._handler = handler

  def handle(self, message):
    self._handler(Message(message))
