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
from ._component import Component

class Feeder(Component):
    """A data feeder."""
    type = 'feeder'
    RETRY_UNLIMITED = -1
    _start_handler = None
    _ack_handler = None

    def __init__(self, feeder):
        super(Feeder, self).__init__(feeder)
        self._feeder = feeder

    def set_feed_queue_max_size(self, queue_size):
        """The maximum number of messages processing at any given time."""
        self._feeder.setFeedQueueMaxSize(queue_size)
    
    def get_feed_queue_max_size(self):
        """The maximum number of messages processing at any given time."""
        return self._feeder.getFeedQueueMaxSize()
    
    max_queue_size = property(get_feed_queue_max_size, set_feed_queue_max_size)
    
    def set_auto_retry(self, retry):
        """Indicates whether to automatically retry sending failed messages."""
        self._feeder.setAutoRetry(retry)
    
    def is_auto_retry(self):
        """Indicates whether to automatically retry sending failed messages."""
        return self._feeder.isAutoRetry()
    
    auto_retry = property(is_auto_retry, set_auto_retry)
    
    def set_auto_retry_attempts(self, attempts):
        """Indicates how many times to retry sending failed messages."""
        self._feeder.setAutoRetryAttempts(attempts)
    
    def get_auto_retry_attempts(self):
        """Indicates how many times to retry sending failed messages."""
        return self._feeder.getAutoRetryAttempts()
    
    auto_retry_attempts = property(get_auto_retry_attempts, set_auto_retry_attempts)

    def set_feed_interval(self, interval):
        """Indicates the interval at which to poll for new messages."""
        self._executor.setFeedInterval(interval)
        return self

    def get_feed_interval(self):
        """Indicates the interval at which to poll for new messages."""
        return self._executor.getFeedInterval()

    feed_interval = property(get_feed_interval, set_feed_interval)
    
    def feed_queue_full(self):
        """Indicates whether the feeder queue is full."""
        return self._feeder.feedQueueFull()

    def ack_handler(self, handler):
        """Sets a default ack handler on the feeder.

        @param handler: A default ack handler to be used when no other ack handler
        is present.
        @return: The added handler
        """
        self._ack_handler = handler
        return handler

    def feed_handler(self, handler):
        """Sets a feed handler on the feeder.

        @param handler: A handler to be called with the feeder as its only argument.
        @return: The feeder instance.
        """
        self._feeder.feedHandler(_FeedHandler(handler, self))
        return self

    def drain_handler(self, handler):
        """Sets a drain handler on the feeder.

        @param handler: A handler to be called when the feeder is prepared to
        accept new message.
        @return: self
        """
        self._feeder.drainHandler(_VoidHandler(handler))
        return self

    def _convert_data(self, data):
        return org.vertx.java.core.json.JsonObject(map_to_java(data))

    def emit(self, data, stream=None, handler=None):
        """Emits a message from the feeder.

        @param data: A dictionary of data to emit.
        @param stream: An optional stream to which to emit the data. If no stream
        is provided then the data will be emitted to the default stream.
        @param handler: An optional asynchronous handler to be called once the
        message has been fully processed. Feeders implement a special type of
        ack handler. Whether the message is successfully processed or fails,
        the second argument to the ack handler will always be the unique message
        correlation identifier.

        @return: The unique emitted message correlation identifier.
        """
        if handler is None and self._ack_handler is not None:
            handler = self._ack_handler
        if stream is not None:
            if handler is not None:
                return self._feeder.emit(stream, self._convert_data(data), _AckHandler(handler)).correlationId()
            else:
                return self._feeder.emit(stream, self._convert_data(data)).correlationId()
        else:
            if handler is not None:
                return self._feeder.emit(self._convert_data(data), _AckHandler(handler)).correlationId()
            else:
                return self._feeder.emit(self._convert_data(data)).correlationId()

class _FeedHandler(org.vertx.java.core.Handler):
    """A feed handler."""
    def __init__(self, handler, feeder):
        self._handler = handler
        self._feeder = feeder

    def handle(self, feeder):
        self._handler(self.feeder)

class _AckHandler(org.vertx.java.core.AsyncResultHandler):
    """An ack handler."""
    def __init__(self, handler):
        self._handler = handler

    def handle(self, result):
        self._handler(result.cause(), result.result().correlationId())

class _VoidHandler(org.vertx.java.core.Handler):
    """A void handler."""
    def __init__(self, handler):
        self.handler = handler

    def handle(self, void):
        self.handler()
