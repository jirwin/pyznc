"""
Config keys - Create a map between WebAdmin form elements and ZNC conf keys.
"""


conf_map = {'Admin': 'isadmin',
            'Allow': 'allowedips',
            'AltNick': 'altnick',
            'AppendTimestamp': 'appendtimestamp',
            'BindHost': None,
            'Buffer': 'bufsize',
            'DCCBindHost': None,
            'DenyLoadMod': 'denyloadmod',
            'DenySetBindHost': 'denysetbindhost',
            'CTCPReply': 'ctcpreplies',
            'ChanModes': 'chanmodes',
            'Ident': 'ident',
            'IRCConnectEnabled': 'doconnect',
            'JoinTries': 'jointries',
            'KeepBuffer': 'keepbuffer',
            'LoadModule': 'loadmod',
            'MaxJoins': 'maxjoins',
            'MultiClients': 'multiclients',
            'Nick': 'nick',
            'PrependTimestamp': 'prependtimestamp',
            'QuitMsg': 'quitmsg',
            'RealName': 'realname',
            'Servers': 'servers',
            'StatusPrefix': 'statusprefix',
            'TimestampFormat': 'timestampformat',
            'TimezoneOffset': 'timezonoffset'}
