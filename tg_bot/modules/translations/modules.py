"""
 - /adminlist | /admins: list of admins in the chat

*Admin only:*
 - /pin: silently pins the message replied to - add 'loud' or 'notify' to give notifs to users.
 - /unpin: unpins the currently pinned message
 - /invitelink: gets invitelink
 - /promote: promotes the user replied to
 - /demote: demotes the user replied to
"""
"""
 - /afk <reason>: mark yourself as AFK.
 - brb <reason>: same as the afk command - but not a command.

When marked as AFK, any mentions will be replied to with a message to say you're not available!
"""
"""
 - /flood: Get the current flood control setting

*Admin only:*
 - /setflood <int/'no'/'off'>: enables or disables flood control
"""
"""
*Admin only:*
 - /antispam <on/off/yes/no>: Will disable antispam security in group, or return your current settings.

Antispam are used by the bot owners to ban spammers across all groups. This helps protect \
you and your groups by removing spam flooders as quickly as possible. They can be disabled for you group by calling \
/antispam
"""
"""
 - /kickme: kicks the user who issued the command

*Admin only:*
 - /ban <userhandle>: bans a user. (via handle, or reply)
 - /tban <userhandle> x(m/h/d): bans a user for x time. (via handle, or reply). m = minutes, h = hours, d = days.
 - /unban <userhandle>: unbans a user. (via handle, or reply)
 - /kick <userhandle>: kicks a user, (via handle, or reply)
"""
"""
Actions are available with connected groups:
 • View and edit notes
 • View and edit filters
 • View and edit blacklists
 • Promote/demote users
 • See adminlist, see invitelink
 • Disable/enable commands in chat
 • Mute/unmute users in chat
 • Restrict/unrestrict users in chat
 • More in future!

 - /connection <chatid>: Connect to remote chat
 - /disconnect: Disconnect from chat
 - /allowconnect on/yes/off/no: Allow connect users to group
"""
"""
 - /filters: list all active filters in this chat.

*Admin only:*
 - /filter <keyword> <reply message>: add a filter to this chat. The bot will now reply that message whenever 'keyword'\
is mentioned. If you reply to a sticker with a keyword, the bot will reply with that sticker. NOTE: all filter \
keywords are in lowercase. If you want your keyword to be a sentence, use quotes. eg: /filter "hey there" How you \
doin?
 - /stop <filter keyword>: stop that filter.
"""
"""
 - /cmds: check the current status of disabled commands

*Admin only:*
 - /enable <cmd name>: enable that command
 - /disable <cmd name>: disable that command
 - /listcmds: list all possible toggleable commands
"""
"""
 - /locktypes: a list of possible locktypes

*Admin only:*
 - /lock <type>: lock items of a certain type (not available in private)
 - /unlock <type>: unlock items of a certain type (not available in private)
 - /locks: the current list of locks in this chat.

Locks can be used to restrict a group's users.
eg:
Locking urls will auto-delete all messages with urls which haven't been whitelisted, locking stickers will delete all \
stickers, etc.
Locking bots will stop non-admins from adding bots to the chat.
"""
"""
*Admin only:*
- /logchannel: get log channel info
- /setlog: set the log channel.
- /unsetlog: unset the log channel.

Setting the log channel is done by:
- adding the bot to the desired channel (as an admin!)
- sending /setlog in the channel
- forwarding the /setlog to the group
"""
"""
 - /id: get the current group id. If used by replying to a message, gets that user's id.
 - /runs: reply a random string from an array of replies.
 - /slap: slap a user, or get slapped if not a reply.
 - /time <place>: gives the local time at the given place.
 - /weather <city>: get weather info in a particular place.
 - /info: get information about a user.
 - /gdpr: deletes your information from the bot's database. Private chats only.
 - /stickerid: reply to a sticker to me to tell you its file ID.
 - /getsticker: reply to a sticker to me to upload its raw PNG file.

 - /markdownhelp: quick summary of how markdown works in telegram - can only be called in private chats.
"""
"""
*Admin only:*
 - /del: deletes the message you replied to
 - /purge: deletes all messages between this and the replied to message.
 - /purge <integer X>: deletes the replied message, and X messages following it.
"""
"""
*Admin only:*
 - /mute <userhandle>: silences a user. Can also be used as a reply, muting the replied to user.
 - /tmute <userhandle> x(m/h/d): mutes a user for x time. (via handle, or reply). m = minutes, h = hours, d = days.
 - /unmute <userhandle>: unmutes a user. Can also be used as a reply, muting the replied to user.
 - /restrict <userhandle>: restricts a user from sending stickers, gif, embed links or media. Can also be used as a reply, restrict the replied to user.
 - /trestrict <userhandle> x(m/h/d): restricts a user for x time. (via handle, or reply). m = minutes, h = hours, d = days.
 - /unrestrict <userhandle>: unrestricts a user from sending stickers, gif, embed links or media. Can also be used as a reply, restrict the replied to user.
"""
"""
 - /get <notename>: get the note with this notename
 - #<notename>: same as /get
 - /notes or /saved: list all saved notes in this chat

If you would like to retrieve the contents of a note without any formatting, use `/get <notename> noformat`. This can \
be useful when updating a current note.

*Admin only:*
 - /save <notename> <notedata>: saves notedata as a note with name notename
A button can be added to a note by using standard markdown link syntax - the link should just be prepended with a \
`buttonurl:` section, as such: `[somelink](buttonurl:example.com)`. Check /markdownhelp for more info.
 - /save <notename>: save the replied message as a note with name notename
 - /clear <notename>: clear note with this name
"""
"""
 - /report <reason>: reply to a message to report it to admins.
 - @admin: reply to a message to report it to admins.
NOTE: neither of these will get triggered if used by admins

*Admin only:*
 - /reports <on/off>: change report setting, or view current status.
   - If done in pm, toggles your status.
   - If in chat, toggles that chat's status.
"""
"""
 - /addrss <link>: add an RSS link to the subscriptions.
 - /removerss <link>: removes the RSS link from the subscriptions.
 - /rss <link>: shows the link's data and the last entry, for testing purposes.
 - /listrss: shows the list of rss feeds that the chat is currently subscribed to.

NOTE: In groups, only admins can add/remove RSS links to the group's subscription
"""
"""
 - /rules: get the rules for this chat.

*Admin only:*
 - /setrules <your rules here>: set the rules for this chat.
 - /clearrules: clear the rules for this chat.
"""
"""
 - s/<text1>/<text2>(/<flag>): Reply to a message with this to perform a sed operation on that message, replacing all \
occurrences of 'text1' with 'text2'. Flags are optional, and currently include 'i' for ignore case, 'g' for global, \
or nothing. Delimiters include `/`, `_`, `|`, and `:`. Text grouping is supported. The resulting message cannot be \
larger than {}.

*Reminder:* Sed uses some special characters to make matching easier, such as these: `+*.?\\`
If you want to use these characters, make sure you escape them!
eg: `\\?`.
"""
"""
 - /setbio <text>: while replying, will save another user's bio
 - /bio: will get your or another user's bio. This cannot be set by yourself.
 - /setme <text>: will set your info
 - /me: will get your or another user's info
"""
"""
 - /warns <userhandle>: get a user's number, and reason, of warnings.
 - /warnlist: list of all current warning filters

*Admin only:*
 - /warn <userhandle>: warn a user. After 3 warns, the user will be banned from the group. Can also be used as a reply.
 - /resetwarn <userhandle>: reset the warnings for a user. Can also be used as a reply.
 - /addwarn <keyword> <reply message>: set a warning filter on a certain keyword. If you want your keyword to \
be a sentence, encompass it with quotes, as such: `/addwarn "very angry" This is an angry user`. 
 - /nowarn <keyword>: stop a warning filter
 - /warnlimit <num>: set the warning limit
 - /strongwarn <on/yes/off/no>: If set to on, exceeding the warn limit will result in a ban. Else, will just kick.
"""

