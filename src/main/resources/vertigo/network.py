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
import org.vertx.java.core.AsyncResultHandler
from core.javautils import map_from_java, map_to_java
import net.kuujo.vertigo.network.ModuleConfig
import net.kuujo.vertigo.network.VerticleConfig
import net.kuujo.vertigo.cluster.ClusterScope
import net.kuujo.vertigo.io.selector.RoundRobinSelector
import net.kuujo.vertigo.io.selector.RandomSelector
import net.kuujo.vertigo.io.selector.HashSelector
import net.kuujo.vertigo.io.selector.FairSelector
import net.kuujo.vertigo.io.selector.AllSelector

class Config(object):
    """Base configuration."""
    def __init__(self, java_obj):
        self.java_obj = java_obj

class NetworkConfig(Config):
    """Network configuration."""
    SCOPE_LOCAL = "local"
    SCOPE_CLUSTER = "cluster"

    _SELECTORS = {
      'round-robin': net.kuujo.vertigo.io.selector.RoundRobinSelector,
      'random': net.kuujo.vertigo.io.selector.RandomSelector,
      'hash': net.kuujo.vertigo.io.selector.HashSelector,
      'fair': net.kuujo.vertigo.io.selector.FairSelector,
      'all': net.kuujo.vertigo.io.selector.AllSelector,
    }

    @property
    def name(self):
        """Returns the network name."""
        return self.java_obj.getName()

    def get_scope(self):
        """Returns the network scope."""
        return self.java_obj.getScope().toString()

    def set_scope(self, scope):
        """Sets the network scope."""
        self.java_obj.setScope(net.kuujo.vertigo.cluster.ClusterScope.parse(scope))
        return self

    scope = property(get_scope, set_scope)

    def add_component(self, name, main, config=None, instances=1):
        """Adds a component to the network.

        Keyword arguments:
        @param name: The name of the component to add.
        @param main: The component verticle main or module name.
        @param config: The component verticle or module configuration.
        @param instances: The number of component instances to add.

        @return: The component configuration.
        """
        component = self.java_obj.addComponent(name, main, config, instances)
        if isinstance(component, net.kuujo.vertigo.network.ModuleConfig):
            return ModuleConfig(component);
        else:
            return VerticleConfig(component)

    def remove_component(self, name):
        """Removes a component from the network.

        Keyword arguments:
        @param name: The name of the component to remove.

        @return: self
        """
        self.java_obj.removeComponent(name)
        return self

    def add_verticle(self, name, main, config=None, instances=1):
        """Adds a verticle component to the network.

        Keyword arguments:
        @param name: The verticle component name.
        @param main: The verticle main.
        @param config: The verticle configuration.
        @param instances: The number of instances to add.

        @return: The verticle configuration.
        """
        return VerticleConfig(self.java_obj.addVerticle(name, main, config, instances))

    def remove_verticle(self, name):
        """Removes a verticle from the network.

        Keyword arguments:
        @param name: The name of the verticle to remove.

        @return: self
        """
        self.java_obj.removeComponent(name)
        return self

    def add_module(self, name, module, config=None, instances=1):
        """Adds a module component to the network.

        Keyword arguments:
        @param name: The module component name.
        @param module: The module name.
        @param config: The module configuration.
        @param instances: The number of instances to add.

        @return: The module configuration.
        """
        return ModuleConfig(self.java_obj.addModule(name, module, config, instances))

    def remove_module(self, name):
        """Removes a module from the network.

        Keyword arguments:
        @param name: The name of the module to remove.

        @return: self
        """
        self.java_obj.removeComponent(name)
        return self

    def create_connection(self, source, target, selector=None):
        """Creates a connection between two components.

        Keyword arguments:
        @param source: A two-tuple indicating the source component name and output port.
        @param target: A two-tuple indicating the target component name and input port.
        @param selector: A connection selector type.

        @return: The connection configuration.
        """
        if selector is not None:
            return ConnectionConfig(self.java_obj.createConnection(source[0], source[1], target[0], target[1], self._SELECTORS[selector]))
        else:
            return ConnectionConfig(self.java_obj.createConnection(source[0], source[1], target[0], target[1]))

    def destroy_connection(self, source, target):
        """Destroys a connection between two components.

        Keyword arguments:
        @param source: A two-tuple indicating the source component name and output port.
        @param target: A two-tuple indicating the target component name and input port.

        @return: self
        """
        self.java_obj.destroyConnection(source[0] if isinstance(source, tuple) else source, target[0] if isinstance(target, tuple) else target)
        return self

