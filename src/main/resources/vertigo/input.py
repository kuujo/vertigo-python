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
from core.buffer import Buffer
import org.vertx.java.core.json.JsonObject
import org.vertx.java.core.json.JsonArray
import org.vertx.java.core.buffer.Buffer
from java.util import (
    Map,
    Set,
    Collection
)
from core.javautils import map_map_from_java, map_set_from_java, map_collection_from_java

if component._component is None:
    raise ImportError("Not a valid Vertigo component.")

this = sys.modules[__name__]

_ports = {}

def port(name):
    """Returns an input port by name.

    Keyword arguments:
    @param name: The name of the port to load.

    @returns: An input port.
    """
    if name not in _ports:
        _ports[name] = InputPort(component._component.input().port(name))
    return _ports[name]

get_port = port

def message_handler(port, handler=None):
    """Registers a message handler for a port.

    Keyword arguments:
    @param port: The port for which to register the handler.
    @param handler: The handler to register.
    """
    if handler is not None:
        get_port(port).message_handler(handler)
        return this
    else:
        def wrap(f):
            get_port(port).message_handler(f)
            return f
        return wrap

def batch_handler(port, handler=None):
    """Registers a batch handler for a port.

    Keyword arguments:
    @param port: The port for which to register the handler.
    @param handler: The handler to register.
    """
    if handler is not None:
        get_port(port).batch_handler(handler)
        return this
    else:
        def wrap(f):
            get_port(port).batch_handler(f)
            return f
        return wrap

def group_handler(port, group, handler=None):
    """Registers a group handler for a port.

    Keyword arguments:
    @param port: The port for which to register the handler.
    @param group: The name of the group for which to register the handler.
    @param handler: The handler to register.
    """
    if handler is not None:
        get_port(port).group_handler(group, handler)
        return this
    else:
        def wrap(f):
            get_port(port).group_handler(group, f)
            return f
        return wrap

def pause(port):
    """Pauses a port.

    @param port: The port to pause.

    @return: The input module.
    """
    get_port(port).pause()
    return this

def resume(port):
    """Resumes a port.

    @param port: The port to resume.

    @return: The input module.
    """
    get_port(port).resume()
    return this

class Input(object):
    """Base input."""
    def __init__(self, java_obj):
        self.java_obj = java_obj

    def pause(self):
        """Pauses the input."""
        self.java_obj.pause()
        return self

    def resume(self):
        """Resumes the input."""
        self.java_obj.resume()
        return self

    def message_handler(self, handler):
        """Sets a message handler on the input.

        Keyword arguments:
        @param handler: A handler to be called when a message is received on the input.

        @return: self
        """
        self.java_obj.messageHandler(MessageHandler(handler))
        return self

    def group_handler(self, name, handler=None):
        """Sets a group handler on the input.

        Keyword arguments:
        @param name: The name of the group to handle.
        @param handler: A handler to be called when a group of the given name is received.

        @return: self
        """
        if handler is None:
            def wrap(handler):
                self.java_obj.groupHandler(name, GroupHandler(handler))
            return wrap
        else:
            self.java_obj.groupHandler(name, GroupHandler(handler))
            return self

class InputPort(Input):
    """Input port."""
    @property
    def name(self):
        """Returns the port name."""
        return self.java_obj.name()

    def batch_handler(self, handler=None):
        """Sets a batch handler on the port.

        Keyword arguments:
        @param handler: A handler to be called when a batch is received.

        @return: self
        """
        if handler is None:
            def wrap(handler):
                self.java_obj.batchHandler(name, BatchHandler(handler))
            return wrap
        else:
            self.java_obj.batchHandler(BatchHandler(handler))
            return self

class InputBatch(Input):
    """Input batch."""
    @property
    def id(self):
        """Returns the unique batch ID."""
        return self.java_obj.id()

    def start_handler(self, handler):
        """Sets a start handler on the batch.

        Keyword arguments:
        @param handler: A handler to be called when the batch is started.

        @return: self
        """
        self.java_obj.startHandler(VoidHandler(handler))
        return self

    def end_handler(self, handler):
        """Sets an end handler on the batch.

        Keyword arguments:
        @param handler: A handler to be called when the batch has ended.

        @return: self
        """
        self.java_obj.endHandler(VoidHandler(handler))
        return self

class InputGroup(Input):
    """Input group."""
    @property
    def id(self):
        """Returns the unique group ID."""
        return self.java_obj.id()

    @property
    def name(self):
        """Returns the group name."""
        return self.java_obj.name()

    def start_handler(self, handler):
        """Sets a start handler on the group.

        Keyword arguments:
        @param handler: A handler to be called when the group is started.

        @return: self
        """
        self.java_obj.startHandler(VoidHandler(handler))
        return self

    def end_handler(self, handler):
        """Sets an end handler on the group.

        Keyword arguments:
        @param handler: A handler to be called when the group has ended.

        @return: self
        """
        self.java_obj.endHandler(VoidHandler(handler))
        return self

class VoidHandler(org.vertx.java.core.Handler):
    def __init__(self, handler):
        self.handler = handler
    def handle(self, void=None):
        if self.handler is not None:
            self.handler()

class BatchHandler(org.vertx.java.core.Handler):
    def __init__(self, handler):
        self.handler = handler
    def handle(self, batch):
        self.handler(InputBatch(batch))

class GroupHandler(org.vertx.java.core.Handler):
    def __init__(self, handler):
        self.handler = handler;
    def handle(self, group):
        self.handler(InputGroup(group))

class MessageHandler(org.vertx.java.core.Handler):
    def __init__(self, handler):
        self.handler = handler;
    def handle(self, message):
        self.handler(map_from_vertx(message))

def map_array_from_java(array):
    """Converts a JsonArray to a list."""
    result = []
    iter = array.iterator()
    while iter.hasNext():
        result.append(map_from_vertx(iter.next()))
    return result

def map_object_from_java(obj):
    """Converts a JsonObject to a dictionary."""
    return map_map_from_java(obj.toMap())

def map_from_vertx(value):
    """Converts a Vert.x type to a Jython type."""
    if value is None:
        return value
    if isinstance(value, Map):
        return map_map_from_java(value)
    elif isinstance(value, Set):
        return map_set_from_java(value)
    elif isinstance(value, Collection):
        return map_collection_from_java(value)
    elif isinstance(value, org.vertx.java.core.json.JsonObject):
        return map_object_from_java(value)
    elif isinstance(value, org.vertx.java.core.json.JsonArray):
        return map_array_from_java(value)
    elif isinstance(value, org.vertx.java.core.buffer.Buffer):
        return Buffer(value)
    return value
