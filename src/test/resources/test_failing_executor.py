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
from test import Assert, Test
from vertigo import executor
from vertigo.error import FailureError

@executor.start_handler
def start_handler(error, executor):
    if error is None:
        executor.result_timeout = 15000
        Assert.equals(15000, executor.result_timeout)
        executor.execute_queue_max_size = 500
        Assert.equals(500, executor.execute_queue_max_size)
        executor.auto_retry = True
        Assert.equals(True, executor.auto_retry)
        executor.auto_retry = False
        executor.auto_retry_attempts = 3
        Assert.equals(3, executor.auto_retry_attempts)
        executor.execute_interval = 500
        Assert.equals(500, executor.execute_interval)
        Assert.false(executor.execute_queue_full())

        def result_handler(error, result):
            Assert.not_null(error)
            Assert.true(isinstance(error, FailureError))
            Test.complete()
        executor.execute({'body': 'Hello world!'}, handler=result_handler)
