# Copyright 2014 the original author or authors.
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
from core.java_utils import map_to_java

class OutputCollector(object):
    """Output collector."""
    def __init__(self, java_obj):
        self.java_obj = java_obj

    def __getattr__(self, name):
        if self.__dict__.has_key(name):
            return self.__dict__.get(name)
        return OutputPort(self.java_obj.port(name))

class Output(object):
    """Base output."""
    def __init__(self, java_obj):
        self.java_obj = java_obj

    def set_send_queue_max_size(self, max_size):
        self.java_obj.setSendQueueMaxSize(max_size)
        return self

    def get_send_queue_max_size(self, max_size):
        return self.java_obj.getSendQueueMaxSize()

    send_queue_max_size = property(get_send_queue_max_size, set_send_queue_max_size)

    def send_queue_full(self):
        return self.java_obj.sendQueueFull()

    def drain_handler(self, handler):
        self.java_obj.drainHandler(DrainHandler(handler))
        return self

    def group(self, name, handler):
        self.java_obj.group(name, GroupHandler(handler))
        return self

    def send(self, message):
        """Sends a message."""
        self.java_obj.send(map_to_java(message))
        return self

class OutputPort(object):
    """Output port."""

class OutputGroup(object):
    """Output group."""

class GroupHandler(org.vertx.java.core.Handler):
    def __init__(self, handler):
        self.handler = handler;
    def handle(self, group):
        self.handler(OutputGroup(group))

class DrainHandler(org.vertx.java.core.Handler):
    def __init__(self, handler):
        self.handler = handler;
    def handle(self, nothing):
        self.handler()
