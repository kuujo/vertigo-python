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
import net.kuujo.vertigo.context.NetworkContext
import org.vertx.java.core.json.JsonObject
from core.javautils import map_from_java, map_to_java

class _AbstractContext(object):
  """
  An abstract context.
  """
  def __init__(self, context):
    self._context = context

class NetworkContext(_AbstractContext):
  """
  A network context.
  """
  @staticmethod
  def from_dict(self, json):
    """Creates a network context from a dictionary."""
    return NetworkContext(net.kuujo.vertigo.context.NetworkContext.fromJson(org.vertx.java.core.json.JsonObject(map_to_java(json))))

  @property
  def address(self):
    return self._context.getAddress()

  @property
  def auditors(self):
    """A list of network auditors."""
    auditors = self._context.getAuditors()
    iterator = auditors.iterator()
    auditors = []
    while iterator.hasNext():
      auditors.append(iterator.next())
    return auditors

  @property
  def acking(self):
    """Indicates whether acking is enabled."""
    return self._context.isAckingEnabled()

  @property
  def ack_timeout(self):
    """The network ack timeout."""
    return self._context.getAckTimeout()

  @property
  def components(self):
    """A dictionary of component contexts, keyed by component addresses."""
    collection = self._context.getComponents()
    iterator = collection.iterator()
    components = {}
    while iterator.hasNext():
      component = iterator.next()
      components[component.getAddress()] = ComponentContext(component)
    return components

class ComponentContext(_AbstractContext):
  """
  A component context.
  """
  @property
  def address(self):
    """The component address."""
    return self._context.getAddress()

  @property
  def type(self):
    """The component type."""
    return self._context.getType()

  @property
  def is_module(self):
    """Indicates whether the component is a module."""
    return self._context.isModule()

  @property
  def is_verticle(self):
    """Indicates whether the component is a verticle."""
    return self._context.isVerticle()

  @property
  def module(self):
    """The module name (if the component is a module)."""
    if self.is_module:
      return self._context.getModule()

  @property
  def main(self):
    """The verticle main (if the component is a verticle)."""
    if self.is_verticle:
      return self._context.getMain()

  @property
  def config(self):
    """The component configuration."""
    return map_from_java(self._context.getConfig().toMap())

  @property
  def instances(self):
    """A list of component instance contexts."""
    collection = self._context.getInstances()
    iterator = collection.iterator()
    instances = []
    while iterator.hasNext():
      instances.append(InstanceContext(iterator.next()))
    return instances

  @property
  def network(self):
    """The parent network context."""
    return NetworkContext(self._context.getNetwork())

class InstanceContext(_AbstractContext):
  """
  An instance context.
  """
  @property
  def id(self):
    """The instance ID."""
    return self._context.id()

  @property
  def component(self):
    """The parent component context."""
    return ComponentContext(self._context.getComponent())
