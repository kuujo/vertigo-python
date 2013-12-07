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
from ._component import Component

class Executor(Component):
    """
    A network executor.
    """
    type = 'executor'
    RETRY_UNLIMITED = -1

    def __init__(self, executor):
        super(Executor, self).__init__(executor)
        self._executor = executor

    def set_execute_queue_max_size(self, queue_size):
        """The maximum number of messages processing at any given time."""
        self._executor.setExecuteQueueMaxSize(queue_size)
    
    def get_execute_queue_max_size(self):
        """The maximum number of messages processing at any given time."""
        return self._executor.getExecuteQueueMaxSize()
    
    execute_queue_max_size = property(get_execute_queue_max_size, set_execute_queue_max_size)
    
    def set_auto_retry(self, retry):
        """Indicates whether to automatically retry sending failed messages."""
        self._executor.setAutoRetry(retry)
    
    def is_auto_retry(self):
        """Indicates whether to automatically retry sending failed messages."""
        return self._executor.isAutoRetry()
    
    auto_retry = property(is_auto_retry, set_auto_retry)
    
    def set_auto_retry_attempts(self, attempts):
        """Indicates how many times to retry sending failed messages."""
        self._executor.setAutoRetryAttempts(attempts)
    
    def get_auto_retry_attempts(self):
        """Indicates how many times to retry sending failed messages."""
        return self._executor.getAutoRetryAttempts()
    
    auto_retry_attempts = property(get_auto_retry_attempts, set_auto_retry_attempts)

    def set_execute_interval(self, interval):
        """Indicates the interval at which to poll for new messages."""
        self._executor.setExecuteInterval(interval)
        return self

    def get_execute_interval(self):
        """Indicates the interval at which to poll for new messages."""
        return self._executor.getExecuteInterval()

    execute_interval = property(get_execute_interval, set_execute_interval)
    
    def execute_queue_full(self):
        """Indicates whether the executor queue is full."""
        return self._executor.feedQueueFull()

    def execute_handler(self, handler):
        """Sets a feed handler on the feeder.

        @param handler: A handler to be called with the executor as its only argument.
        @return: The executor instance.
        """
        self._executor.executeHandler(_ExecuteHandler(handler, self))
        return self

    def drain_handler(self, handler):
        """Sets a drain handler on the executor.

        @param handler: A handler to be called when the executor is prepared to
        accept new message.
        @return: The executor instance.
        """
        self._executor.drainHandler(_VoidHandler(handler))
        return self

    def _convert_data(self, data):
        return org.vertx.java.core.json.JsonObject(map_to_java(data))

    def execute(self, data, stream=None, handler=None):
        """Performs an execution.

        @param data: The dictionary data to emit.
        @param stream: An optional stream to which to emit the data. If no stream
        is provided then the default stream will be used.
        @param handler: An asynchronous result handler. The handler will be called
        with the execution result once the message has been fully processed. If
        multiple results are received for the execution then the handler will be
        called multiple times.

        @return: The feeder instance.
        """
        if stream is not None:
            if handler is not None:
                self._executor.execute(stream, self._convert_data(data), _ResultHandler(handler)).correlationId()
            else:
                self._executor.execute(stream, self._convert_data(data), _ResultHandler(None)).correlationId()
        else:
            if handler is not None:
                self._executor.execute(self._convert_data(data), _ResultHandler(handler)).correlationId()
            else:
                self._executor.execute(self._convert_data(data), _ResultHandler(None))

class _ExecuteHandler(org.vertx.java.core.Handler):
    """An execute handler."""
    def __init__(self, handler, executor):
        self._handler = handler
        self._executor = executor

    def handle(self, executor):
        self._handler(self.executor)

class _ResultHandler(org.vertx.java.core.AsyncResultHandler):
    """An asynchronous result handler."""
    def __init__(self, handler):
        self._handler = handler

    def handle(self, result):
        if self._handler is not None:
            if result.succeeded():
                self._handler(None, Message(result.result()))
            else:
                self._handler(result.cause(), None)

class _VoidHandler(org.vertx.java.core.Handler):
    """A void handler."""
    def __init__(self, handler):
        self.handler = handler

    def handle(self, void):
        self.handler()
