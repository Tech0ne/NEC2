##################################
#    ___ _     _          _    
#   / __| |___| |__  __ _| |___
#  | (_ | / _ \ '_ \/ _` | (_-<
#   \___|_\___/_.__/\__,_|_/__/
#                              
##################################

## AUTH METHODS
PASSWORD        = 0
CERTIFICATE     = 1

## MESSAGE ORIGIN
SERVER          = 0
CLIENT          = 1

## PROTOCOL METHODS
# Both side
CLOSE           = b"CLOSE"      # Close connection
ERROR           = b"ERROR"      # An error occured
PING            = b"PING"       # Ask for PING request
PONG            = b"PONG"       # Answer with a PONG response

ANY_SIDE_PROTOCOL_METHOS = [CLOSE, ERROR, PING, PONG]

# Client side

NICK            = b"NICK"       # Set nickname
MSG             = b"MSG"        # Send message to the main ServerChannel
PRIVMSG         = b"PRIVMSG"    # Send private message to someone (provided UserID)
SETINFOS        = b"SETPASS"    # Change password. Send a sha256 of the password, and the server keeps a sha256 of it

CLIENT_SIDE_PROTOCOL_METHODS = [NICK, MSG, PRIVMSG, SETINFOS] + ANY_SIDE_PROTOCOL_METHOS

# Server side

JOIN            = b"JOIN"       # People join
LEAVE           = b"LEAVE"      # People leave
BROADCAST       = b"BROADCAST"  # Receive message on the main ServerChannel
MSGPRIV         = b"MSGPRIV"    # Receive private message

SERVER_SIDE_PROTOCOL_METHODS = [JOIN, LEAVE, BROADCAST, MSGPRIV] + ANY_SIDE_PROTOCOL_METHOS

## ERROR CODES
NICKNAME_TAKEN      = 0
NICKNAME_INVALID    = 1
RSA_ERROR           = 2
KICKED              = 3
