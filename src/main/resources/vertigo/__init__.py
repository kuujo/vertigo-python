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
import net.kuujo.vertigo.Vertigo
import org.vertx.java.platform.impl.JythonVerticleFactory
from core.javautils import map_to_java
from network import NetworkConfig, ActiveNetwork

this = sys.modules[__name__]

_vertigo = net.kuujo.vertigo.Vertigo(org.vertx.java.platform.impl.JythonVerticleFactory.vertx, org.vertx.java.platform.impl.JythonVerticleFactory.container)

def create_network(network):
    """Creates a new network.

    Keyword arguments:
    @param name: The network name or dictionary configuration.

    @return: A new network instance.
    """
    if isinstance(network, dict):
        return NetworkConfig(org.vertx.java.core.json.JsonObject(_vertigo.createNetwork(map_to_java(network))))
    return NetworkConfig(_vertigo.createNetwork(network))

def deploy_network(network, handler=None):
    """
    Deploys a network.

    Keyword arguments:
    @param network: The network name or configuration to deploy.
    @param handler: An optional asynchronous handler to be called once the deployment
    is complete.

    @return: The current vertigo instance.
    """
    if isinstance(network, dict):
        network = _vertigo.createNetwork(org.vertx.java.core.json.JsonObject(map_to_java(network)))
    if handler is not None:
        _vertigo.deployNetwork(network if isinstance(network, basestring) else network.java_obj, _DeployHandler(handler))
    else:
        _vertigo.deployNetwork(network if isinstance(network, basestring) else network.java_obj)
    return this

def undeploy_network(network, handler=None):
    """
    Undeploys a network.

    Keyword arguments:
    @param context: The network configuration or name for the network to undeploy.
    @param handler: An optional asynchronous handler to be called once the undeployment
    is complete.

    @return: The current vertigo instance.
    """
    if isinstance(network, dict):
        network = _vertigo.createNetwork(org.vertx.java.core.json.JsonObject(map_to_java(network)))
    if handler is not None:
        _vertigo.undeployNetwork(network if isinstance(network, basestring) else network.java_obj, _UndeployHandler(handler))
    else:
        _vertigo.undeployNetwork(network if isinstance(network, basestring) else network.java_obj)
    return this

class _DeployHandler(org.vertx.java.core.AsyncResultHandler):
    def __init__(self, handler):
        self._handler = handler
    def handle(self, result):
        if result.succeeded():
            self._handler(None, ActiveNetwork(result.result()))
        else:
            self._handler(result.cause(), None)

class _UndeployHandler(org.vertx.java.core.AsyncResultHandler):
    def __init__(self, handler):
        self._handler = handler
    def handle(self, result):
        if result.succeeded():
            self._handler(None)
        else:
            self._handler(result.cause())
