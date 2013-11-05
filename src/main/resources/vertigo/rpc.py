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
import net.kuujo.vertigo.context.InstanceContext
import net.kuujo.vertigo.rpc.DefaultBasicExecutor
import net.kuujo.vertigo.rpc.DefaultPollingExecutor
import net.kuujo.vertigo.rpc.DefaultStreamExecutor
import org.vertx.java.platform.impl.JythonVerticleFactory
import org.vertx.java.core.Handler
import org.vertx.java.core.json.JsonObject
from core.javautils import map_from_java, map_to_java

class _AbstractExecutor(object):
  """
  An abstract executor.
  """
  _handlercls = None

  def __init__(self, context=None):
    if context is not None:
      context = context._context
    else:
      context = net.kuujo.vertigo.context.InstanceContext.fromJson(org.vertx.java.platform.impl.JythonVerticleFactory.container.config().getObject('__context__'))
      org.vertx.java.platform.impl.JythonVerticleFactory.container.config().removeField('__context__')
    self._executor = self._handlercls(
      org.vertx.java.platform.impl.JythonVerticleFactory.vertx,
      org.vertx.java.platform.impl.JythonVerticleFactory.container,
      context
    )

  def set_ack_timeout(self, timeout):
    self._executor.setAckTimeout(timeout)

  def get_ack_timeout(self):
    return self._executor.getAckTimeout()

  ack_timeout = property(get_ack_timeout, set_ack_timeout)

  def set_max_queue_size(self, queue_size):
    self._executor.setMaxQueueSize(queue_size)

  def get_max_queue_size(self):
    return self._executor.getMaxQueueSize()

  max_queue_size = property(get_max_queue_size, set_max_queue_size)

  def set_auto_retry(self, retry):
    self._executor.setAutoRetry(retry)

  def get_auto_retry(self):
    return self._executor.getAutoRetry()

  auto_retry = property(get_auto_retry, set_auto_retry)

  def set_retry_attempts(self, attempts):
    self._executor.setRetryAttempts(attempts)

  def get_retry_attempts(self):
    return self._executor.getRetryAttempts()

  retry_attempts = property(get_retry_attempts, set_retry_attempts)

  def queue_full(self):
    """
    Indicates whether the executor queue is full.
    """
    return self._executor.queueFull()

  def start(self, handler=None):
    """
    Starts the executor.
    """
    if handler is not None:
      self._executor.start(StartHandler(handler, self))
    else:
      self._executor.start()

  def execute(self, data, tag=None, handler=None):
    """
    Executes rpc on the network.
    """
    if handler is not None:
      if tag is not None:
        self._executor.execute(self._convert_data(data), tag, ExecuteResultHandler(handler))
      else:
        self._executor.execute(self._convert_data(data), ExecuteResultHandler(handler))
    else:
      if tag is not None:
        self._executor.execute(self._convert_data(data), tag)
      else:
        self._executor.execute(self._convert_data(data))
    return self

  def _convert_data(self, data):
    return org.vertx.java.core.json.JsonObject(map_to_java(data))

class BasicExecutor(_AbstractExecutor):
  """
  A basic executor.
  """
  _handlercls = net.kuujo.vertigo.rpc.DefaultBasicExecutor

class PollingExecutor(_AbstractExecutor):
  """
  A polling executor.
  """
  _handlercls = net.kuujo.vertigo.rpc.DefaultPollingExecutor

  def set_execute_delay(self, delay):
    self._executor.setExecuteDelay(delay)

  def get_execute_delay(self):
    return self._executor.getExecuteDelay()

  execute_delay = property(get_execute_delay, set_execute_delay)

  def execute_handler(self, handler):
    """
    Registers a execute handler.
    """
    self._executor.executeHandler(ExecuteHandler(handler, self))
    return handler

class StreamExecutor(_AbstractExecutor):
  """
  A stream executor.
  """
  _handlercls = net.kuujo.vertigo.rpc.DefaultStreamExecutor

  def full_handler(self, handler):
    """
    Registers a full handler.
    """
    self._executor.fullHandler(VoidHandler(handler))
    return handler

  def drain_handler(self, handler):
    """
    Registers a drain handler.
    """
    self._executor.drainHandler(VoidHandler(handler))
    return handler

class StartHandler(org.vertx.java.core.AsyncResultHandler):
  """
  A start handler.
  """
  def __init__(self, handler, executor):
    self.handler = handler
    self.executor = executor

  def handle(self, result):
    if result.succeeded():
      self.handler(None, self.executor)
    else:
      self.handler(result.cause(), self.executor)

class ExecuteResultHandler(org.vertx.java.core.AsyncResultHandler):
  """
  An execute result handler.
  """
  def __init__(self, handler):
    self.handler = handler

  def handle(self, result):
    if result.succeeded():
      self.handler(None, result.result())
    else:
      self.handler(result.cause(), None)

class ExecuteHandler(org.vertx.java.core.Handler):
  """
  An execute handler.
  """
  def __init__(self, handler, executor):
    self.handler = handler
    self.executor = executor

  def handle(self, executor):
    self.handler(self.executor)

class VoidHandler(org.vertx.java.core.Handler):
  """
  A void handler.
  """
  def __init__(self, handler):
    self.handler = handler

  def handle(self, void):
    self.handler()
