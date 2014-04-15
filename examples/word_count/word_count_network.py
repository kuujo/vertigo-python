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
import vertigo

network = vertigo.create_network('word_count')
network.add_verticle('word_feeder', 'word_count_feeder.py', config={'words': ['apple', 'banana', 'orange']})
network.add_verticle('word_counter', 'word_count_worker.py', instances=2)
network.create_connection(('word_feeder', 'out'), ('word_counter', 'in'), grouping='hash')

def deploy_handler(error, context):
    if error:
        print error.getMessage()

vertigo.deploy_local_network(network, handler=deploy_handler)
