class news:
    news_id = 0
    image_url = ''
    author = ''
    date =''
    title = ''
    summary = ''
    body =''

    def __init__(self,title,body,url):
        self.title = title
        self.body = body

class user:
    name=''
    family=''
    password =''
