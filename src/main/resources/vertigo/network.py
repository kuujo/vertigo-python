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
import net.kuujo.vertigo.network.Network
import net.kuujo.vertigo.network.Verticle
import net.kuujo.vertigo.network.Module
import net.kuujo.vertigo.hooks.EventBusHook
import org.vertx.java.core.json.JsonObject
from core.javautils import map_to_java
from input import Input
from grouping import Grouping

class Network(object):
  """
  A Vertigo network.
  """
  def __init__(self, address):
    self._network = net.kuujo.vertigo.network.Network(address)

  @property
  def address(self):
    return self._network.getAddress()

  def get_num_auditors(self):
    """The number of network auditors."""
    return self._network.getNumAuditors()

  def set_num_auditors(self, num):
    """The number of network auditors."""
    self._network.setNumAuditors(num)

  num_auditors = property(get_num_auditors, set_num_auditors)

  def enable_acking(self):
    """Enables acking on the network."""
    self._network.enableAcking()
    return self

  def disable_acking(self):
    """Disables acking on the network."""
    self._network.disableAcking()
    return self

  def set_acking(self, acking):
    """Sets network acking."""
    if acking:
      self._network.enableAcking()
    else:
      self._network.disableAcking()

  def get_acking(self):
    """Gets network acking."""
    return self._network.isAckingEnabled()

  acking = property(get_acking, set_acking)

  def get_ack_timeout(self):
    """Gets the network ack timeout."""
    return self._network.getAckTimeout()

  def set_ack_timeout(self, timeout):
    """Sets the network ack timeout."""
    self._network.setAckTimeout(timeout)

  ack_expire = property(get_ack_timeout, set_ack_timeout)

  def add_component(self, component):
    """Adds a component to the network."""
    self._network.addComponent(component._component)
    return component

  def add_verticle(self, address, main=None, config=None, instances=1):
    """Adds a verticle component to the network.

    Keyword arguments:
    @param address: The component event bus address.
    @param main: The verticle main.
    @param config: The verticle component configuration.
    @param instances: The number of verticle instances.

    @return: A new Verticle component definition.
    """
    if main is not None and config is not None:
      return Verticle(self._network.addVerticle(address, main, map_to_java(config), instances))
    elif main is not None:
      return Verticle(self._network.addVerticle(address, main, instances))
    elif config is not None:
      return Verticle(self._network.addVerticle(address, map_to_java(config), instances))
    else:
      return Verticle(self._network.addVerticle(address).setInstances(instances))

  def add_module(self, address, module=None, config=None, instances=1):
    """Adds a module component to the network.

    Keyword arguments:
    @param address: The component event bus address.
    @param main: The module name.
    @param config: The module component configuration.
    @param instances: The number of module instances.

    @return: A new Module component definition.
    """
    if module is not None and config is not None:
      return Module(self._network.addModule(address, module, map_to_java(config), instances))
    elif module is not None:
      return Module(self._network.addModule(address, module, instances))
    elif config is not None:
      return Module(self._network.addModule(address, map_to_java(config), instances))
    else:
      return Module(self._network.addModule(address).setInstances(instances))

  @property
  def components(self):
    components = []
    iterator = self._network.getComponents().iterator()
    while iterator.hasNext():
      info = iterator.next()
      if info.isModule():
        components.append(Module(info))
      elif info.isVerticle():
        components.append(Verticle(info))
    return components

class Component(object):
  """
  A base component.
  """
  def __init__(self, component):
    self._component = component
    self._hooked = False

  @property
  def address(self):
    """The component address."""
    return self._component.getAddress()

  @property
  def type(self):
    """The component type, either "module" or "verticle"."""
    return self._component.getType()

  def set_config(self, config):
    """Sets the component configuration."""
    self._component.setConfig(org.vertx.java.core.json.JsonObject(map_to_java(config)))

  def get_config(self):
    """Gets the component configuration."""
    return map_from_java(self._component.getConfig().toMap())

  config = property(get_config, set_config)

  def get_instances(self):
    """Gets the number of component instances."""
    return self._component.getInstances()

  def set_instances(self, instances):
    """Sets the number of component instances."""
    self._component.setInstances(instances)

  instances = property(get_instances, set_instances)

  def add_hook(self, hook):
    """Adds a hook to the component.

    Keyword arguments:
    @param hook: The Hook to add to the component.

    @return: self
    """
    if not self._hooked:
      self._component.addHook(net.kuujo.vertigo.hooks.EventBusHook())
    return self

  @property
  def hooks(self):
    """Gets a list of hooks.

    @return: A list of component hooks.
    """
    iterator = self._component.getHooks().iterator()
    hooks = []
    while iterator.hasNext():
      hooks.append(iterator.next())
    return hooks

  def add_input(self, address, grouping=None, *filters):
    """Adds an input to the component.

    Keyword arguments:
    @param address: The input address. This is the event bus address of the component
    from which this component should receive messages via the added input.
    @param grouping: An input grouping.
    @param filters: A list of input filters.
    @return: A new Input instance.
    """
    if grouping is not None:
      if isinstance(grouping, Grouping):
        return Input(self._component.addInput(address, grouping._grouping, *[filter._filter for filter in filters]))
      else:
        return Input(self._component.addInput(address, grouping._filter, *[filter._filter for filter in filters]))
    else:
      return Input(self._component.addInput(address))

  @property
  def inputs(self):
    """A list of component inputs."""
    iterator = self._component.getInputs().iterator()
    inputs = []
    while iterator.hasNext():
      inputs.append(Input(iterator.next()))
    return inputs

class Verticle(Component):
  """
  A verticle component.
  """
  def get_main(self):
    """Gets the verticle main."""
    return self._component.getMain()

  def set_main(self, main):
    """Sets the verticle main."""
    self._component.setMain(main)

  main = property(get_main, set_main)

class Module(Component):
  """
  A module component.
  """
  def get_module(self):
    """Gets the module name."""
    return self._component.getModule()

  def set_module(self, module):
    """Sets the module name."""
    self._component.setModule(module)

  module = property(get_module, set_module)
