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
import component
import org.vertx.java.core.Handler
from core.javautils import map_from_java

if component._component is None:
    raise ImportError("Not a valid Vertigo component.")

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

def message_handler(port):
    """Registers a message handler for a port.

    Keyword arguments:
    @param port: The port for which to register the handler.
    """
    def wrap(f):
        get_port(port).message_handler(f)
        return f
    return wrap

def group_handler(port, group):
    """Registers a group handler for a port.

    Keyword arguments:
    @param port: The port for which to register the handler.
    @param group: The name of the group for which to register the handler.
    """
    def wrap(f):
        get_port(port).group_handler(group, f)
        return f
    return wrap

class Input(object):
    """Base input."""
    def __init__(self, java_obj):
        self.java_obj = java_obj

    @property
    def name(self):
        """Returns the input name."""
        return self.java_obj.name()

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

class InputGroup(Input):
    """Input group."""
    @property
    def id(self):
        """Returns the unique group ID."""
        return self.java_obj.id()

    def start_handler(self, handler):
        """Sets a start handler on the group.

        Keyword arguments:
        @param handler: A handler to be called when the group is started.

        @return: self
        """
        self.java_obj.startHandler(VoidHandler(handler))
        return self

    def end_handler(self, handler):
        """Sets an end handler on the gorup.

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

class GroupHandler(org.vertx.java.core.Handler):
    def __init__(self, handler):
        self.handler = handler;
    def handle(self, group):
        self.handler(InputGroup(group))

class MessageHandler(org.vertx.java.core.Handler):
    def __init__(self, handler):
        self.handler = handler;
    def handle(self, message):
        self.handler(map_from_java(message))