class ComponentConfig(Config):
    """Component configuration."""
    MODULE = "module"
    VERTICLE = "verticle"

    @property
    def type(self):
        """Returns the component type."""
        return self.java_obj.getType().toString()

    @property
    def name(self):
        """Returns the unique component name."""
        return self.java_obj.getName()

    def get_config(self):
        """Returns the component configuration."""
        return map_from_java(self.java_obj.getConfig())

    def set_config(self, config):
        """Sets the component configuration."""
        self.java_obj.setConfig(map_to_java(config))
        return self

    config = property(get_config, set_config)

    def get_instances(self):
        """Returns the number of component instances."""
        return self.java_obj.getInstances()

    def set_instances(self, instances):
        """Sets the number of component instances."""
        self.java_obj.setInstances(instances)
        return self

    instances = property(get_instances, set_instances)

    def get_group(self):
        """Returns the component deployment group."""
        return self.java_obj.getGroup()

    def set_group(self, group):
        """Sets the component deployment group."""
        self.java_obj.setGroup(group)
        return self

    group = property(get_group, set_group)

class ModuleConfig(ComponentConfig):
    """Module component configuration."""
    def get_module(self):
        """Returns the module name."""
        return self.java_obj.getModule()

    def set_module(self, module):
        """Sets the module name."""
        self.java_obj.setModule(module)
        return self

    module = property(get_module, set_module)

class VerticleConfig(ComponentConfig):
    """Verticle component configuration."""
    def get_main(self):
        """Returns the verticle main."""
        return self.java_obj.getMain()

    def set_main(self, main):
        """Sets the verticle main."""
        self.java_obj.setMain(main)
        return self

    main = property(get_main, set_main)

    def is_worker(self):
        """Returns whether the verticle should be deployed as a worker."""
        return self.java_obj.isWorker()

    def set_worker(self, worker):
        """Sets whether the verticle should be deployed as a worker."""
        self.java_obj.setWorker(worker)
        return self

    worker = property(is_worker, set_worker)

    def is_multi_threaded(self):
        """Returns whether a worker verticle should be deployed as multi-threaded."""
        return self.java_obj.isMultiThreaded()

    def set_multi_threaded(self, multi_threaded):
        """Sets whether a worker verticle should be deployed as multi-threaded."""
        self.java_obj.setMultiThreaded(multi_threaded)
        return self

    multi_threaded = property(is_multi_threaded, set_multi_threaded)

class ConnectionConfig(Config):
    """Connection configuration."""
    @property
    def source(self):
        """Returns the connection source."""
        return Endpoint(self.java_obj.getSource())

    @property
    def target(self):
        """Returns the connection target."""
        return Endpoint(self.java_obj.getTarget())

    def random_select(self):
        """Sets a random selector on the connection."""
        self.java_obj.randomSelect()
        return self

    def round_select(self):
        """Sets a round selector on the connection."""
        self.java_obj.roundSelect()
        return self

    def hash_select(self):
        """Sets a hash selector on the connection."""
        self.java_obj.hashSelect()
        return self

    def fair_select(self):
        """Sets a fair selector on the connection."""
        self.java_obj.fairSelect()
        return self

    def all_select(self):
        """Sets an all selector on the connection."""
        self.java_obj.allSelect()
        return self

    class Endpoint(Config):
        """Connection connection endpoint information."""
        def get_component(self):
            """Returns the endpoint component."""
            return self.java_obj.getComponent()

        def set_component(self, component):
            """Sets the connection endpoint component."""
            self.java_obj.setComponent(component)
            return self

        component = property(get_component, set_component)

        def get_port(self):
            """Returns the connection endpoint port."""
            return self.java_obj.getPort()

        def set_port(self, port):
            """Sets the connection endpoint port."""
            self.java_obj.setPort(port)
            return self

        port = property(get_port, set_port)

