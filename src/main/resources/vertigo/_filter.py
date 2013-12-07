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
from .message import Message

class Filter(object):
    """A message filter."""
    def __init__(self, filter):
        self._filter = filter

    def __call__(self, func):
        self.filter(func)
        return func

    def filter(self, func):
        """Registers a filter function on the filter."""
        self._filter.filterFunction(_FilterFunction(func))

class _FilterFunction(net.kuujo.vertigo.function.Function):
    """A filter function handler."""
    def __init__(self, func):
        self._func = func

    def call(self, message):
        return self._func(Message(message))
