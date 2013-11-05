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
    """
    Creates a network context from a dictionary.
    """
    return NetworkContext(net.kuujo.vertigo.context.NetworkContext.fromJson(org.vertx.java.core.json.JsonObject(map_to_java(json))))

  @property
  def address(self):
    return self._context.getAddress()

  @property
  def broadcast_address(self):
    return self._context.getBroadcastAddress()

  @property
  def auditors(self):
    auditors = self._context.getAuditors()
    iterator = auditors.iterator()
    return [iterator.next() while iterator.hasNext()]

  @property
  def components(self):
    collection = self._context.getComponents()
    iterator = collection.iterator()
    return [ComponentContext(iterator.next()) while iterator.hasNext()]

class ComponentContext(_AbstractContext):
  """
  A component context.
  """
  @property
  def address(self):
    return self._context.getAddress()

  @property
  def type(self):
    return self._context.getType()

  @property
  def is_module(self):
    return self._context.isModule()

  @property
  def is_verticle(self):
    return self._context.isVerticle()

  @property
  def module(self):
    if self.is_module:
      return self._context.getModule()

  @property
  def main(self):
    if self.is_verticle:
      return self._context.getMain()

  @property
  def config(self):
    return map_from_java(self._context.config().toMap())

  @property
  def instances(self):
    collection = self._context.getInstances()
    iterator = collection.iterator()
    return [InstanceContext(iterator.next()) while iterator.hasNext()]

  @property
  def network(self):
    return NetworkContext(self._context.getNetwork())

class InstanceContext(_AbstractContext):
  """
  An instance context.
  """
  @property
  def id(self):
    return self._context.id()

  @property
  def component(self):
    return ComponentContext(self._context.getComponent())
