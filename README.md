Vert.igo Python API
===================

Vertigo is a fast, reliable, fault-tolerant event processing framework built on
the [Vert.x](http://vertx.io/) application platform. Combining concepts of
cutting-edge [real-time systems](http://storm.incubator.apache.org/) and
[flow-based programming](http://en.wikipedia.org/wiki/Flow-based_programming),
Vertigo allows real-time problems to be broken down into smaller tasks (as
Vert.x verticles) and distributed across a Vert.x cluster. Vertigo provides
fault-tolerance for data streams and components, allowing developers to spend more
time focusing on application code.

For an in-depth look at the concepts underlying Vertigo, check out
[how it works](#how-it-works).

# Python User Manual
1. [Introduction](#introduction)
1. [Setup](#setup)
   * [Adding Vertigo as a Maven dependency](#adding-vertigo-as-a-maven-dependency)
   * [Including Vertigo in a Vert.x module](#including-vertigo-in-a-vertx-module)
1. [Networks](#networks)
   * [Creating a new network](#creating-a-new-network)
   * [Adding components to a network](#adding-components-to-a-network)
   * [Creating connections between components](#)
   * [Routing messages between multiple component instances](#routing-messages-between-multiple-component-instances)
   * [Creating networks from JSON](#creating-networks-from-json)
1. [Deployment](#deployment)
   * [Deploying a network](#deploying-a-network)
   * [Undeploying a network](#undeploying-a-network)
   * [Reconfiguring a network](#reconfiguring-a-network)
   * [Deploying a bare network](#deploying-a-bare-network)
   * [Working with active networks](#working-with-active-networks)
   * [Deploying networks from the command line](#deploying-networks-from-the-command-line)
1. [Clustering](#clustering)
   * [Configuring cluster scopes](#configuring-cluster-scopes)
1. [Components](#components)
   * [Creating a component](#creating-a-component)
   * [The elements of a Vertigo component](#the-elements-of-a-vertigo-component)
1. [Messaging](#messaging)
   * [Sending messages on an output port](#sending-messages-on-an-output-port)
   * [Receiving messages on an input port](#receiving-messages-on-an-input-port)
   * [Working with message groups](#working-with-message-groups)
1. [How it works](#how-it-works)
   * [How Vertigo handles messaging](#how-vertigo-handles-messaging)
   * [How Vertigo performs deployments](#how-vertigo-performs-deployments)
   * [How Vertigo coordinates networks](#how-vertigo-coordinates-networks)

## Introduction
Vertigo is a multi-step event processing framework built on Vert.x. It exposes a
very simple yet powerful API defines networks of Vert.x verticles and the relationships
between them in a manner that abstracts communication details from implementations, making
Vertigo components reusable. It provides for advanced messaging requirements such as
strong ordering and exactly-once processing and supports deployment of networks within a
single Vert.x instance or across a cluster of Vert.x instances and performs setup and
coordination internally.

## Setup
To use Vertigo simply add the library as a Maven dependency or as a Vert.x module include.

### Adding Vertigo as a Maven dependency

```
<dependency>
  <groupId>net.kuujo</groupId>
  <artifactId>vertigo</artifactId>
  <version>0.7.0-SNAPSHOT</version>
</dependency>
```

### Including Vertigo in a Vert.x module

To use the Vertigo Java API, you can include the Vertigo module in your module's
`mod.json` file. This will make Vertigo classes available within your module.

```
{
  "main": "com.mycompany.myproject.MyVerticle",
  "includes": "net.kuujo~vertigo~0.7.0-SNAPSHOT"
}
```

## Networks
Vertigo networks are collections of Vert.x verticles and modules that are connected
together by the Vert.x event bus. Networks and the relationships therein are defined
externally to their components, promoting reusability.

### Creating a network
To create a new network, create a new `Vertigo` instance and call the `createNetwork` method.

```python
import vertigo

network = vertigo.create_network('my-network')
```

All Vertigo networks have an explicit, unique name. This name is very important to
Vertigo as it can be used to reference networks from anywhere within a Vert.x cluster,
but more on that later.

### Adding components to a network
To add a component to the network, use one of the `add_verticle` or `add_module` methods.

```python
network.add_verticle(name='foo', main='foo.js')
```

The `addVerticle` and `addModule` methods each accept a component name, module or
main, configuration, and number of instances.

Just as with networks, Vertigo components are explicitly named. The component name
*must be unique within the network to which the component belongs*.

The network configuration API also exposes an abstract `addComponent` method which detects
whether the added component is a module or a verticle based on module naming conventions.

Once a component has been added to the network, the component configuration will
be returned. Users can set additional options on the component configuration. The
most important of these options is the `group` option. When deploying networks within
a Vert.x cluster, the `group` indicates the HA group to which to deploy the module or verticle.

### Creating connections between components
A set of components is not a network until connections are created between those
components. Vertigo uses a concept of *ports* to abstract input and output from
each component instance. When creating connections between components, you must
specify a component and port to which the connection connects. Each connection
binds one component's output port with another component's input port.

To create a connectoin between two components use the `createConnection` method.

```python
network.create_connection(('foo', 'out'), ('bar', 'in'))
```

The arguments to the `createConnection` method are, in order:
* A two-tuple indicating the source component's name and output port
* A two-tuple indicating the target component's name and input port

You may wonder why components and ports are specified by strings rather than
objects. Vertigo supports reconfiguring live networks with partial configurations,
so objects may not necessarily be available within the network configuration
when a partial configuration is created. More on partial network deployment
and runtime configuration changes in the [deployment](#deployment) section.

### Routing messages between multiple component instances
Just as with Vert.x verticles and modules, each Vertigo component can support
any number of instances. But connections are created between components and
not component instances. This means that a single connection can reference
multiple instances of each component. By default, the Vert.x event bus routes
messages to event bus handlers in a round-robin fashion. But Vertigo provides
additional routing methods known as *selectors*. Selectors indicate how messages
should be routed between multiple instances of a component.

Vertigo provides several selector types by default and supports custom selectors
as well.

* Round robin selector - selects targets in a round-robin fashion
* Random selector - selects a random target to which to send each message
* Hash selector - uses a simple mod hash algorithm to select a target for each message
* Fair selector - selects the target with the least number of messages in the queue
* All selector - sends each message to all target instances

The `ConnectionConfig` API provides several methods for setting selectors
on a connection.
* `round_select()` - sets a round-robin selector on the connection
* `random_select()` - sets a random selector on the connection
* `hash_select()` - sets a mod hash based selector on the connection
* `fair_select()` - sets a fair selector on the connection
* `all_select()` - sets an all selector on the connection

### Creating networks from JSON
Vertigo supports creating networks from json configurations. To create a network
from json call the `Vertigo.createNetwork(JsonObject)` method.

```python
network = vertigo.create_network({'name': 'test-network'})
```


The JSON configuration format is as follows:

* `name` - the network name
* `cluster` - the network's cluster configuration
   * `address` - the event bus address to the cluster manager. This only applies
     to networks with a `cluster` scope
   * `scope` - the network's cluster scope, e.g. `local` or `cluster` See [configuring cluster scopes](#configuring-cluster-scopes)
* `components` - an object of network components, keyed by component names
   * `name` - the component name
   * `type` - the component type, either `module` or `verticle`
   * `main` - the verticle main (if the component is a verticle)
   * `module` - the module name (if the component is a module)
   * `config` - the module or verticle configuration
   * `instances` - the number of component instances
   * `group` - the component deployment group (Vert.x HA group for clustering)
   * `storage` - an object defining the component data storage facility
      * `type` - the component data storage type. This is a fully qualified `DataStore` class name
      * `...` - additional data store configuration options
* `connections` - an array of network connections
   * `source` - an object defining the connection source
      * `component` - the source component name
      * `port` - the source component's output port
   * `target` - an object defining the connection target
      * `component` - the target component name
      * `port` - the target component's input port
   * `selector`- an object defining the connection selector
      * `type` - the selector type, e.g. `round-robin`, `random`, `hash`, `fair`, `all`, or `custom`
      * `selector` - for custom selectors, the selector class
      * `...` - additional selector options

For example...

```
{
  "name": "my-network",
  "cluster": {
    "scope": "local"
  },
  "components": {
    "foo": {
      "name": "foo",
      "type": "verticle",
      "main": "foo.js",
      "config": {
        "foo": "bar"
      },
      "instances": 2
    },
    "bar": {
      "name": "bar",
      "type": "module",
      "module": "com.foo~bar~1.0",
      "instances": 4
    }
  },
  "connections": [
    {
      "source": {
        "component": "foo",
        "port": "out"
      },
      "target": {
        "component": "bar",
        "port": "in"
      },
      "selector": {
        "type": "fair"
      }
    }
  ]
}
```

## Deployment
One of the most important tasks of Vertigo is to support deployment and startup
of networks in a consistent and reliable manner. Vertigo supports network deployment
either within a single Vert.x instance (local) or across a cluster of Vert.x instances.
When a Vertigo network is deployed, a special verticle known as the *network manager*
is deployed. The network manager is tasked with managing and monitoring components
within the network, handling runtime configuration changes, and coordinating startup
and shutdown of networks.

Networks can be deployed and configured from any verticle within any node in a Vert.x
cluster. Even if a network is deployed from another verticle, the network can still be
referenced and updated from anywhere in the cluster. Vertigo's internal coordination
mechanisms ensure consistency for deployments across all nodes in a cluster.

For more information on network deployment and coordination see [how it works](#how-it-works)

### Deploying a network
To deploy a network, simply use the `deploy_network` method.

```python
network = vertigo.create_network('test')
network.add_verticle('foo', main='foo.js', instances=2)
network.add_verticle('bar', main='bar.py', instances=4)

vertigo.deploy_network(network)
```

When Vertigo deploys the network, it will automatically detect the current Vert.x
cluster scope. If the current Vert.x instance is a Hazelcast clustered instance,
Vertigo will attempt to deploy the network across the cluster. This behavior can
be configured in the network's configuration.

If the current Vert.x instance is not clustered then all network deployment will
automatically fall back to the Vert.x `Container`. Even if a network is configured
to be deployed locally, Vertigo will still coordinate using Hazelcast if it's
available.

Note that in order to support remote component deployment you must use a
[Xync](http://github.com/kuujo/xync) node or some other facility that supports
event bus deployments.

### Undeploying a network
To undeploy a network, use the `undeploy_network` method.

```python
def undeploy_handler(error=None):
  if not error:
    print "Successfully undeployed network"

vertigo.undeploy_network('test', handler=undeploy_handler)
```

Passing a string network name to the method will cause the entire network to
be undeployed. The method also supports a network configuration which can be
used to undeploy portions of the network without undeploying the entire network.
More on that in a minute.

### Reconfiguring a network
Vertigo networks can be reconfigured even after deployment. This is where network
names become particularly important. When a user deploys a network, Vertigo first
determines whether the network is already deployed within the current Vertigo cluster.
If a network with the same name is already deployed, *the given network configuration
will be merged with the existing network configuration* and Vertigo will update
components and connections within the network rather than deploying a new network.
This means that Vertigo networks can be deployed one component or connection at
a time.

```python
# Create and deploy a two component network
network = vertigo.create_network('test')
network.add_verticle('foo', main='foo.js', instances=2)
network.add_verticle('bar', main='bar.py', instances=4)

def deploy_handler(error, network):
  # Create and deploy a connection between the two components
  network = vertigo.create_network('test') # Note the same network name
  network.create_connection(('foo', 'out'), ('bar', 'in'))
  vertigo.deploy_network(network)

vertigo.deploy_network(network, handler=deploy_handler)
```

### Deploying a bare network
Since networks can be reconfigured *after* deployment, Vertigo provides a simple
helper method for deploying empty networks that will be reconfigured after deployment.
To deploy an empty network simply deploy a string network name.

```python
vertigo.deploy_network('test')
```

Note that this method can also be used to reference an existing network and retrieve
an `ActiveNetwork` instance (more on active networks below):

```python
def deploy_handler(error, network):
  pass # 'network' is an active network

vertigo.deploy_network('test', handler=deploy_handler)
```

### Working with active networks
Vertigo provides a helper API for reconfiguring netowrks known as *active networks*.
The `ActiveNetwork` is a `NetworkConfig` like object that exposes methods that directly
update the running network when called. Obviously, the name is taken from the active
record pattern.

When deploying any network an `ActiveNetwork` instance for the deployed network will
be returned once the deployment is complete.

```python
def deploy_handler(error, network):
  # Add a component and connection to the running network.
  network.add_verticle('bar', main='bar.py', instances=4)
  network.create_connection(('foo', 'out'), ('bar', 'in'))

network = vertigo.create_network('test')
network.add_verticle('foo', main='foo.js', instances=2)

vertigo.deploy_network(network, handler=deploy_handler)
```

The active network instance contains a reference to the *entire* network configuration,
even if the configuration that was deployed was only a partial network configuration.

### Deploying networks from the command line
Vertigo provides a special facility for deploying networks from json confguration files.
This feature is implemented as a Vert.x language module, so the network deployer must
be first added to your `langs.properties` file.

```
network=net.kuujo~vertigo-deployer~0.7.0:net.kuujo.vertigo.NetworkFactory
.network=network
```

You can replace the given extension with anything that works for you. Once the language
module has been configured, simply run a network configuration file like any other
Vert.x verticle.

```
vertx run my_network.network
```

The `NetworkFactory` will construct the network from the json configuration file and
deploy the network to the available cluster.

## Clustering
Vertigo currently provides two different clustering methods. When networks are deployed,
Vertigo will automatically detect the current Vert.x cluster type and adjust its behavior
based on available features. The available cluster scopes are as follows:
* `local` - *Vert.x is not clustered*. Vertigo will use Vert.x `SharedData` for coordination
  of networks and deployments will be performed via the Vert.x `Container`.
* `cluster` - *Vert.x is clustered using the default `HazelcastClusterManager`*. Vertigo will
  coordinate networks through Hazelcast and, for network confgured for the `cluster` scope,
  will attempt to deploy components remotely over the event bus.

For more information on Vertigo clustering see [how Vertigo coordinates networks](#how-vertigo-coordinates-networks)

### Configuring cluster scopes
Users can optionally configure the cluster scope for individual Vertigo networks.
To configure the cluster scope for a network simply use the `setScope` method on the
network configuration.

```python
network = vertigo.create_network('test')
network.scope = 'local'
```

The network scope defaults to `cluster` which is considered the highest level scope.
If the current Vert.x is not a clustered Vert.x instance, the cluster scope will
automatically fall back to `local`. This allows for networks to be easily tested
in a single Vert.x instance.

It's important to note that while configuring the cluster scope on a network will
cause the network to be *deployed* in that scope, the network's scope configuration
*does not impact Vertigo's synchronization*. In other words, even if a network is
deployed locally, if the current Vert.x instance is a cluster member, Vertigo will still
use Hazelcast to coordinate networks. This allows locally deployed networks
to be referenced and reconfigured even outside of the instance in which it was deployed.
For instance, users can deploy one component of the `foo` network locally in one Vert.x
instance and deploy a separate component of the `foo` network locally in another Vert.x
instance and both components will still become a part of the same network event though
the network is `local`.

## Components
Components are "black box" Vert.x verticles that communicate with other components within
the same network through named *input* and *output* ports.

For detailed information on component startup and coordination see
[how Vertigo coordinates networks](#how-vertigo-coordinates-networks)

### Creating a component
Components use the `vertigo.component` module.

```python
from vertigo import component
```

In Javascript components, it's important that you always register a start handler
by calling the `start_handler` method. Once the component has completed startup
this function will be called.

```python
from vertigo import component

@component.start_handler
def start_handler(error=None):
  if not error:
    print "Component started successfully!"
```

### The elements of a Vertigo component
Each Java component has several additional fields:
* `cluster` - the Vertigo `Cluster` to which the component belongs
* `input` - the component's `InputCollector`, an interface to input ports
* `output`- the component's `OutputCollector`, an interface to output ports
* `logger` - the component's `PortLogger`, a special logger that logs messages to output ports

## Messaging
The Vertigo messaging API is simply a wrapper around the Vert.x event bus.
Vertigo messages are not sent through any central router. Rather, Vertigo uses
network configurations to create direct event bus connections between components.
Vertigo components send and receive messages using only output and input *ports*
and are hidden from event bus address details which are defined in network configurations.
This is the element that makes Vertigo components reusable.

Vertigo messages are guaranteed to arrive in order. Vertigo also provides an API
that allows for logical grouping and ordering of collections of messages known as
[groups](#working-with-message-groups). Groups are strongly ordered named batches
of messages that can be nested.

### Sending messages on an output port
To reference an output port, use the `output.port(name)` method.

```python
from vertigo import output

port = output.port('out')
```

If the referenced output port is not defined in the network configuration, the
port will be lazily created, though it will not actually reference any connections.

Any message that can be sent on the Vert.x event bus can be sent on the output port.
To send a message on the event bus, simply call the `send` method.

```python
output.port('out').send("Hello world!")
```

Internally, Vertigo will route the message to any connections as defined in the
network configuration.

### Receiving messages on an input port
Input ports are referenced in the same was as output ports.

```python
from vertigo import input

port = input.port('in')
```

To receive messages on an input port, register a message handler on the port.

```python
from vertigo import input, output

port = input.port('in')

@port.message_handler
def message_handler(message):
  output.port('out').send(message)
```

Note that Vertigo messages arrive in plain format and not in any sort of `Message`
wrapper. This is because Vertigo messages are inherently uni-directional, and message
acking is handled internally.

### Working with message groups
Vertigo provides a mechanism for logically grouping messages appropriately
named *groups*. Groups are logical collections of messsages that are strongly
ordered by name. Before any given group can stat, each of the groups of the same
name at the same level that preceeded it must have been completed. Additionally,
messages within a group are *guaranteed to be delivered to the same instance* of each
target component. In other words, routing is performed per-group rather than per-message.

When a new output group is created, Vertigo will await the completion of all groups
of the same name that were created prior to the new group before sending the new group's
messages.

```python
def group_handler(group):
  group.send('foo').send('bar').send('baz').end()

output.port('out').group('foo', handler=group_handler)
```

Note that the group's `end()` method *must* be called in order to indicate completion of
the group. Groups are fully asynchronous, meaning they support asynchronous calls to other
APIs, and this step is crucial to that functionality.

```python
def group_handler(group):
  def callback(result):
    group.send(result).end()
  some_async_api(callback)

output.port('out').group('foo', handler=group_handler)
```

The `OutputGroup` API exposes the same methods as the `OutputPort`. That means that groups
can be nested and Vertigo will still guarantee ordering across groups.

```javascript
output.port('out').group('foo', function(group) {
  group.group('bar', function(group) {
    group.send(1).send(2).send(3).end();
  });
  group.group('baz', function(group) {
    group.send(1).send(2).send(3).end();
  });
  group.end();
});
```

As with receiving messages, to receive message groups register a handler on an
input port using the `group_handler` method, passing a group name as the first
argument.

```python
port = input.port('in')

@port.group_handler('foo')
def group_handler(group):
  @group.message_handler
  def message_handler(message):
    output.port('out').send(message)
```

The `InputGroup` API also supports a `start_handler` and `end_handler`. The `end_handler`
can be particularly useful for aggregations. Vertigo guarantees that if a group's
`end_handler` is called then *all* of the messages sent for that group were received
by that group.

```python
port = input.port('in')

@port.group_handler('foo')
def group_handler(group):
  messages = []

  @group.message_handler
  def message_handler(message):
    messages.append(message)

  @group.end_handler
  def end_handler():
    print "Received %s messages in group" % (len(messages),)
```

As with output groups, input groups can be nested, representing the same structure
sent by an output group.

```python
port = input.port('in')

@port.group_handler('foo')
def foo_handler(group):

  @group.group_handler('bar')
  def bar_handler(group):
    @group.message_handler
    def message_handler(message):
      output.port('out').send(message)

  @group.group_handler('baz')
  def baz_handler(group):
    @group.message_handler
    def message_handler(message):
      output.port('out').send(message)
```

## Logging
Ecah Vertigo component contains a special *port logger* which logs messages
to component output ports in addition to standard Vert.x log files. This allows
other components to listen for log messages on input ports.

The port logger logs to ports named for each logger method:
* `fatal`
* `error`
* `warn`
* `info`
* `debug`
* `trace`

### Logging messages to output ports
The port logger simply exposes the standard Vert.x logger interface.
So, to log a message to an output port simply call the appropriate log method:

```python
from vertigo import component, logger

@component.start_handler
def start_handler(error=None):
  if not error:
    logger.info("Component started successfully!")
```

### Reading log messages
To listen for log messages from a component, simply add a connection to a network
configuration listening on the necessary output port. For instance, you could
aggregate and count log messages from one component by connecting each log port to
a single input port on another component.

```python
import vertigo

network = vertigo.create_network('log-test')
network.add_verticle('logger', main='logger.js', instances=2)
network.add_verticle('log-reader', 'log_reader.py', instances=2)
network.create_connection(('logger', 'fatal'), ('log-reader', 'log'), selector='hash')
network.create_connection(('logger', 'error'), ('log-reader', 'log'), selector='hash')
network.create_connection(('logger', 'warn'), ('log-reader', 'log'), selector='hash')
network.create_connection(('logger', 'info'), ('log-reader', 'log'), selector='hash')
network.create_connection(('logger', 'debug'), ('log-reader', 'log'), selector='hash')
network.create_connection(('logger', 'trace'), ('log-reader', 'log'), selector='hash')
```

With a hash selector on each connection, we guarantee that the same log message
will always go to the same `log-reader` instance.

Log messages will arrive as simple strings:

```python
from vertigo import input, output

counts = {}

@input.message_handler('log')
def log_message_handler(message):
  if message not in counts:
    counts[message] = 0
  counts[message] += 1
  output.send('count', counts[message])
```

## How it works
This section is a more in-depth examination of how Vertigo deploys and manages
networks and the communication between them. It is written with the intention
of assisting users in making practical decisions when working with Vertigo.

### How Vertigo handles messaging
All Vertigo messaging is done over the Vert.x event bus. Vertigo messaging is
designed to provide guaranteed ordering and exactly-once processing semantics.
Internally, Vertigo uses *streams* to model connections between an output port
on one set of component instances and an input port on another set of component
instances. Each output port can contain any number of output streams, and each
output stream can contain any number of output connections (equal to the number
of instances of the target component). Connections represent a single event bus
address connection between two instances of two components on a single Vertigo
connection. Connection selectors are used at the stream level to select a set
of connections to which to send each message for the stream.

(See `net.kuujo.vertigo.io`)

Vertigo ensures exactly-once semantics by batching messages for each connection.
Each message that is sent on a single output connection will be tagged with a
monotonically increasing ID for that connection. The input connection that receives
messages from the specific output connection will keep track of the last seen
monotonically increasing ID for the connection. When a new message is received,
the input connection checks to ensure that it is the next message in the sequence
according to its ID. If a message is received out of order, the input connection
immediately sends a message to the output connection indicating the last sequential
ID that it received. The output connection will then begin resending messages from
that point. Even if a message is not received out of order, input connections will
periodically send a message to their corresponding output connection notifying it
of the last message received. This essentially acts as a *ack* for a batch of
messages and allows the output connection to clear its output queue.

In the future, this batching algorithm will be the basis for state persistence.
By coordinating batches between multiple input connections, components can
checkpoint their state after each batch and notify data sources that it's safe
to clear persisted messages.

### How Vertigo performs deployments
Vertigo provides two mechanisms for deployment - local and cluster. The *local*
deployment method simply uses the Vert.x `Container` for deployments. However, Vertigo's
internal deployment API is designed in such a way that each deployment is *assigned*
a unique ID rather than using Vert.x's internal deployment IDs. This allows Vertigo
to reference and evaluate deployments after failures. In the case of local deployments,
deployment information is stored in Vert.x's `SharedData` structures.

Vertigo also supports clustered deployments using Xync. Xync exposes user-defined
deployment IDs in its own API.

(See `net.kuujo.vertigo.cluster.Cluster` and `net.kuujo.vertigo.cluster.ClusterManager`)

When Vertigo begins deploying a network, it first determines the current cluster scope.
If the current Vert.x instance is a Hazelcast clustered instance, Vertigo will perform
all coordination through the Hazelcast cluster. Once the cluster scope is determined,
Vertigo will check the cluster's shard data structures to determine whether the network
is already deployed. If the network is already deployed then Vertigo will load the
network's cluster scope - which may differ from the actual cluster scope - and deploy
the network's manager. Actual component deployments are performed by the manager.
For more information on the network manager and coordination see
[how vertigo coordinates networks](#how-vertigo-coordinates-networks).

### How Vertigo coordinates networks
Vertigo uses a very unique and flexible system for coordinating network deployment,
startup, and configuration. The Vertigo coordination system is built on a distributed
observer implementation. Vertigo will always use the highest cluster scope available
for coordination. That is, if the current Vert.x cluster is a Hazelcast cluster then Vertigo
will use Hazelcast for coordination. This ensures that Vertigo can coordinate
all networks within a cluster, even if they are deployed as local networks.

The distributed observer pattern is implemented as map events for both Vert.x `SharedData`
and Hazelcast-based maps. Events for any given key in a Vertigo cluster can be
watched by simply registering an event bus address to which to send events. The Vertigo
`NetworkManager` and components both use this mechanism for coordination with one another.

(See `net.kuujo.vertigo.data.WatchableAsyncMap`)

The `NetworkManager` is a special verticle that is tasked with starting, configuring,
and stopping a single network and its components. When a network is deployed, Vertigo
simply deploys a network manager and sets the network configuration in the cluster. The
network manager completes the rest of the process.

When the network manager first starts up, it registers to receive events for the
network's configuration key in the cluster. Once the key has been set, the manager will
be notified of the configuration change through the event system, load the network
configuration, and deploy the necessary components.

(See `net.kuujo.vertigo.network.manager.NetworkManager`)

This is the mechanism that makes live network configurations possible in Vertigo.
Since the network manager already receives notifications of configuration changes for
the network, all we need to do is set the network's configuration key to a new configuration
and the network will be automatically notified and updated asynchronously.

But deployment is only one part of the equation. Often times network reconfigurations
may consist only of new connections between components. For this reason, each Vertigo
component also watches its own configuration key in the cluster. When the network
configuration changes, the network manager will update each component's key in the
cluster, causing running components to be notified of their new configurations.
Whenever such a configuration is detected by a component, the component will automatically
update its internal input and output connections asynchronously.

(See `net.kuujo.vertigo.component.ComponentCoordinator`)

Finally, cluster keys are used to coordinate startup, pausing, resuming, and shutdown
of all components within a network. When a component is deployed and completes setting
up its input and output connections, it will set a special status key in the cluster.
The network manager watches status keys for each component in the network. Once the
status keys have been set for all components in the cluster, the network will be
considered ready to start. The network manager will then set a special network-wide
status key which each component in turn watches. Once the components see the network
status key has been set they will finish startup and call the `start()` method.

During configuration changes, the network manager will unset the network-wide status
key, causing components to optionally pause during the configuration change.

It's important to note that each of these updates is essentially atomic. The network
manager, components, and connections each use internal queues to enqueue and process
updates atomically in the order in which they occur. This has practically no impact on
performance since configuration changes should be rare and it ensures that rapid configuration
changes (through an `ActiveNetwork` object for instance) do not cause race conditions.

One of the most important properties of this coordination system is that it is completely
fault-tolerant. Since configurations are stored in the cluster, even if a component fails
it can reload its last existing configuration from the cluster once failover occurs.
If the network manager fails, the rest of the network can continue to run as normal.
Only configuration changes will be unavailable. Once the manager comes back online, it
will fetch the last known configuration for the network and continue normal operation.

**Need support? Check out the [Vertigo Google Group][google-group]**

**[Java API](https://github.com/kuujo/vertigo)**
**[Javascript API](https://github.com/kuujo/vertigo-js) is under development**

[google-group]: https://groups.google.com/forum/#!forum/vertx-vertigo
