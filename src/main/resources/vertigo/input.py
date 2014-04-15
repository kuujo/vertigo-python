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
from core.javautils import map_from_java

class InputCollector(object):
    """Input collector."""
    def __init__(self, java_obj):
        self.java_obj = java_obj
        self._ports = {}

    def port(self, name):
        """Returns an input port by name.

        Keyword arguments:
        @param name: The name of the port to get.

        @return: An input port.
        """
        if name not in self._ports:
            self._ports[name] = InputPort(self.java_obj.port(name))
        return self._ports[name]

    def __getattr__(self, name):
        if self.__dict__.has_key(name):
            return self.__dict__.get(name)
        return InputPort(self.java_obj.port(name))

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

class InputGroup(Input):
    """Input group."""

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