class ActiveNetwork(Config):
    """Active network configuration."""
    def add_component(self, name, main, config=None, instances=1, handler=None):
        """Adds a component to the network.

        Keyword arguments:
        @param name: The name of the component to add.
        @param main: The component verticle main or module name.
        @param config: The component verticle or module configuration.
        @param instances: The number of component instances to add.
        @param handler: An asynchronous handler to be called once the network has been updated.

        @return: The component configuration.
        """
        component = self.java_obj.addComponent(name, main, config, instances, ActiveNetworkHandler(handler) if handler is not None else None)
        if isinstance(component, net.kuujo.vertigo.network.ModuleConfig):
            return ModuleConfig(component);
        else:
            return VerticleConfig(component)

    def remove_component(self, name, handler=None):
        """Removes a component from the network.

        Keyword arguments:
        @param name: The name of the component to remove.
        @param handler: An asynchronous handler to be called once the network has been updated.

        @return: self
        """
        self.java_obj.removeComponent(name, ActiveNetworkHandler(handler) if handler is not None else None)
        return self

    def add_verticle(self, name, main, config=None, instances=1, handler=None):
        """Adds a verticle component to the network.

        Keyword arguments:
        @param name: The verticle component name.
        @param main: The verticle main.
        @param config: The verticle configuration.
        @param instances: The number of instances to add.
        @param handler: An asynchronous handler to be called once the network has been updated.

        @return: The verticle configuration.
        """
        return VerticleConfig(self.java_obj.addVerticle(name, main, config, instances, ActiveNetworkHandler(handler) if handler is not None else None))

    def remove_verticle(self, name, handler=None):
        """Removes a verticle component from the network.

        Keyword arguments:
        @param name: The name of the verticle to remove.
        @param handler: An asynchronous handler to be called once the network has been updated.

        @return: self
        """
        self.java_obj.removeVerticle(name, ActiveNetworkHandler(handler) if handler is not None else None)
        return self

    def add_module(self, name, module, config=None, instances=1, handler=None):
        """Adds a module component to the network.

        Keyword arguments:
        @param name: The module component name.
        @param module: The module name.
        @param config: The module configuration.
        @param instances: The number of instances to add.
        @param handler: An asynchronous handler to be called once the network has been updated.

        @return: The module configuration.
        """
        return ModuleConfig(self.java_obj.addModule(name, module, config, instances, ActiveNetworkHandler(handler) if handler is not None else None))

    def remove_module(self, name, handler=None):
        """Removes a module component from the network.

        Keyword arguments:
        @param name: The name of the module to remove.
        @param handler: An asynchronous handler to be called once the network has been updated.

        @return: self
        """
        self.java_obj.removeModule(name, ActiveNetworkHandler(handler) if handler is not None else None)
        return self

    def create_connection(self, source, target, handler=None):
        """Creates a connection between two components.

        Keyword arguments:
        @param source: A two-tuple indicating the source component name and output port.
        @param target: A two-tuple indicating the target component name and input port.
        @param handler: An asynchronous handler to be called once the network has been updated.

        @return: The connecion configuration.
        """
        return ConnectionConfig(self.java_obj.createConnection(source[0], source[1], target[0], target[1], ActiveNetworkHandler(handler) if handler is not None else None))

    def destroy_connection(self, source, target, handler=None):
        """Destroys a connection between two components.

        Keyword arguments:
        @param source: A two-tuple indicating the source component name and output port.
        @param target: A two-tuple indicating the target component name and input port.
        @param handler: An asynchronous handler to be called once the network has been updated.

        @return: self
        """
        self.java_obj.destroyConnection(source[0] if isinstance(source, tuple) else source, target[0] if isinstance(target, tuple) else target, ActiveNetworkHandler(handler) if handler is not None else None)
        return self

class ActiveNetworkHandler(org.vertx.java.core.AsyncResultHandler):
    def __init__(self, handler):
        self.handler = handler
    def handle(self, result):
        if result.failed():
            self.handler(result.cause(), None)
        else:
            self.handler(None, ActiveNetwork(result.result()))
