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
import org.vertx.java.core.json.JsonObject
from core.javautils import map_from_java, map_to_java
from message import Message

class _AbstractExecutor(object):
  def __init__(self, executor):
    self._executor = executor

  def set_reply_timeout(self, timeout):
    """The executor result timeout."""
    self._executor.setReplyTimeout(timeout)

  def get_reply_timeout(self):
    """The executor result timeout."""
    return self._executor.getReplyTimeout()

  ack_timeout = property(get_reply_timeout, set_reply_timeout)

  def set_max_queue_size(self, queue_size):
    """The maximum number of messages that can be in the network at any given time."""
    self._executor.setMaxQueueSize(queue_size)

  def get_max_queue_size(self):
    """The maximum number of messages that can be in the network at any given time."""
    return self._executor.getMaxQueueSize()

  max_queue_size = property(get_max_queue_size, set_max_queue_size)

  def queue_full(self):
    """Indicates whether the executor queue is full."""
    return self._executor.queueFull()

  def start(self, handler=None):
    """Starts the executor.

    Keyword arguments:
    @param handler: a handler to be called with the executor once started

    @return: self
    """
    if handler is not None:
      self._executor.start(StartHandler(handler, self))
    else:
      self._executor.start()
    return self

  def _convert_data(self, data):
    return org.vertx.java.core.json.JsonObject(map_to_java(data))

class PollingExecutor(_AbstractExecutor):
  """A polling executor."""
  def set_execute_delay(self, delay):
    """The maximum delay between execution attempts."""
    self._executor.setExecuteDelay(delay)

  def get_execute_delay(self):
    """The maximum delay between execution attempts."""
    return self._executor.getExecuteDelay()

  execute_delay = property(get_execute_delay, set_execute_delay)

  def execute_handler(self, handler):
    """Registers a execute handler.

    Keyword arguments:
    @param handler: a handler to be called when the executor is prepared for the next message.

    @return: the added handler.
    """
    self._executor.executeHandler(ExecuteHandler(handler, self))
    return handler

  def result_handler(self, handler):
    """Registers an execution result handler.

    Keyword arguments:
    @param handler: a handler to be called when an execution result is received.

    @return: the added handler.
    """
    self._executor.resultHandler(ResultHandler(handler))
    return handler

  def fail_handler(self, handler):
    """Registers a fail handler.

    Keyword arguments:
    @param handler: a handler to be called when an execution failure is received.

    @return: the added handler.
    """
    self._executor.failHandler(FailHandler(handler))
    return handler

  def execute(self, data, tag=None):
    """Executes rpc on the network.

    Keyword arguments:
    @param data: the data to emit.
    @param tag: an optional tag to apply to the output data.

    @return: the unique output message identifier.
    """
    if tag is not None:
      return self._executor.execute(self._convert_data(data), tag)
    else:
      return self._executor.execute(self._convert_data(data))

class StreamExecutor(_AbstractExecutor):
  """
  A stream executor.
  """
  def drain_handler(self, handler):
    """
    Registers a drain handler.
    """
    self._executor.drainHandler(VoidHandler(handler))
    return handler

  def execute(self, data, tag=None, handler=None):
    """Executes rpc on the network.

    Keyword arguments:
    @param data: the data to emit.
    @param tag: an optional tag to apply to the output data.
    @param handler: an asynchronous result handler to be called with the result or failure

    @return: the unique output message identifier.
    """
    if handler is not None:
      if tag is not None:
        return self._executor.execute(self._convert_data(data), tag, ExecuteResultHandler(handler))
      else:
        return self._executor.execute(self._convert_data(data), ExecuteResultHandler(handler))
    else:
      if tag is not None:
        return self._executor.execute(self._convert_data(data), tag)
      else:
        return self._executor.execute(self._convert_data(data))

class StartHandler(org.vertx.java.core.AsyncResultHandler):
  """A start handler."""
  def __init__(self, handler, executor):
    self.handler = handler
    self.executor = executor

  def handle(self, result):
    if result.succeeded():
      self.handler(None, self.executor)
    else:
      self.handler(result.cause(), self.executor)

class ResultHandler(org.vertx.java.core.Handler):
  """A synchronous result handler."""
  def __init__(self, handler):
    self.handler = handler

  def handle(self, result):
    self.handler(Message(result))

class FailHandler(org.vertx.java.core.Handler):
  """A fail handler."""
  def __init__(self, handler):
    self.handler = handler

  def handle(self, messageid):
    self.handler(messageid)

class ExecuteResultHandler(org.vertx.java.core.AsyncResultHandler):
  """An execute result handler."""
  def __init__(self, handler):
    self.handler = handler

  def handle(self, result):
    if result.succeeded():
      self.handler(None, Message(result.result()))
    else:
      self.handler(result.cause(), None)

class ExecuteHandler(org.vertx.java.core.Handler):
  """An execute handler."""
  def __init__(self, handler, executor):
    self.handler = handler
    self.executor = executor

  def handle(self, executor):
    self.handler(self.executor)

class VoidHandler(org.vertx.java.core.Handler):
  """A void handler."""
  def __init__(self, handler):
    self.handler = handler

  def handle(self, void):
    self.handler()
