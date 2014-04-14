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
from core.java_utils import map_from_java, map_to_java
import net.kuujo.vertigo.network.ModuleConfig
import net.kuujo.vertigo.network.VerticleConfig

class Config(object):
    """Base configuration."""
    def __init__(self, java_obj):
        self.java_obj = java_obj

class NetworkConfig(Config):
    """Network configuration."""
    @property
    def name(self):
        return self.java_obj.getName()

    def add_component(self, name, main, config=None, instances=1):
        """Adds a component to the network."""
        component = self.java_obj.addComponent(name, main, config, instances)
        if isinstance(component, net.kuujo.vertigo.network.ModuleConfig):
            return ModuleConfig(component);
        else:
            return VerticleConfig(component)

    def add_verticle(self, name, main, config=None, instances=1):
        """Adds a verticle component to the network."""
        return VerticleConfig(self.java_obj.addVerticle(name, main, config, instances))

    def add_module(self, name, module, config=None, instances=1):
        """Adds a module component to the network."""
        return ModuleConfig(self.java_obj.addModule(name, module, config, instances))

    def create_connection(self, source, target):
        """Creates a connection between two components."""
        return ConnectionConfig(self.java_obj.createConnection(source[0], source[1], target[0], target[1]))

    def destroy_connection(self, source, target):
        """Destroys a connection between two components."""
        self.java_obj.destroyConnection(source[0] if isinstance(source, tuple) else source, target[0] if isinstance(target, tuple) else target)
        return self

class ComponentConfig(Config):
    """Component configuration."""
    MODULE = "module"
    VERTICLE = "verticle"

    @property
    def type(self):
        return self.java_obj.getType().toString()

    @property
    def name(self):
        return self.java_obj.getName()

    def get_config(self):
        return map_from_java(self.java_obj.getConfig())

    def set_config(self, config):
        self.java_obj.setConfig(map_to_java(config))
        return self

    config = property(get_config, set_config)

    def get_instances(self):
        return self.java_obj.getInstances()

    def set_instances(self, instances):
        self.java_obj.setInstances(instances)
        return self

    instances = property(get_instances, set_instances)

    def get_group(self):
        return self.java_obj.getGroup()

    def set_group(self, group):
        self.java_obj.setGroup(group)
        return self

    group = property(get_group, set_group)

class ModuleConfig(ComponentConfig):
    """Module component configuration."""
    def get_module(self):
        return self.java_obj.getModule()

    def set_module(self, module):
        self.java_obj.setModule(module)
        return self

    module = property(get_module, set_module)

class VerticleConfig(ComponentConfig):
    """Verticle component configuration."""
    def get_main(self):
        return self.java_obj.getMain()

    def set_main(self, main):
        self.java_obj.setMain(main)
        return self

    main = property(get_main, set_main)

    def is_worker(self):
        return self.java_obj.isWorker()

    def set_worker(self, worker):
        self.java_obj.setWorker(worker)
        return self

    worker = property(is_worker, set_worker)

    def is_multi_threaded(self):
        return self.java_obj.isMultiThreaded()

    def set_multi_threaded(self, multi_threaded):
        self.java_obj.setMultiThreaded(multi_threaded)
        return self

    multi_threaded = property(get_multi_threaded, set_multi_threaded)

class ConnectionConfig(Config):
    """Connection configuration."""
    @property
    def source(self):
        return Endpoint(self.java_obj.getSource())

    @property
    def target(self):
        return Endpoint(self.java_obj.getTarget())

    def random_groupin(self):
        self.java_obj.randomGrouping()
        return self

    def round_grouping(self):
        self.java_obj.roundGrouping()
        return self

    def hash_grouping(self):
        self.java_obj.hashGrouping()
        return self

    def fair_grouping(self):
        self.java_obj.fairGrouping()
        return self

    def all_grouping(self):
        self.java_obj.allGrouping()
        return self

    class Endpoint(Config):
        """Connection endpoint information."""
        def get_component(self):
            return self.java_obj.getComponent()

        def set_component(self, component):
            self.java_obj.setComponent(component)
            return self

        component = property(get_component, set_component)

        def get_port(self):
            return self.java_obj.getPort()

        def set_port(self, port):
            self.java_obj.setPort(port)
            return self

        port = property(get_port, set_port)

class ActiveNetwork(Config):
    """Active network configuration."""
    def add_component(self, name, main, config=None, instances=1, handler=None):
        """Adds a component to the network."""

    def add_module(self, name, main, config=None, instances=1, handler=None):
        """Adds a module component to the network."""

    def add_verticle(self, name, main, config=None, instances=1, handler=None):
        """Adds a verticle component to the network."""

    def create_connection(self, source, target, handler=None):
        """Creates a connection between two components in the network."""

    def destroy_connection(self, source, target, handler=None):
        """Destroys a connection between two components in the network."""
