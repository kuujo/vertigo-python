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

class _AbstractFeeder(object):
  RETRY_UNLIMITED = -1

  def __init__(self, feeder):
    self._feeder = feeder

  def set_max_queue_size(self, queue_size):
    """The maximum number of messages processing at any given time."""
    self._feeder.setMaxQueueSize(queue_size)

  def get_max_queue_size(self):
    """The maximum number of messages processing at any given time."""
    return self._feeder.getMaxQueueSize()

  max_queue_size = property(get_max_queue_size, set_max_queue_size)

  def set_auto_retry(self, retry):
    """Indicates whether to automatically retry sending failed messages."""
    self._feeder.setAutoRetry(retry)

  def get_auto_retry(self):
    """Indicates whether to automatically retry sending failed messages."""
    return self._feeder.getAutoRetry()

  auto_retry = property(get_auto_retry, set_auto_retry)

  def set_retry_attempts(self, attempts):
    """Indicates how many times to retry sending failed messages."""
    self._feeder.setRetryAttempts(attempts)

  def get_retry_attempts(self):
    """Indicates how many times to retry sending failed messages."""
    return self._feeder.getRetryAttempts()

  retry_attempts = property(get_retry_attempts, set_retry_attempts)

  def queue_full(self):
    """Indicates whether the feeder queue is full."""
    return self._feeder.queueFull()

  def start(self, handler=None):
    """Starts the feeder.

    Keyword arguments:
    @param handler: an asynchronous start handler to be invoked once the feeder is started.

    @return self
    """
    if handler is not None:
      self._feeder.start(StartHandler(handler, self))
    else:
      self._feeder.start()
    return self

  def _convert_data(self, data):
    return org.vertx.java.core.json.JsonObject(map_to_java(data))

class BasicFeeder(_AbstractFeeder):
  """A basic feeder."""
  def emit(self, data, tag=None):
    """Emits data from the feeder.

    Keyword arguments:
    @param data: the data to emit.
    @param tag: a tag to apply to the emitted message.

    @return: the unique message identifier
    """
    if tag is not None:
      return self._feeder.emit(self._convert_data(data), tag)
    else:
      return self._feeder.emit(self._convert_data(data))

class PollingFeeder(BasicFeeder):
  """A polling feeder."""
  def set_feed_delay(self, delay):
    """The maximum interval to wait between attempting feeds."""
    self._feeder.setFeedDelay(delay)

  def get_feed_delay(self):
    """The maximum interval to wait between attempting feeds."""
    return self._feeder.getFeedDelay()

  feed_delay = property(get_feed_delay, set_feed_delay)

  def feed_handler(self, handler):
    """Registers a feed handler.

    Keyword arguments:
    @param handler: a handler to be invoked when the feeder is prepared for new messages

    @return: the added handler
    """
    self._feeder.feedHandler(FeedHandler(handler, self))
    return handler

  def ack_handler(self, handler):
    """Registers an ack handler on the feeder.

    Keyword arguments:
    @param handler: a handler to be called when a message is acked with the message id.

    @return: the added handler
    """
    self._feeder.ackHandler(AckFailTimeoutHandler(handler))
    return handler

  def fail_handler(self, handler):
    """Registers a fail handler on the feeder.

    Keyword arguments:
    @param handler: a handler to be called when a message is failed with the message id.

    @return: the added handler
    """
    self._feeder.failHandler(AckFailTimeoutHandler(handler))
    return handler

  def timeout_handler(self, handler):
    """Registers a timeout handler on the feeder.

    Keyword arguments:
    @param handler: a handler to be called when a message times out with the message id.

    @return: the added handler
    """
    self._feeder.timeoutHandler(AckFailTimeoutHandler(handler))
    return handler

class StreamFeeder(_AbstractFeeder):
  """A stream feeder."""
  def drain_handler(self, handler):
    """Registers a drain handler.

    Keyword arguments:
    @param handler: a handler to be called when the feeder is prepared for new messages.

    @return: the added handler.
    """
    self._feeder.drainHandler(VoidHandler(handler))
    return handler

  def emit(self, data, tag=None, handler=None):
    """Emits data from the feeder.

    Keyword arguments:
    @param data: the data to emit.
    @param tag: a tag to apply to the emitted message.
    @param handler: an asynchronous handler to be called once the message is acked.

    @return: the new message identifier.
    """
    if handler is not None:
      if tag is not None:
        return self._feeder.emit(self._convert_data(data), tag, FeedResultHandler(handler))
      else:
        return self._feeder.emit(self._convert_data(data), FeedResultHandler(handler))
    else:
      if tag is not None:
        return self._feeder.emit(self._convert_data(data), tag)
      else:
        return self._feeder.emit(self._convert_data(data))

class StartHandler(org.vertx.java.core.AsyncResultHandler):
  """A start handler."""
  def __init__(self, handler, feeder):
    self.handler = handler
    self.feeder = feeder

  def handle(self, result):
    if result.succeeded():
      self.handler(None, self.feeder)
    else:
      self.handler(result.cause(), self.feeder)

class AckFailTimeoutHandler(org.vertx.java.core.Handler):
  """An ack/fail/timeout handler."""
  def __init__(self, handler):
    self.handler = handler

  def handle(self, messageid):
    self.handler(messageid)

class FeedResultHandler(org.vertx.java.core.AsyncResultHandler):
  """A feed result handler."""
  def __init__(self, handler):
    self.handler = handler

  def handle(self, result):
    if result.succeeded():
      self.handler(None)
    else:
      self.handler(result.cause())

class FeedHandler(org.vertx.java.core.Handler):
  """A feed handler."""
  def __init__(self, handler, feeder):
    self.handler = handler
    self.feeder = feeder

  def handle(self, feeder):
    self.handler(self.feeder)

class VoidHandler(org.vertx.java.core.Handler):
  """A void handler."""
  def __init__(self, handler):
    self.handler = handler

  def handle(self, void):
    self.handler()
