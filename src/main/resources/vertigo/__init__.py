# Copyright 2014 the original author or authors.
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
import sys
import net.kuujo.vertigo.Vertigo
import org.vertx.java.platform.impl.JythonVerticleFactory
import org.vertx.java.core.json.JsonObject
from core.javautils import map_to_java
from network import NetworkConfig, ActiveNetwork

this = sys.modules[__name__]

_vertigo = net.kuujo.vertigo.Vertigo(org.vertx.java.platform.impl.JythonVerticleFactory.vertx, org.vertx.java.platform.impl.JythonVerticleFactory.container)

def create_network(network):
    """Creates a new network.

    Keyword arguments:
    @param name: The network name or dictionary configuration.

    @return: A new network instance.
    """
    if isinstance(network, dict):
        return NetworkConfig(org.vertx.java.core.json.JsonObject(_vertigo.createNetwork(map_to_java(network))))
    return NetworkConfig(_vertigo.createNetwork(network))

class ClusterManager(object):
    """Vertigo cluster manager."""
    def __init__(self, java_obj):
        self.java_obj = java_obj

    @property
    def address(self):
        """Returns the cluster address."""
        return self.java_obj.address()

    def get_network(self, network, handler):
        """Loads a network from the cluster.

        @param network: The name of the network to load.
        @param handler: A handler to be called once the network is loaded.

        @return: self
        """
        self.java_obj.getNetwork(network, _DeployHandler(handler))
        return self

    def get_networks(self, handler):
        """Loads all networks from the cluster.

        @param handler: A handler to be called once the networks are loaded.

        @return: self
        """
        self.java_obj.getNetworks(_GetsHandler(handler))
        return self

    def deploy_network(self, network, handler=None):
        """Deploys a network to the cluster.

        Keyword arguments:
        @param network: The network to deploy.
        @param handler: A handler to be called once complete.

        @return: self
        """
        if isinstance(network, dict):
            if handler is not None:
                self.java_obj.deployNetwork(org.vertx.java.core.json.JsonObject(map_to_java(network)), _DeployHandler(handler))
            else:
                self.java_obj.deployNetwork(org.vertx.java.core.json.JsonObject(map_to_java(network)))
        else:
            if handler is not None:
                self.java_obj.deployNetwork(network if isinstance(network, basestring) else network.java_obj, _DeployHandler(handler))
            else:
                self.java_obj.deployNetwork(network if isinstance(network, basestring) else network.java_obj)
        return self

    def undeploy_network(self, network, handler=None):
        """Undeploys a network from the cluster.

        Keyword arguments:
        @param network: The network to undeploy.
        @param handler: A handler to be called once complete.

        @return: self
        """
        if isinstance(network, dict):
            if handler is not None:
                self.java_obj.undeployNetwork(org.vertx.java.core.json.JsonObject(map_to_java(network)), _UndeployHandler(handler))
            else:
                self.java_obj.undeployNetwork(org.vertx.java.core.json.JsonObject(map_to_java(network)))
        else:
            if handler is not None:
                self.java_obj.undeployNetwork(network if isinstance(network, basestring) else network.java_obj, _UndeployHandler(handler))
            else:
                self.java_obj.undeployNetwork(network if isinstance(network, basestring) else network.java_obj)
        return self

def deploy_cluster(address, nodes=None, handler=None):
    """Deploys a cluster.

    Keyword arguments:
    @param address: The address at which to deploy the cluster
    @param nodes: The number of nodes to deploy.
    @param handler: A handler to be called once complete.

    @return: The current Vertigo instance.
    """
    if nodes is None:
        nodes = 1
    if handler is not None:
        _vertigo.deployCluster(address, nodes, _ClusterHandler(handler))
    else:
        _vertigo.deployCluster(address, nodes)
    return this

def get_cluster(address):
    """Loads a cluster manager for the given cluster.

    Keyword arguments:
    @param address: The address of the cluster to load.

    @return: A cluster manager.
    """
    return ClusterManager(_vertigo.getCluster(address))

def deploy_network(cluster, network, handler=None):
    """Deploys a network.

    Keyword arguments:
    @param cluster: The cluster to which to deploy the network.
    @param network: The network name or configuration to deploy.
    @param handler: An optional asynchronous handler to be called once the deployment
    is complete.

    @return: The current vertigo instance.
    """
    if isinstance(network, dict):
        network = _vertigo.createNetwork(org.vertx.java.core.json.JsonObject(map_to_java(network)))
    if handler is not None:
        _vertigo.deployNetwork(cluster, network if isinstance(network, basestring) else network.java_obj, _DeployHandler(handler))
    else:
        _vertigo.deployNetwork(cluster, network if isinstance(network, basestring) else network.java_obj)
    return this

def undeploy_network(cluster, network, handler=None):
    """Undeploys a network.

    Keyword arguments:
    @param cluster: The cluster from which to undeploy the network.
    @param context: The network configuration or name for the network to undeploy.
    @param handler: An optional asynchronous handler to be called once the undeployment
    is complete.

    @return: The current vertigo instance.
    """
    if isinstance(network, dict):
        network = _vertigo.createNetwork(org.vertx.java.core.json.JsonObject(map_to_java(network)))
    if handler is not None:
        _vertigo.undeployNetwork(cluster, network if isinstance(network, basestring) else network.java_obj, _UndeployHandler(handler))
    else:
        _vertigo.undeployNetwork(cluster, network if isinstance(network, basestring) else network.java_obj)
    return this

class _ClusterHandler(org.vertx.java.core.AsyncResultHandler):
    def __init__(self, handler):
        self._handler = handler
    def handle(self, result):
        if result.succeeded():
            self._handler(None, ClusterManager(result.result()))
        else:
            self._handler(result.cause(), None)

class _DeployHandler(org.vertx.java.core.AsyncResultHandler):
    def __init__(self, handler):
        self._handler = handler
    def handle(self, result):
        if result.succeeded():
            self._handler(None, ActiveNetwork(result.result()))
        else:
            self._handler(result.cause(), None)

class _UndeployHandler(org.vertx.java.core.AsyncResultHandler):
    def __init__(self, handler):
        self._handler = handler
    def handle(self, result):
        if result.succeeded():
            self._handler(None)
        else:
            self._handler(result.cause())

class _GetsHandler(org.vertx.java.core.AsyncResultHandler):
    def __init__(self, handler):
        self._handler = handler
    def handle(self, result):
        if result.succeeded():
            results = []
            for item in result.result():
                results.append(ActiveNetwork(item))
            self._handler(results)
        else:
            self._handler(result.cause(), None)
