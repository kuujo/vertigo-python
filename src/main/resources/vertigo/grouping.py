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
import net.kuujo.vertigo.input.grouping.AllGrouping
import net.kuujo.vertigo.input.grouping.RandomGrouping
import net.kuujo.vertigo.input.grouping.RoundGrouping
import net.kuujo.vertigo.input.grouping.FieldsGrouping

class Grouping(object):
  """
  A base grouping.
  """

class AllGrouping(Grouping):
  """
  An all grouping.
  """
  def __init__(self):
    self._grouping = net.kuujo.vertigo.input.grouping.AllGrouping()

class RandomGrouping(Grouping):
  """
  A random grouping.
  """
  def __init__(self):
    self._grouping = net.kuujo.vertigo.input.grouping.RandomGrouping()

class RoundGrouping(Grouping):
  """
  A round-robin grouping.
  """
  def __init__(self):
    self._grouping = net.kuujo.vertigo.input.grouping.RoundGrouping()

class FieldsGrouping(Grouping):
  """
  A fields-based grouping.
  """
  def __init__(self, *fields):
    self._grouping = net.kuujo.vertigo.input.grouping.FieldsGrouping(*fields)
