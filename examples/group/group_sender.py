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
from vertigo import component

port = component.output.out

@port.group('sentences')
def sentences_handler(group):

    sentences = [
        'Oak is strong and also gives shade',
        'Cats and dogs each hate the other',
        'The pipe began to rust while new',
        'Open the crate but don\'t break the glass',
        'Add the sum to the product of these three',
    ]

    # Loop through sentences and create groups of words.
    for sentence in sentences:
        # Create a new 'words' group for the sentence's words.
        @group.group('words')
        def words_handler(group):
            words = sentence.split(' ')
            for word in sentence.split(' '):
                group.send(word)
            group.end() # End the words group
    group.end() # End the sentences group
