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
import component
from core.javautils import map_to_java
import org.vertx.java.core.AsyncResultHandler

if component._component is None:
    raise ImportError("Not a valid Vertigo component.")

address = component._component.cluster().address()

def is_deployed(self, deployment_id, handler):
    """Checks whether a deployment is deployed.

    Keyword arguments:
    @param deployment_id: The deployment ID of the deployment to check.
    @param handler: An asynchronous handler to be called with the result.

    @return: self
    """
    component._component.cluster().isDeployed(name, DeployHandler(handler))
    return self

def deploy_module(self, deployment_id, module, config=None, instances=1, ha=False, handler=None):
    """Deploys a module.

    Keyword arguments:
    @param deploymen_id: The unique deployment ID of the deployment.
    @param module: The name of the module to deploy.
    @param config: The module configuration.
    @param instances: The number of instances to deploy.
    @param ha: Whether to deploy the module with HA.
    @param handler: An asynchronous handler to be called once deployment is complete.

    @return: self
    """
    component._component.cluster().deployModule(deployment_id, module, map_to_java(config) if config is not None else None, instances, ha, DeployHandler(handler) if handler is not None else None)
    return self

def deploy_module_to(self, deployment_id, group_id, module, config=None, instances=1, ha=False, handler=None):
    """Deploys a module to a specific HA group.

    Keyword arguments:
    @param deploymen_id: The unique deployment ID of the deployment.
    @param group_id: The name of the group to which to deploy the module.
    @param module: The name of the module to deploy.
    @param config: The module configuration.
    @param instances: The number of instances to deploy.
    @param ha: Whether to deploy the module with HA.
    @param handler: An asynchronous handler to be called once deployment is complete.

    @return: self
    """
    component._component.cluster().deployModuleTo(deployment_id, group_id, module, map_to_java(config) if config is not None else None, instances, ha, DeployHandler(handler) if handler is not None else None)
    return self

def deploy_verticle(self, deployment_id, main, config=None, instances=1, ha=False, handler=None):
    """Deploys a verticle.

    Keyword arguments:
    @param deploymen_id: The unique deployment ID of the deployment.
    @param module: The verticle main.
    @param config: The verticle configuration.
    @param instances: The number of instances to deploy.
    @param ha: Whether to deploy the verticle with HA.
    @param handler: An asynchronous handler to be called once deployment is complete.

    @return: self
    """
    component._component.cluster().deployVerticle(deployment_id, main, map_to_java(config) if config is not None else None, instances, ha, DeployHandler(handler) if handler is not None else None)
    return self

def deploy_verticle_to(self, deployment_id, group_id, main, config=None, instances=1, ha=False, handler=None):
    """Deploys a verticle to a specific HA group.

    Keyword arguments:
    @param deploymen_id: The unique deployment ID of the deployment.
    @param group_id: The name of the group to which to deploy the verticle.
    @param main: The verticle main.
    @param config: The verticle configuration.
    @param instances: The number of instances to deploy.
    @param ha: Whether to deploy the verticle with HA.
    @param handler: An asynchronous handler to be called once deployment is complete.

    @return: self
    """
    component._component.cluster().deployVerticleTo(deployment_id, group_id, main, map_to_java(config) if config is not None else None, instances, ha, DeployHandler(handler) if handler is not None else None)
    return self

def deploy_worker_verticle(self, deployment_id, main, config=None, instances=1, multi_threaded=False, ha=False, handler=None):
    """Deploys a verticle.

    Keyword arguments:
    @param deploymen_id: The unique deployment ID of the deployment.
    @param module: The verticle main.
    @param config: The verticle configuration.
    @param instances: The number of instances to deploy.
    @param multi_threaded: Whether the worker verticle is multi-threaded.
    @param ha: Whether to deploy the verticle with HA.
    @param handler: An asynchronous handler to be called once deployment is complete.

    @return: self
    """
    component._component.cluster().deployWorkerVerticle(deployment_id, main, map_to_java(config) if config is not None else None, instances, multi_threaded, ha, DeployHandler(handler) if handler is not None else None)
    return self

def deploy_worker_verticle_to(self, deployment_id, group_id, main, config=None, instances=1, multi_threaded=False, ha=False, handler=None):
    """Deploys a worker verticle to a specific HA group.

    Keyword arguments:
    @param deploymen_id: The unique deployment ID of the deployment.
    @param group_id: The name of the group to which to deploy the verticle.
    @param main: The verticle main.
    @param config: The verticle configuration.
    @param instances: The number of instances to deploy.
    @param multi_threaded: Whether the worker verticle is multi-threaded.
    @param ha: Whether to deploy the verticle with HA.
    @param handler: An asynchronous handler to be called once deployment is complete.

    @return: self
    """
    component._component.cluster().deployWorkerVerticleTo(deployment_id, group_id, main, map_to_java(config) if config is not None else None, instances, multi_threaded, ha, DeployHandler(handler) if handler is not None else None)
    return self

def undeploy_module(self, deployment_id, handler=None):
    """Undeploys a module.

    Keyword arguments:
    @param deployment_id: The unique deployment ID of the deployment to undeploy.
    @param handler: An asynchronous handler to be called once complete.

    @return: self
    """
    component._component.cluster().undeployModule(deployment_id, UndeployHandler(handler) if handler is not None else None)
    return self

def undeploy_verticle(self, deployment_id, handler=None):
    """Undeploys a verticle.

    Keyword arguments:
    @param deployment_id: The unique deployment ID of the deployment to undeploy.
    @param handler: An asynchronous handler to be called once complete.

    @return: self
    """
    component._component.cluster().undeployVerticle(deployment_id, UndeployHandler(handler) if handler is not None else None)
    return self

class DeployHandler(org.vertx.java.core.AsyncResultHandler):
    def __init__(self, handler):
        self.handler = handler
    def handle(self, result):
        if result.failed():
            self.handler(result.cause(), None)
        else:
            self.handler(None, result.result())

class UndeployHandler(org.vertx.java.core.AsyncResultHandler):
    def __init__(self, handler):
        self.handler = handler
    def handle(self, result):
        if result.failed():
            self.handler(result.cause())
        else:
            self.handler(None)
