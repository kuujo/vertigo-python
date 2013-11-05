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
import net.kuujo.vertigo.feeder.DefaultBasicFeeder
import net.kuujo.vertigo.feeder.DefaultPollingFeeder
import net.kuujo.vertigo.feeder.DefaultStreamFeeder
import org.vertx.java.platform.impl.JythonVerticleFactory
import org.vertx.java.core.Handler
import org.vertx.java.core.json.JsonObject
from core.javautils import map_from_java, map_to_java

class _AbstractFeeder(object):
  """
  An abstract feeder.
  """
  _handlercls = None

  def __init__(self, context=None):
    if context is not None:
      context = context._context
    else:
      context = net.kuujo.vertigo.context.InstanceContext.fromJson(org.vertx.java.platform.impl.JythonVerticleFactory.container.config().getObject('__context__'))
      org.vertx.java.platform.impl.JythonVerticleFactory.container.config().removeField('__context__')
    self._feeder = self._handlercls(
      org.vertx.java.platform.impl.JythonVerticleFactory.vertx,
      org.vertx.java.platform.impl.JythonVerticleFactory.container,
      context
    )

  def set_ack_timeout(self, timeout):
    self._feeder.setAckTimeout(timeout)

  def get_ack_timeout(self):
    return self._feeder.getAckTimeout()

  ack_timeout = property(get_ack_timeout, set_ack_timeout)

  def set_max_queue_size(self, queue_size):
    self._feeder.setMaxQueueSize(queue_size)

  def get_max_queue_size(self):
    return self._feeder.getMaxQueueSize()

  max_queue_size = property(get_max_queue_size, set_max_queue_size)

  def set_auto_retry(self, retry):
    self._feeder.setAutoRetry(retry)

  def get_auto_retry(self):
    return self._feeder.getAutoRetry()

  auto_retry = property(get_auto_retry, set_auto_retry)

  def set_retry_attempts(self, attempts):
    self._feeder.setRetryAttempts(attempts)

  def get_retry_attempts(self):
    return self._feeder.getRetryAttempts()

  retry_attempts = property(get_retry_attempts, set_retry_attempts)

  def queue_full(self):
    """
    Indicates whether the feeder queue is full.
    """
    return self._feeder.queueFull()

  def start(self, handler=None):
    """
    Starts the feeder.
    """
    if handler is not None:
      self._feeder.start(StartHandler(handler, self))
    else:
      self._feeder.start()

  def feed(self, data, tag=None, handler=None):
    """
    Feeds data to the network.
    """
    if handler is not None:
      if tag is not None:
        self._feeder.feed(self._convert_data(data), tag, FeedResultHandler(handler))
      else:
        self._feeder.feed(self._convert_data(data), FeedResultHandler(handler))
    else:
      if tag is not None:
        self._feeder.feed(self._convert_data(data), tag)
      else:
        self._feeder.feed(self._convert_data(data))
    return self

  def _convert_data(self, data):
    return org.vertx.java.core.json.JsonObject(map_to_java(data))

class BasicFeeder(_AbstractFeeder):
  """
  A basic feeder.
  """
  _handlercls = net.kuujo.vertigo.feeder.DefaultBasicFeeder

class PollingFeeder(_AbstractFeeder):
  """
  A polling feeder.
  """
  _handlercls = net.kuujo.vertigo.feeder.DefaultPollingFeeder

  def set_feed_delay(self, delay):
    self._feeder.setFeedDelay(delay)

  def get_feed_delay(self):
    return self._feeder.getFeedDelay()

  feed_delay = property(get_feed_delay, set_feed_delay)

  def feed_handler(self, handler):
    """
    Registers a feed handler.
    """
    self._feeder.feedHandler(FeedHandler(handler, self))
    return handler

class StreamFeeder(_AbstractFeeder):
  """
  A stream feeder.
  """
  _handlercls = net.kuujo.vertigo.feeder.DefaultStreamFeeder

  def full_handler(self, handler):
    """
    Registers a full handler.
    """
    self._feeder.fullHandler(VoidHandler(handler))
    return handler

  def drain_handler(self, handler):
    """
    Registers a drain handler.
    """
    self._feeder.drainHandler(VoidHandler(handler))
    return handler

class StartHandler(org.vertx.java.core.AsyncResultHandler):
  """
  A start handler.
  """
  def __init__(self, handler, feeder):
    self.handler = handler
    self.feeder = feeder

  def handle(self, result):
    if result.succeeded():
      self.handler(None, self.feeder)
    else:
      self.handler(result.cause(), self.feeder)

class FeedResultHandler(org.vertx.java.core.AsyncResultHandler):
  """
  A feed result handler.
  """
  def __init__(self, handler):
    self.handler = handler

  def handle(self, result):
    if result.succeeded():
      self.handler(None)
    else:
      self.handler(result.cause())

class FeedHandler(org.vertx.java.core.Handler):
  """
  A feed handler.
  """
  def __init__(self, handler, feeder):
    self.handler = handler
    self.feeder = feeder

  def handle(self, feeder):
    self.handler(self.feeder)

class VoidHandler(org.vertx.java.core.Handler):
  """
  A void handler.
  """
  def __init__(self, handler):
    self.handler = handler

  def handle(self, void):
    self.handler()
