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
import org.vertx.java.platform.impl.JythonVerticleFactory
import net.kuujo.vertigo.util.Factories.createComponent
from _cluster import Cluster
from _input import InputCollector
from _output import OutputCollector

cluster = None
logger = None
input = None
output = None
try:
    component = Component(createComponent(org.vertx.java.platform.impl.JythonVerticleFactory.vertx, org.vertx.java.platform.impl.JythonVerticleFactory.container))
except:
    raise ImportError("Not a valid component instance.")
else:
    cluster = Cluster(component.cluster())
    logger = component.logger()
    input = InputCollector(component.input())
    output = OutputCollector(component.output())
