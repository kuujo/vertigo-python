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
import sys, component

__this = sys.modules[__name__]

def fatal(message):
    """Logs a fatal message.

    @param message: The message to log.

    @return: The logger.
    """
    component._component.logger().fatal(message)
    return __this

def error(message):
    """Logs an error message.

    @param message: The message to log.

    @return: The logger.
    """
    component._component.logger().error(message)
    return __this

def warn(message):
    """Logs a warning message.

    @param message: The message to log.

    @return: The logger.
    """
    component._component.logger().warn(message)
    return __this

def info(message):
    """Logs an info message.

    @param message: The message to log.

    @return: The logger.
    """
    component._component.logger().info(message)
    return __this

def debug(message):
    """Logs a debug message.

    @param message: The message to log.

    @return: The logger.
    """
    component._component.logger().debug(message)
    return __this

def trace(message):
    """Logs a trace message.

    @param message: The message to log.

    @return: The logger.
    """
    component._component.logger().trace(message)
    return __this
