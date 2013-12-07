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
import net.kuujo.vertigo.function.Function
import net.kuujo.vertigo.function.Function2
from .message import Message
from core.javautils import map_from_java, map_to_java

class Aggregator(object):
    """A message aggregator."""
    def __init__(self, aggregator):
        self._aggregator = aggregator

    def init(self, func):
        """Registers an init function on the aggregator."""
        self._aggregator.initFunction(_InitFunction(func))
        return self

    def aggregate(self, func):
        """Registers an aggregator function on the aggregator."""
        self._aggregator.aggregateFunction(_AggregateFunction(func))
        return self

    def complete(self, func):
        """Registers a complete function on the aggregator."""
        self._aggregator.completeFunction(_CompleteFunction(func))
        return self

class _InitFunction(net.kuujo.vertigo.function.Function):
    """An init function handler."""
    def __init__(self, func):
        self._func = func

    def call(self, message):
        return self._func(Message(message))

class _AggregateFunction(net.kuujo.vertigo.function.Function2):
    """An aggregate function."""
    def __init__(self, func):
        self._func = func

    def call(self, current, message):
        return map_to_java(self._func(map_from_java(current), Message(message)))

class _CompleteFunction(net.kuujo.vertigo.function.Function):
    """A complete function handler."""
    def __init__(self, func):
        self._func = func

    def call(self, current):
        return self._func(map_from_java(current))
