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
from core.javautils import map_from_java

class Message(object):
    """A Vertigo message."""
    def __init__(self, message):
        self._message = message
        self._body = map_from_java(message.body().toMap())

    @property
    def id(self):
        """The unique message correlation identifier."""
        return self._message.messageId().correlationId()

    @property
    def source(self):
        """The message source address."""
        return self._message.source()

    def has_parent(self):
        """Indicates whether the message has a parent."""
        return self._message.messageId().hasParent()

    @property
    def parent(self):
        """The unique parent message identifier."""
        return self._message.messageId().parent()

    def has_root(self):
        """Indicates whether the message has a root."""
        return self._message.messageId().hasRoot()

    def is_root(self):
        """Indicates whether the message is a root message."""
        return self._message.messageId().isRoot()

    @property
    def root(self):
        """The unique root message identifier."""
        return self._message.messageId().root()

    @property
    def body(self):
        """The message body."""
        return self._body

    @property
    def stream(self):
        """The stream on which the message was emitted."""
        return self._message.stream()
