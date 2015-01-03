import datetime
import os
from sqlalchemy import func

from plugins.baseplugin import BasePlugin
from plugins.leavemessage.models import Message


class Plugin(BasePlugin):
    name = 'LeaveMessagePlugin'

    def admin_message_queue(self, user, nick, channel, rest):
        """Asks {nick} for the number of undelivered messages."""
        message = "Error loading messages"
        with self.getDbSession() as db_session:
            count = db_session.query(func.count(Message.id)).scalar()
            message = "%d messages pending delivery" % count
        self.reply(channel, nick, message)

    def command_leavemessage(self, user, nick, channel, rest):
        """
        Leaves a message for someone next time they log in or say something.
        Usage: {command_prefix}leavemessage target_nick message
        """

        params = rest.split(' ')
        if len(params) < 2:
            self.reply(
                channel,
                nick,
                self.formatDoc(
                    "Usage: {command_prefix}leavemessage target_nick message"
                )
            )
            return False

        target = params[0]
        message = ' '.join(params[1:])

        with self.getDbSession() as db_session:
            db_session.add(
                Message(
                        user=user,
                        nick=nick,
                        message_time=datetime.datetime.now(),
                        to_nick=target,
                        channel=channel,
                        message=message
                    )
                )

        self.reply(channel, nick, 'Message saved for %s' % target)

    def command_check_messages(self, user, nick, channel, more):
        self._handleMessages(nick, requested=True)

    def onUserJoined(self, user, nick, channel):
        self._handleMessages(nick)

    def onUserRenamed(self, user, old_nick, new_nick):
        self._handleMessages(new_nick)

    def onMessage(self, user, nick, channel, message, *args, **kwargs):
        self._handleMessages(nick)

    def _handleMessages(self, nick, requested=False):
        messages = []
        responses = []
        with self.getDbSession() as db_session:
            messages = (db_session
                    .query(Message)
                    .filter(Message.to_nick==nick)
                )

            for message in messages:
                content = "%s left you a message at %s: %s" % (
                        message.nick,
                        message.message_time.strftime("%Y-%m-%d %H:%M:%S UTC"),
                        message.message
                    )
                responses.append((nick, content))

                # TODO: if send fails, dont delete (requires yaib update)
                db_session.delete(message)

        for to_nick, content in responses:
            self.send(to_nick, content)

        # if user asked for their messages but they have none, tell them
        if requested and len(responses) == 0:
            self.send(
                nick, "There are no messages currently waiting for %s" % nick
            )