"""
Your group's welcome/goodbye messages can be personalised in multiple ways. If you want the messages \
to be individually generated, like the default welcome message is, you can use *these* variables:
 - `{{first}}`: this represents the user's *first* name
 - `{{last}}`: this represents the user's *last* name. Defaults to *first name* if user has no last name.
 - `{{fullname}}`: this represents the user's *full* name. Defaults to *first name* if user has no last name.
 - `{{username}}`: this represents the user's *username*. Defaults to a *mention* of the user's first name if has no username.
 - `{{mention}}`: this simply *mentions* a user - tagging them with their first name.
 - `{{id}}`: this represents the user's *id*.
 - `{{count}}`: this represents the user's *member number*.
 - `{{chatname}}`: this represents the *current chat name*.
Each variable MUST be surrounded by `{{}}` to be replaced.
Welcome messages also support markdown, so you can make any elements bold/italic/code/links. \
Buttons are also supported, so you can make your welcomes look awesome with some nice intro \
buttons. To create a button linking to your rules, use this: `[Rules](buttonurl://t.me/{}?start=group_id)`. \
Simply replace `group_id` with your group's id, which can be obtained via /id, and you're good to \
go. Note that group ids are usually preceded by a `-` sign; this is required, so please don't \
remove it. \
If you're feeling fun, you can even set images/gifs/videos/voice messages as the welcome message by \
replying to the desired media, and calling /setwelcome.

*Admin only:*
 - /welcome <on/off>: enable/disable welcome messages.
 - /welcome: shows current welcome settings.
 - /welcome noformat: shows current welcome settings, without the formatting - useful to recycle your welcome messages!
 - /goodbye -> same usage and args as /welcome.
 - /setwelcome <sometext>: set a custom welcome message. If used replying to media, uses that media.
 - /setgoodbye <sometext>: set a custom goodbye message. If used replying to media, uses that media.
 - /resetwelcome: reset to the default welcome message.
 - /resetgoodbye: reset to the default goodbye message.
 - /cleanwelcome <on/off>: On new member, try to delete the previous welcome message to avoid spamming the chat.
 - /cleanservice <on/off/yes/no>: deletes all service message; those are the annoying "x joined the group" you see when people join.
 - /welcomesecurity <off/soft/hard>: soft - restrict user's permission to send media files for 24 hours, hard - restict user's permission to send messages until they click on the button \"I'm not a bot\"
"""