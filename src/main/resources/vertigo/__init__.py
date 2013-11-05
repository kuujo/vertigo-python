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

def create_network(address):
  """
  Creates a new network.
  """
  return Network(address)

def create_basic_feeder(context=None):
  """
  Creates a basic feeder.
  """
  return BasicFeeder(context)

def create_polling_feeder(context=None):
  """
  Creates a polling feeder.
  """
  return PollingFeeder(context)

def create_stream_feeder(context=None):
  """
  Creates a stream feeder.
  """
  return StreamFeeder(context)

def create_basic_executor(context=None):
  """
  Creates a basic executor.
  """
  return BasicExecutor(context)

def create_polling_executor(context=None):
  """
  Creates a polling executor.
  """
  return PollingExecutor(context)

def create_stream_executor(context=None):
  """
  Creates a stream executor.
  """
  return StreamExecutor(context)

def create_worker(context=None):
  """
  Creates a basic worker.
  """
  return BasicWorker(context)
