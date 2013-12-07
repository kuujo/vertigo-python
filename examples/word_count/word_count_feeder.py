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
from vertigo import feeder
from vertigo.error import FailureError

@feeder.start_handler
def start_handler(error, feeder):
    if not error:
        feeder.auto_retry = True
        feeder.auto_retry_attempts = feeder.RETRY_UNLIMITED

        words = feeder.config['words']

        def ack_handler(error, id):
            if isinstance(error, FailureError):
                print error.getMessage()

        @feeder.feed_handler
        def feed_handler(feeder):
            word = words[rand(len(words)-1)]
            feeder.emit({'word': word}, handler=ack_handler)
