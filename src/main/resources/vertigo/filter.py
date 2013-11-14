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
import net.kuujo.vertigo.input.filter.FieldFilter
import net.kuujo.vertigo.input.filter.TagsFilter
import net.kuujo.vertigo.input.filter.SourceFilter
from core.javautils import map_from_java, map_to_java

class Filter(object):
  """A base filter."""

class FieldFilter(Filter):
  """A field filter."""
  def __init__(self, field, value):
    self._filter = net.kuujo.vertigo.input.filter.FieldFilter(field, map_to_java(value))

  def get_field(self):
    """The filter field."""
    return self._filter.getField()

  def set_field(self, field):
    """The filter field."""
    self._filter.setField(field)

  field = property(get_field, set_field)

  def get_value(self):
    """The filter field value."""
    return map_from_java(self._filter.getValue())

  def set_value(self, value):
    """The filter field value."""
    self._filter.setValue(map_to_java(value))

  value = property(get_value, set_value)

class TagsFilter(Filter):
  """A tags filter."""
  def __init__(self, *tags):
    self._filter = net.kuujo.vertigo.input.filter.TagsFilter(tags)

  def add_tag(self, tag):
    """Adds a tag to the filter.

    Keyword arguments:
    @param tag: the tag to add.

    @return: self
    """
    self._filter.addTag(tag)
    return self

class SourceFilter(Filter):
  """A message source filter."""
  def __init__(self, source):
    self._filter = net.kuujo.vertigo.input.filter.SourceFilter(source)

  def get_source(self):
    """The filter source."""
    return self._filter.getSource()

  def set_source(self, source):
    """The filter source."""
    self._filter.setSource(source)

  source = property(get_source, set_source)
