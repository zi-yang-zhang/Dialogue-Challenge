PATIENT_RECORD_NOT_FOUND = 'PRE1'
PATIENT_RECORD_EMAIL_DUPLICATE = 'PRE2'
PATIENT_RECORD_PAGE_NOT_FOUND = 'PRE3'


class Error(object):
    def __init__(self, req_id='', status=None, title='', detail='', code='', source=None):
        self.id = req_id
        self.status = status
        self.title = title
        self.detail = detail
        self.code = code
        self.source = source

    def __str__(self):
        return "Error:{id:{!r}, status:{!r}, title:{!r}, detail:{!r}, code:{!r}, source:{!r}".format(self.id,
                                                                                                     self.status,
                                                                                                     self.title, self.detail,
                                                                                                     self.code, self.source)

    @property
    def to_json(self):
        return {
            'id': self.id,
            'status': str(self.status),
            'title': self.title,
            'detail': self.detail,
            'code': self.code,
            'source': self.source
        }

    @classmethod
    def create_not_found_exception(cls):
        return cls(status=404, title='Not Found', detail='Page not found')
