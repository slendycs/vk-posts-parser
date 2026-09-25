class VKError(Exception):
    def __init__(self, error_msg):
        self.error_msg = error_msg

    def __str__(self):
        return f'Some error from VK servers: {self.error_msg}'
    
class APICallError(Exception):
    def __init__(self, error_msg, method):
        self.error_msg = str(error_msg)
        self.method = method

    def __str__(self):
        return f'Failed to execute request to method "{self.method}": {self.error_msg}'

class NoItemsError(Exception):
    def __init__(self, error_msg, domain):
        self.domain = domain
        self.error_msg = error_msg
    
    def __str__(self):
        return f'No post items for domain "{self.domain}": {self.error_msg}'