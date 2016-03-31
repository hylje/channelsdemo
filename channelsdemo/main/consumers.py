from channels import Group

def ws_add_board(message):
    Group("board").add(message.reply_channel)

def ws_add_thread(message, thread_id):
    Group("thread-%s" % thread_id).add(message.reply_channel)

def ws_disconnect_board(message):
    Group("board").discard(message.reply_channel)

def ws_disconnect_thread(message, thread_id):
    Group("thread-%s" % thread_id).discard(message.reply_channel)
