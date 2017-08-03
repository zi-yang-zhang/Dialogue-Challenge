import uuid


class Error(object):
    def __init__(self, status='', title='', detail='', code='', source=None):
        self.id = uuid.uuid4()
        self.status = status
        self.title = title
        self.detail = detail
        self.code = code
        self.source = source

    def __str__(self):
        return "Error:{id:%s, status:%s, title:%s, detail:%s, code:%s, source:%s".format(self.id, self.status,
                                                                                         self.title, self.detail,
                                                                                         self.code, self.source)
