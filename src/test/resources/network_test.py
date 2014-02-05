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
from vertigo.network import Verticle, Module
from vertigo.context import NetworkContext, ComponentContext, InstanceContext
from vertigo.grouping import RoundGrouping

class NetworkTestCase(TestCase):
    """
    A network test case.
    """
    def check_context(self, context):
        """
        Checks a network context.
        """
        Assert.false(context.address == None)
        Assert.true(isinstance(context.auditors, list))
        Assert.true(len(context.auditors) > 0)
        Assert.true(context.acking)
        Assert.true(context.ack_timeout > 0)
        Assert.true(isinstance(context.components, dict))
        Assert.true(len(context.components) > 0)

        for address, component in context.components.iteritems():
            Assert.true(isinstance(component, ComponentContext))
            Assert.equals(context.address, component.network.address)
            Assert.false(component.address == None)
            Assert.true(component.type in ('feeder', 'worker', 'executor'))
            Assert.true(component.is_module or component.is_verticle)
            if component.is_module:
                Assert.false(component.module == None)
            elif component.is_verticle:
                Assert.false(component.main == None)
            Assert.true(isinstance(component.config, dict))
            Assert.true(isinstance(component.instances, list))
            Assert.true(isinstance(component.network, NetworkContext))
            for instance in component.instances:
                Assert.true(isinstance(instance, InstanceContext))
                Assert.true(isinstance(instance.component, ComponentContext))
                Assert.equals(component.address, instance.component.address)

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
        network.num_auditors = 2
        self.assert_equals(2, network.num_auditors)
        component1 = network.add_feeder('test_feeder_verticle', main='test_feeder_verticle.py')
        self.assert_equals('test_feeder_verticle', component1.address)
        self.assert_equals('test_feeder_verticle.py', component1.main)
        component1.instances = 4
        self.assert_equals(4, component1.instances)
        component2 = network.add_worker('test_worker_verticle', main='test_worker_verticle.py')
        self.assert_equals('worker', component2.type)
        component2.main = 'test_worker_verticle.py'
        self.assert_equals('test_worker_verticle.py', component2.main)
        self.complete()

    def test_add_feeder(self):
        """
        Tests adding a feeder to a network.
        """
        network = vertigo.create_network('test')
        self.assert_equals('test', network.address)
        component = network.add_feeder('test_feeder', main='test_feeder.py', config={'foo': 'bar'}, instances=2)
        self.assert_true(isinstance(component, Verticle))
        self.assert_equals('test_feeder.py', component.main)
        self.assert_equals('bar', component.config['foo'])
        component.config = {'bar': 'baz'}
        self.assert_equals('baz', component.config['bar'])
        self.assert_equals(2, component.instances)
        component.instances = 1
        self.assert_equals(1, component.instances)
        self.assert_false(component.worker)
        component.worker = True
        self.assert_true(component.worker)
        self.assert_false(component.multi_threaded)
        component.multi_threaded = True
        self.assert_true(component.multi_threaded)
        self.complete()

    def test_add_feeder_module(self):
        """
        Tests adding a feeder to a network.
        """
        network = vertigo.create_network('test')
        self.assert_equals('test', network.address)
        component = network.add_feeder_module('test_feeder', module='com.test~test~0.1', config={'foo': 'bar'}, instances=2)
        self.assert_true(isinstance(component, Module))
        self.assert_equals('com.test~test~0.1', component.module)
        self.assert_equals('bar', component.config['foo'])
        component.config = {'bar': 'baz'}
        self.assert_equals('baz', component.config['bar'])
        self.assert_equals(2, component.instances)
        component.instances = 1
        self.assert_equals(1, component.instances)
        self.complete()

    def test_add_feeder_verticle(self):
        """
        Tests adding a feeder to a network.
        """
        network = vertigo.create_network('test')
        self.assert_equals('test', network.address)
        component = network.add_feeder_verticle('test_feeder', main='test_feeder.py', config={'foo': 'bar'}, instances=2)
        self.assert_true(isinstance(component, Verticle))
        self.assert_equals('test_feeder.py', component.main)
        self.assert_equals('bar', component.config['foo'])
        component.config = {'bar': 'baz'}
        self.assert_equals('baz', component.config['bar'])
        self.assert_equals(2, component.instances)
        component.instances = 1
        self.assert_equals(1, component.instances)
        self.assert_false(component.worker)
        component.worker = True
        self.assert_true(component.worker)
        self.assert_false(component.multi_threaded)
        component.multi_threaded = True
        self.assert_true(component.multi_threaded)
        self.complete()

    def test_add_executor(self):
        """
        Tests adding an executor to a network.
        """
        network = vertigo.create_network('test')
        self.assert_equals('test', network.address)
        component = network.add_executor('test_executor', main='test_executor.py', config={'foo': 'bar'}, instances=2)
        self.assert_true(isinstance(component, Verticle))
        self.assert_equals('test_executor.py', component.main)
        self.assert_equals('bar', component.config['foo'])
        component.config = {'bar': 'baz'}
        self.assert_equals('baz', component.config['bar'])
        self.assert_equals(2, component.instances)
        component.instances = 1
        self.assert_equals(1, component.instances)
        self.assert_false(component.worker)
        component.worker = True
        self.assert_true(component.worker)
        self.assert_false(component.multi_threaded)
        component.multi_threaded = True
        self.assert_true(component.multi_threaded)
        self.complete()

    def test_add_executor_module(self):
        """
        Tests adding an executor to a network.
        """
        network = vertigo.create_network('test')
        self.assert_equals('test', network.address)
        component = network.add_executor_module('test_executor', module='com.test~test~0.1', config={'foo': 'bar'}, instances=2)
        self.assert_true(isinstance(component, Module))
        self.assert_equals('com.test~test~0.1', component.module)
        self.assert_equals('bar', component.config['foo'])
        component.config = {'bar': 'baz'}
        self.assert_equals('baz', component.config['bar'])
        self.assert_equals(2, component.instances)
        component.instances = 1
        self.assert_equals(1, component.instances)
        self.complete()

    def test_add_executor_verticle(self):
        """
        Tests adding an executor to a network.
        """
        network = vertigo.create_network('test')
        self.assert_equals('test', network.address)
        component = network.add_executor_verticle('test_executor', main='test_executor.py', config={'foo': 'bar'}, instances=2)
        self.assert_true(isinstance(component, Verticle))
        self.assert_equals('test_executor.py', component.main)
        self.assert_equals('bar', component.config['foo'])
        component.config = {'bar': 'baz'}
        self.assert_equals('baz', component.config['bar'])
        self.assert_equals(2, component.instances)
        component.instances = 1
        self.assert_equals(1, component.instances)
        self.assert_false(component.worker)
        component.worker = True
        self.assert_true(component.worker)
        self.assert_false(component.multi_threaded)
        component.multi_threaded = True
        self.assert_true(component.multi_threaded)
        self.complete()

    def test_add_worker(self):
        """
        Tests adding a worker to a network.
        """
        network = vertigo.create_network('test')
        self.assert_equals('test', network.address)
        component = network.add_worker('test_worker', main='test_worker.py', config={'foo': 'bar'}, instances=2)
        self.assert_true(isinstance(component, Verticle))
        self.assert_equals('test_worker.py', component.main)
        self.assert_equals('bar', component.config['foo'])
        component.config = {'bar': 'baz'}
        self.assert_equals('baz', component.config['bar'])
        self.assert_equals(2, component.instances)
        component.instances = 1
        self.assert_equals(1, component.instances)
        self.assert_false(component.worker)
        component.worker = True
        self.assert_true(component.worker)
        self.assert_false(component.multi_threaded)
        component.multi_threaded = True
        self.assert_true(component.multi_threaded)
        self.complete()

    def test_add_worker_module(self):
        """
        Tests adding a worker to a network.
        """
        network = vertigo.create_network('test')
        self.assert_equals('test', network.address)
        component = network.add_worker_module('test_worker', module='com.test~test~0.1', config={'foo': 'bar'}, instances=2)
        self.assert_true(isinstance(component, Module))
        self.assert_equals('com.test~test~0.1', component.module)
        self.assert_equals('bar', component.config['foo'])
        component.config = {'bar': 'baz'}
        self.assert_equals('baz', component.config['bar'])
        self.assert_equals(2, component.instances)
        component.instances = 1
        self.assert_equals(1, component.instances)
        self.complete()

    def test_add_worker_verticle(self):
        """
        Tests adding a worker to a network.
        """
        network = vertigo.create_network('test')
        self.assert_equals('test', network.address)
        component = network.add_worker_verticle('test_worker', main='test_worker.py', config={'foo': 'bar'}, instances=2)
        self.assert_true(isinstance(component, Verticle))
        self.assert_equals('test_worker.py', component.main)
        self.assert_equals('bar', component.config['foo'])
        component.config = {'bar': 'baz'}
        self.assert_equals('baz', component.config['bar'])
        self.assert_equals(2, component.instances)
        component.instances = 1
        self.assert_equals(1, component.instances)
        self.assert_false(component.worker)
        component.worker = True
        self.assert_true(component.worker)
        self.assert_false(component.multi_threaded)
        component.multi_threaded = True
        self.assert_true(component.multi_threaded)
        self.complete()
    
    def test_add_input(self):
        """
        Tests adding inputs to components.
        """
        network = vertigo.create_network('test')
        component1 = network.add_feeder('test_feeder_verticle', main='test_feeder_verticle.py')
        component2 = network.add_worker('test_worker_verticle', main='test_worker_verticle.py', instances=2)
        component2.add_input('test_feeder_verticle')
        self.assert_equals(0, len(component1.inputs))
        self.assert_equals(1, len(component2.inputs))
        component2.add_input('test_feeder_verticle', grouping=RoundGrouping())
        self.assert_equals(2, len(component2.inputs))
        self.complete()
    
    def _create_feeder_network(self, feeder, worker):
        network = vertigo.create_network('test')
        network.acking = True
        network.add_feeder('test_feeder', feeder)
        network.add_worker('test_worker', worker).add_input('test_feeder')
        return network
    
    def test_feeder_ack(self):
        """
        Tests the basic feeder acking support.
        """
        network = self._create_feeder_network('test_acking_feeder.py', 'test_acking_worker.py')
        def deploy_handler(error, context):
            self.assert_null(error)
            self.assert_not_null(context)
            self.check_context(context)
        vertigo.deploy_local_network(network, deploy_handler)
    
    def test_feeder_fail(self):
        """
        Tests the basic feeder fail support.
        """
        network = self._create_feeder_network('test_failing_feeder.py', 'test_failing_worker.py')
        def deploy_handler(error, context):
            self.assert_null(error)
            self.assert_not_null(context)
            self.check_context(context)
        vertigo.deploy_local_network(network, deploy_handler)
    
    def test_feeder_timeout(self):
        """
        Tests the basic feeder timeout support.
        """
        network = self._create_feeder_network('test_timeout_feeder.py', 'test_timeout_worker.py')
        network.ack_timeout = 500
        def deploy_handler(error, context):
            self.assert_null(error)
            self.assert_not_null(context)
            self.check_context(context)
        vertigo.deploy_local_network(network, deploy_handler)
    
    def _create_executor_network(self, executor, worker):
        network = vertigo.create_network('test')
        network.acking = True
        network.add_executor('test_executor', executor).add_input('test_worker')
        network.add_worker('test_worker', worker).add_input('test_executor')
        return network
    
    def test_executor_ack(self):
        """
        Tests the basic executor acking support.
        """
        network = self._create_executor_network('test_acking_executor.py', 'test_acking_worker.py')
        def deploy_handler(error, context):
            self.assert_null(error)
            self.assert_not_null(context)
            self.check_context(context)
        vertigo.deploy_local_network(network, deploy_handler)
    
    def test_executor_timeout(self):
        """
        Tests the basic executor timeout support.
        """
        network = self._create_executor_network('test_timeout_executor.py', 'test_timeout_worker.py')
        network.ack_timeout = 500
        def deploy_handler(error, context):
            self.assert_null(error)
            self.assert_not_null(context)
            self.check_context(context)
        vertigo.deploy_local_network(network, deploy_handler)

    def test_nested_network(self):
        """
        Tests a simple nested network.
        """
        network1 = vertigo.create_network('test1')
        network1.add_feeder('test1.feeder1', 'test_periodic_feeder.py')
        def deploy_handler(error, context):
            self.assert_null(error)
            self.assert_not_null(context)
            self.check_context(context)
            network2 = vertigo.create_network('test2')
            network2.add_worker('test2.worker1', 'test_completing_worker.py').add_input('test1.feeder1')
            def deploy_handler2(error, context):
                self.assert_null(error)
                self.assert_not_null(context)
                self.check_context(context)
            vertigo.deploy_local_network(network2, deploy_handler2)
        vertigo.deploy_local_network(network1, deploy_handler)

    def test_event_bus_hook(self):
        """
        Tests running an event bus hook.
        """
        network = vertigo.create_network('test')
        network.acking = True
        network.add_feeder('test_feeder', 'test_acking_feeder.py')
        worker = network.add_worker('test_worker', 'test_acking_worker.py')
        worker.add_input('test_feeder')
    
        @worker.hook('start')
        def handle_start(context):
            self.assert_true(context.id[:11] == 'test_worker')
    
        def deploy_handler(error, context):
            self.assert_null(error)
            self.assert_not_null(context)
            self.check_context(context)
        vertigo.deploy_local_network(network, deploy_handler)

run_test(NetworkTestCase())
