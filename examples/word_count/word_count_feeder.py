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
import vertx
from vertigo import component

@component.start_handler
def start_handler(error, component):
    if not error:
        words = vertx.config['words']

        def do_send():
            while not component.output.out.send_queue_full():
                component.output.out.send(words[rand(len(words) - 1)])

            @component.output.out.drain_handler
            def drain_handler():
                do_send()
