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
from test import Assert, Test
from vertigo import feeder

@feeder.start_handler
def start_handler(error, feeder):
    if error is None:
        feeder.emit({'body': 'Hello world!'})

@feeder.ack_handler
def ack_handler(error, id):
    Assert.null(error)
    Test.complete()
