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
import sys
import org.vertx.java.platform.impl.JythonVerticleFactory
import net.kuujo.vertigo.util.Factories.createComponent

__this = sys.modules[__name__]

_component = None

try:
    _component = net.kuujo.vertigo.util.Factories.createComponent(org.vertx.java.platform.impl.JythonVerticleFactory.vertx, org.vertx.java.platform.impl.JythonVerticleFactory.container)
except:
    raise ImportError("Not a valid component instance.")

__start_handler = None
__started = None
def __check_start():
    if __start_handler is not None and __started is not None:
        if __started.failed():
            __start_handler(__started.cause(), None)
        else:
            __start_handler(None, __this)

def start_handler(handler):
    global __start_handler
    __start_handler = handler
    __check_start()

class StartHandler(org.vertx.java.core.AsyncResultHandler):
    def handle(self, result):
        global __started
        __started = result
        __check_start()

_component.start(StartHandler())
