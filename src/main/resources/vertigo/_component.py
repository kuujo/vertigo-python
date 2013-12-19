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
import org.vertx.java.core.AsyncResultHandler
import net.kuujo.vertigo.message.schema.MessageSchema
from .context import InstanceContext
from core.javautils import map_from_java

from . import is_component
if not is_component():
    raise ImportError("Not a Vertigo component instance.")

class Component(object):
    """A base component."""
    type = None

    def __init__(self, component):
        self._component = component
        self._start_handler, self._start_result = None, None
        self.__start_handler = _StartHandler(self)

    @property
    def context(self):
        """The component context."""
        return InstanceContext(self._component.getContext())

    @property
    def config(self):
        """The component configuration."""
        return map_from_java(self._component.getContext().getComponent().getConfig().toMap())

    def declare_schema(self, fields):
        """Declares a schema for the component."""
        self._component.declareSchema(net.kuujo.vertigo.message.schema.MessageSchema(fields))

    schema = property(lambda: None, declare_schema)

    def start_handler(self, handler):
        """Sets a start handler on the component.

        @param handler: A handler to be called once the component is started.
        @return: The added start handler.
        """
        self._start_handler = handler
        self._check_start()
        return handler

    def _check_start(self):
        if self._start_result is not None and self._start_handler is not None:
            if self._start_result.succeeded():
                self._start_handler(None, self)
            else:
                self._start_handler(self._start_result.cause(), self)

    def start(self):
        """Starts the component."""
        self._component.start(self.__start_handler)
        return self

class _StartHandler(org.vertx.java.core.AsyncResultHandler):
    """A start handler."""
    def __init__(self, component):
        self._component = component

    def handle(self, result):
        self._component._start_result = result
        self._component._check_start()
