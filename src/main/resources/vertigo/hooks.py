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
import org.vertx.java.platform.impl.JythonVerticleFactory
import org.vertx.java.core.Handler
from context import InstanceContext

class Hook(object):
  """A component hook."""
  def __init__(self, address):
    self.__hook = net.kuujo.vertigo.hooks.EventBusHookListener(address, org.vertx.java.platform.impl.JythonVerticleFactory.vertx.eventBus())
    self.__hook.startHandler(StartStopHandler(self))
    self.__hook.receiveHandler(MessageIdHandler(self.handle_receive))
    self.__hook.ackHandler(MessageIdHandler(self.handle_ack))
    self.__hook.failHandler(MessageIdHandler(self.handle_fail))
    self.__hook.emitHandler(MessageIdHandler(self.handle_emit))
    self.__hook.ackedHandler(MessageIdHandler(self.handle_acked))
    self.__hook.failedHandler(MessageIdHandler(self.handle_failed))
    self.__hook.timeoutHandler(MessageIdHandler(self.handle_timeout))
    self.__hook.stopHandler(StartStopHandler(self))

  def handle_start(self, context):
    """Called when the hooked component is started."""

  def handle_receive(self, id):
    """Called when the hook component received a message."""

  def handle_ack(self, id):
    """Called when the hook component acked a message."""

  def handle_fail(self, id):
    """Called when the hook component failed a message."""

  def handle_emit(self, id):
    """Called when the hook component emitted a message."""

  def handle_acked(self, id):
    """Called when the hook component received an ack for an emitted message."""

  def handle_failed(self, id):
    """Called when the hook component received a failure for an emitted message."""

  def handle_timeout(self, id):
    """Called when the hook component received a timeout for an emitted message."""

  def handle_stop(self, context):
    """Called when the hooked component is stopped."""

class StartStopHandler(org.vertx.java.core.Handler):
  def __init__(self, hook):
    self.hook = hook

  def handle(self, javacontext):
    self.hook(InstanceContext(javacontext))

class MessageIdHandler(org.vertx.java.core.Handler):
  def __init__(self, handler):
    self.handler = handler

  def handle(self, id):
    self.handler(id)
