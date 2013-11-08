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
from network import Network
from worker import BasicWorker
from feeder import BasicFeeder, PollingFeeder, StreamFeeder
from rpc import BasicExecutor, PollingExecutor, StreamExecutor
import net.kuujo.vertigo.Vertigo
import org.vertx.java.platform.impl.JythonVerticleFactory

vertigo = net.kuujo.vertigo.Vertigo(org.vertx.java.platform.impl.JythonVerticleFactory.vertx, org.vertx.java.platform.impl.JythonVerticleFactory.container)

def is_component():
  """
  Indicates whether the current verticle is a Vertigo component instance.
  """
  return vertigo.isComponent()

def create_network(address):
  """
  Creates a new network.
  """
  return Network(address)

def create_feeder():
  """
  Creates a basic feeder.
  """
  return create_basic_feeder()

def create_basic_feeder():
  """
  Creates a basic feeder.
  """
  return BasicFeeder(vertigo.createBasicFeeder())

def create_polling_feeder():
  """
  Creates a polling feeder.
  """
  return PollingFeeder(vertigo.createPollingFeeder())

def create_stream_feeder():
  """
  Creates a stream feeder.
  """
  return StreamFeeder(vertigo.createStreamFeeder())

def create_executor():
  """
  Creates a basic executor.
  """
  return create_basic_executor()

def create_basic_executor():
  """
  Creates a basic executor.
  """
  return BasicExecutor(vertigo.createBasicExecutor())

def create_polling_executor():
  """
  Creates a polling executor.
  """
  return PollingExecutor(vertigo.createPollingExecutor())

def create_stream_executor():
  """
  Creates a stream executor.
  """
  return StreamExecutor(vertigo.createStreamExecutor())

def create_worker():
  """
  Creates a basic worker.
  """
  return create_basic_worker()

def create_basic_worker():
  """
  Creates a basic worker.
  """
  return BasicWorker(vertigo.createBasicWorker())
