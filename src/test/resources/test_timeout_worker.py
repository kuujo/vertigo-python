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
from test import Assert
from vertigo import worker
from vertigo.message import Message

@worker.message_handler
def message_handler(message):
    Assert.not_null(message)
    Assert.true(isinstance(message, Message))
    Assert.true(isinstance(message.id, basestring))
    Assert.true(isinstance(message.source, basestring))
    Assert.true(isinstance(message.body, dict))
    Assert.true(isinstance(message.has_parent(), bool))
    if message.has_parent():
        Assert.true(isinstance(message.parent, basestring))
    Assert.true(isinstance(message.has_root(), bool))
    Assert.true(isinstance(message.is_root(), bool))
    if message.has_root():
        Assert.true(isinstance(message.root, basestring))
    else:
        Assert.true(message.is_root())
    Assert.true(isinstance(message.stream, basestring))

    worker.emit(message.body, parent=message)
