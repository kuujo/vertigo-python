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
import sys, component
import org.vertx.java.core.Handler
from java.lang import (
    Long,
    Double,
    Integer
)
from core.buffer import Buffer
import org.vertx.java.core.json.JsonObject
import org.vertx.java.core.json.JsonArray
from core.javautils import map_to_java, map_seq_to_java, map_dict_to_java

if component._component is None:
    raise ImportError("Not a valid Vertigo component.")

this = sys.modules[__name__]

_ports = {}

def port(name):
    """Loads an output port.

    Keyword arguments:
    @param name: The output port name.

    @return: An output port.
    """
    if name not in _ports:
        _ports[name] = OutputPort(component._component.output().port(name))
    return _ports[name]

get_port = port

def send(port, message):
    """Sends a message on an output port.

    Keyword arguments:
    @param port: The port on which to send the message.
    @param message: The message to send.
    """
    get_port(port).send(message)
    return this

def batch(port, handler=None):
    """Creates a batch for a specific port.

    Keyword arguments:
    @param port: The port for which to create the batch.
    @param handler: A handler to be called once the batch has been created.
    """
    if handler is not None:
        get_port(port).batch(handler)
        return this
    else:
        def wrap(f):
            get_port(port).batch(f)
            return f
        return wrap

def group(port, group, handler=None):
    """Creates a group for a specific port.

    Keyword arguments:
    @param port: The port for which to create the group.
    @param group: The name of the group to create.
    @param handler: A handler to be called once the group has been created.
    """
    if handler is not None:
        get_port(port).group(group, handler)
        return this
    else:
        def wrap(f):
            get_port(port).group(group, f)
            return f
        return wrap

def send_queue_full(port):
    """Checks if a send queue is full on a port.

    @param port: The port to check.

    @return: Indicates whether the queue is full.
    """
    return get_port(port).send_queue_full()

def drain_handler(port, handler=None):
    """Sets a drain handler on a port.

    Keyword arguments:
    @param port: The port on which to set the handler.
    @param handler: The handler to set.
    """
    if handler is not None:
        get_port(port).drain_handler(handler)
        return this
    else:
        def wrap(f):
            get_port(port).drain_handler(f)
            return f
        return wrap

class Output(object):
    """Base output."""
    def __init__(self, java_obj):
        self.java_obj = java_obj

    def set_send_queue_max_size(self, max_size):
        """Sets the maximum send queue size for the output."""
        self.java_obj.setSendQueueMaxSize(max_size)
        return self

    def get_send_queue_max_size(self, max_size):
        """Returns the maximum send queue size for the output."""
        return self.java_obj.getSendQueueMaxSize()

    send_queue_max_size = property(get_send_queue_max_size, set_send_queue_max_size)

    def send_queue_full(self):
        """Indicates whether the send queue is full."""
        return self.java_obj.sendQueueFull()

    def drain_handler(self, handler):
        """Sets a drain handler on the output."""
        self.java_obj.drainHandler(DrainHandler(handler))
        return self

    def group(self, name, handler=None):
        """Creates an output group.

        @param name: The name of the group to create.
        @param handler: A handler to be called once the group is created.

        @return: self
        """
        if handler is None:
            def wrap(f):
                self.java_obj.group(name, GroupHandler(f))
            return wrap
        else:
            self.java_obj.group(name, GroupHandler(handler))
        return self

    def send(self, message):
        """Sends a message.

        Keyword arguments:
        @param message: The message to send.

        @return: self
        """
        self.java_obj.send(map_to_vertx(message))
        return self

class OutputPort(Output):
    """Output port."""
    @property
    def name(self):
        """Returns the port name."""
        return self.java_obj.name()

    def batch(self, handler=None):
        """Creates an output batch.

        Keyword arguments:
        @param handler: A handler to be called once the batch is created.

        @return: self
        """
        if handler is None:
            def wrap(f):
                self.java_obj.batch(BatchHandler(f))
            return wrap
        else:
            self.java_obj.batch(BatchHandler(handler))
        return self

class OutputBatch(Output):
    """Output batch."""
    @property
    def id(self):
        """Returns the unique group identifier."""
        return self.java_obj.id()

    def end(self):
        """Ends the output group."""
        self.java_obj.end()

class OutputGroup(Output):
    """Output group."""
    @property
    def id(self):
        """Returns the unique group identifier."""
        return self.java_obj.id()

    @property
    def name(self):
        """Returns the group name."""
        return self.java_obj.name()

    def end(self):
        """Ends the output group."""
        self.java_obj.end()

class BatchHandler(org.vertx.java.core.Handler):
    def __init__(self, handler):
        self.handler = handler
    def handle(self, batch):
        self.handler(OutputBatch(batch))

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

def map_to_vertx(value):
    """Converts a Jython type to a Vert.x type."""
    if value is None:
        return value
    if isinstance(value, (list, tuple)):
        return org.vertx.java.core.json.JsonArray(map_seq_to_java(value))
    elif isinstance(value, dict):
        return org.vertx.java.core.json.JsonObject(map_dict_to_java(value))
    elif isinstance(value, Buffer):
        return value._to_java_buffer()
    elif isinstance(value, long):
        return Long(value)
    elif isinstance(value, float):
        return Double(value)
    elif isinstance(value, int):
        return Integer(value)
    return map_to_java(value)
