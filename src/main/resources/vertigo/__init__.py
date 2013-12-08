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
import sys
import net.kuujo.vertigo.util.Context
import net.kuujo.vertigo.DefaultVertigoFactory
import net.kuujo.vertigo.component.DefaultComponentFactory
import org.vertx.java.platform.impl.JythonVerticleFactory
from context import NetworkContext, InstanceContext
from network import Network

this = sys.modules[__name__]

current_context = None
_context = net.kuujo.vertigo.util.Context.parseContext(org.vertx.java.platform.impl.JythonVerticleFactory.container.config())
if _context is not None:
    current_context = InstanceContext(_context)

def _setup_vertigo():
    vertx = org.vertx.java.platform.impl.JythonVerticleFactory.vertx
    container = org.vertx.java.platform.impl.JythonVerticleFactory.container
    factory = net.kuujo.vertigo.DefaultVertigoFactory(vertx, container)
    if current_context is not None:
        component_factory = net.kuujo.vertigo.component.DefaultComponentFactory(vertx, container)
        return factory.createVertigo(component_factory.createComponent(current_context._context))
    else:
        return factory.createVertigo()

_vertigo = _setup_vertigo()

def is_component():
    """
    Indicates whether the current verticle is a Vertigo component instance.

    @return: A boolean indicating whether the current Vert.x verticle is
    a Vertigo component instance.
    """
    return _vertigo.isComponent()

if _vertigo.isComponent():
    _component_type = net.kuujo.vertigo.util.Component.serializeType(_vertigo.context().getComponent().getType())
    if _component_type == 'feeder':
        from . import _feeder
        feeder = _feeder.Feeder(_vertigo.component()).start()
    elif _component_type == 'executor':
        from . import _executor
        executor = _executor.Executor(_vertigo.component()).start()
    elif _component_type == 'worker':
        from . import _worker
        worker = _worker.Worker(_vertigo.component()).start()
    else:
        raise ImportError("Unknown Vertigo component type %s" % (_component_type,))

logger = org.vertx.java.platform.impl.JythonVerticleFactory.container.logger()

def create_network(address):
    """
    Creates a new network.

    @param address: The network address.
    @return: A new network instance.
    """
    return Network(_vertigo.createNetwork(address))

def deploy_local_network(network, handler=None):
    """
    Deploys a local network.

    @param network: The network to deploy.
    @param handler: An optional asynchronous handler to be called once the deployment
    is complete.
    @return: The current vertigo instance.
    """
    if handler is not None:
        _vertigo.deployLocalNetwork(network._network, _DeployHandler(handler))
    else:
        _vertigo.deployLocalNetwork(network._network)
    return this

def shutdown_local_network(context, handler=None):
    """
    Shuts down a local network.

    @param context: The network context for the network to shutdown.
    @param handler: An optional asynchronous handler to be called once the shutdown
    is complete.
    @return: The current vertigo instance.
    """
    if handler is not None:
        _vertigo.shutdownLocalNetwork(context._context, _ShutdownHandler(handler))
    else:
        _vertigo.shutdownLocalNetwork(context._context)
    return this

def deploy_remote_network(address, network, handler=None):
    """
    Deploys a remote network.

    @param address: The event bus address to which to deploy modules and verticles.
    @param network: The network to deploy.
    @param handler: An optional asynchronous handler to be called once the deployment
    is complete.
    @return: The current vertigo instance.
    """
    if handler is not None:
        _vertigo.deployRemoteNetwork(address, network._network, _DeployHandler(handler))
    else:
        _vertigo.deployRemoteNetwork(address, network._network)
    return this

def shutdown_remote_network(address, context, handler=None):
    """
    Shuts down a remote network.

    @param address: The event bus address to which to deploy modules and verticles.
    @param context: The network context for the network to shutdown.
    @param handler: An optional asynchronous handler to be called once the shutdown
    is complete.
    @return: The current vertigo instance.
    """
    if handler is not None:
        _vertigo.shutdownRemoteNetwork(address, context._context, _ShutdownHandler(handler))
    else:
        _vertigo.shutdownRemoteNetwork(address, context._context)
    return this

class _DeployHandler(org.vertx.java.core.AsyncResultHandler):
    def __init__(self, handler):
        self._handler = handler
    def handle(self, result):
        if result.succeeded():
            self._handler(None, NetworkContext(result.result()))
        else:
            self._handler(result.cause(), None)

class _ShutdownHandler(org.vertx.java.core.AsyncResultHandler):
    def __init__(self, handler):
        self._handler = handler
    def handle(self, result):
        if result.succeeded():
            self._handler(None)
        else:
            self._handler(result.cause())
