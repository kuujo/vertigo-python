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
from vertigo.grouping import RoundGrouping
from vertigo.filter import TagsFilter

class NetworkTestCase(TestCase):
  """
  A network test case.
  """
  def test_create_network(self):
    """
    Tests creating a network.
    """
    network = vertigo.create_network('test')
    self.assert_equals('test', network.address)
    network.enable_acking()
    self.assert_true(network.acking)
    network.disable_acking()
    self.assert_false(network.acking)
    network.acking = True
    self.assert_true(network.acking)
    network.ack_expire = 60000
    self.assert_equals(60000, network.ack_expire)
    network.ack_delay = 1000
    self.assert_equals(1000, network.ack_delay)
    network.num_auditors = 2
    self.assert_equals(2, network.num_auditors)
    component1 = network.add_verticle('test_feeder_verticle', main='test_feeder_verticle.py')
    self.assert_equals('test_feeder_verticle', component1.address)
    self.assert_equals('test_feeder_verticle.py', component1.main)
    component1.instances = 4
    self.assert_equals(4, component1.instances)
    component2 = network.add_verticle('test_worker_verticle')
    self.assert_equals('verticle', component2.type)
    component2.main = 'test_worker_verticle.py'
    self.assert_equals('test_worker_verticle.py', component2.main)
    self.complete()

  def test_add_input(self):
    """
    Tests adding inputs to components.
    """
    network = vertigo.create_network('test')
    component1 = network.add_verticle('test_feeder_verticle', main='test_feeder_verticle.py')
    component2 = network.add_verticle('test_worker_verticle', main='test_worker_verticle.py', instances=2)
    component2.add_input('test_feeder_verticle')
    self.assert_equals(0, len(component1.inputs))
    self.assert_equals(1, len(component2.inputs))
    component2.add_input('test_feeder_verticle', grouping=RoundGrouping())
    self.assert_equals(2, len(component2.inputs))
    component2.add_input('test_feeder_verticle', TagsFilter('foo', 'bar'))
    self.assert_equals(3, len(component2.inputs))
    self.complete()

run_test(NetworkTestCase())
