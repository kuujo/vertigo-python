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
class Cluster(object):
    """Vertigo cluster."""
    def __init__(self, java_obj):
        self.java_obj = java_obj

    def is_deployed(self, name, handler):
        pass

    def deploy_module(self, deployment_id, module, config=None, instances=1, handler=None):
        pass

    def deploy_verticle(self, deployment_id, main, config=None, instances=1, handler=None):
        pass

    def deploy_worker_verticle(self, deployment_id, main, config=None, instances=1, multi_threaded=False, handler=None):
        pass

    def undeploy_module(self, deployment_id, handler=None):
        pass

    def undeploy_verticle(self, deployment_id, handler=None):
        pass

    def get_map(self, name):
        pass

    def get_list(self, name):
        pass

    def get_set(self, name):
        pass

    def get_queue(self, name):
        pass

    def get_id_generator(self, name):
        pass

    def get_lock(self, name):
        pass
