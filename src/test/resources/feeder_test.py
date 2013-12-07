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
from test import TestCase, run_test
import vertigo

class FeederTestCase(TestCase):
  """
  A feeder test case.
  """
  def _create_network(self, feeder, worker):
    network = vertigo.create_network('test')
    network.acking = True
    network.add_feeder('test_feeder', feeder)
    network.add_worker('test_worker', worker).add_input('test_feeder')
    return network

  def _create_fail_network(self, feeder):
    network = vertigo.create_network('test')
    network.acking = True
    network.add_feeder('test_feeder', feeder)
    network.add_worker('test_worker', 'test_failing_worker.py').add_input('test_feeder')
    return network

  def test_feeder_ack(self):
    """
    Tests the basic feeder acking support.
    """
    network = self._create_network('test_acking_feeder.py', 'test_acking_worker.py')
    def deploy_handler(error, context):
      self.assert_null(error)
      self.assert_not_null(context)
    vertigo.deploy_local_network(network, deploy_handler)

  def test_feeder_fail(self):
    """
    Tests the basic feeder fail support.
    """
    network = self._create_network('test_failing_feeder.py', 'test_failing_worker.py')
    def deploy_handler(error, context):
      self.assert_null(error)
      self.assert_not_null(context)
    vertigo.deploy_local_network(network, deploy_handler)

run_test(FeederTestCase())
