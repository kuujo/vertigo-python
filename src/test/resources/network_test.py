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
from test import TestCase, Assert, run_test
import vertigo

class NetworkTestCase(TestCase):
    """A network test case."""
    def test_create_network(self):
        """Tests creating a network."""
        network = vertigo.create_network('test')
        self.assert_equals('test', network.name)
        component1 = network.add_verticle('test_verticle1', main='test_verticle1.py')
        self.assert_equals('test_verticle1', component1.name)
        self.assert_equals('test_verticle1.py', component1.main)
        component1.instances = 4
        self.assert_equals(4, component1.instances)
        component2 = network.add_verticle('test_verticle2', main='test_verticle2.py')
        component2.main = 'test_verticle3.py'
        self.assert_equals('test_verticle3.py', component2.main)
        self.complete()

    def test_basic_send(self):
        """Test sending a basic message between two components."""
        network = vertigo.create_network('test')
        network.add_verticle('sender', main='test_basic_sender.py')
        network.add_verticle('receiver', main='test_basic_receiver.py')
        network.create_connection(('sender', 'out'), ('receiver', 'in'))
        def handler(error, network):
            self.assert_null(error)
        vertigo.deploy_local_network(network, handler)

run_test(NetworkTestCase())
