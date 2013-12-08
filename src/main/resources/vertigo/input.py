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
import net.kuujo.vertigo.input.Input;
import net.kuujo.vertigo.input.DefaultListener
import org.vertx.java.platform.impl.JythonVerticleFactory

class Input(object):
    """A component input."""
    def __init__(self, javaobj):
        self._input = javaobj

    def group_by(self, grouping):
        """Sets a grouping on the input.

        Keyword arguments:
        @param grouping: an input grouping.

        @return: self
        """
        self._input.groupBy(grouping._grouping)
        return self

    def random_grouping(self):
        """Sets a random grouping on the input."""
        self._input.randomGrouping()
        return self

    def round_grouping(self):
        """Sets a round-robin grouping on the input."""
        self._input.roundGrouping()
        return self

    def fields_grouping(self, *fields):
        """Sets a fields grouping on the input."""
        self._input.fieldsGrouping(*fields)
        return self

    def all_grouping(self):
        """Sets an all grouping on the input."""
        self._input.allGrouping()
        return self

class Listener(object):
    """An input listener."""
    def __init__(self, address):
        self._listener = net.kuujo.vertigo.input.DefaultListener(address, org.vertx.java.platform.impl.JythonVerticleFactory.vertx)

    def get_auto_ack(self):
        """Indicates whether auto acking is enabled."""
        return self._listener.isAutoAck()

    def set_auto_ack(self, ack):
        """Sets auto acking."""
        self._listener.setAutoAck(ack)

    auto_ack = property(get_auto_ack, set_auto_ack)

    def message_handler(self, handler):
        """Registers a message handler on the listener."""
        self._listener.messageHandler(MessageHandler(handler, self))
        return handler

    def ack(self, message):
        """Acks a message.
    
        Keyword arguments:
        @param message: the message to ack.
    
        @return: self
        """
        self._listener.ack(message._message)
        return self

    def fail(self, message):
        """Fails a message.
    
        Keyword arguments:
        @param message: the message to fail.
    
        @return: self
        """
        self._listener.fail(message._message)
        return self

    def start(self, handler=None):
        """Starts the listener."""
        if handler is not None:
          self._listener.start(StartHandler(handler))
        else:
          self._listener.start()
        return self

    def stop(self, handler=None):
        """Stops the listener."""
        if handler is not None:
          self._listener.stop(StopHandler(handler))
        else:
          self._listener.stop()
        return self

class StartHandler(org.vertx.java.core.AsyncResultHandler):
    """A listener start handler."""
    def __init__(self, handler):
        self.handler = handler

    def handle(self, result):
        if result.failed():
          self.handler(result.cause())
        else:
          self.handler(None)

class StopHandler(org.vertx.java.core.AsyncResultHandler):
    """A listener stop handler."""
    def __init__(self, handler):
        self.handler = handler

    def handle(self, result):
        if result.failed():
          self.handler(result.cause())
        else:
          self.handler(None)

class MessageHandler(org.vertx.java.core.Handler):
    """A message handler wrapper."""
    def __init__(self, handler, listener):
        self.handler = handler
        self.listener = listener

    def handle(self, message):
        self.handler(Message(message), self.listener)
