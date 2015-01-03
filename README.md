Yaib LeaveMessage Plugin
=================

A plugin for [yaib](https://github.com/collingreen/yaib) that allows users
to leave messages for each other by nick. If the message recipient joins a
channel or sends a message, Yaib will PM them with all of their pending
messages.

NOTE: This is not a secure system in any way - anyone can get any messages for any
nick.


## Usage:
Leave messages with the `!leavemessage` command.
Example:
~~~
nick1: !leavemessage othernick hey, this is a message when you get back
*nick2 joins the channel*
yaib->nick2: nick left you a message at 2015-01-02 19:48:03 UTC: hey, this is a
message when you get back
~~~

Get your pending messages with `!check_messages`. Admins can check how many
messages are waiting to be delivered with `!message_queue`.


## Setup:
The only thing required is a properly configured persistence module (Yaib comes
configured with a working local sqlite database out of the box - change the
`persistence.connection` string in config.json to change database connections.
Consult the Yaib and SQLAlchemy docs for more info.


## Tables:
This plugin creates one table in the database named `Message` (database tables
in Yaib plugins are namespaced automatically, so it will actually be
`leavemessage_message`). All the pending messages are stored in this table
and will be removed as they are delivered.
