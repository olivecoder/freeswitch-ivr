import pycurl
import urllib
import StringIO

class Client(object):
    def __init__(self, useragent = 'Simple Client HTTP v0.1', debug=False):
        self.http_useragent = useragent
        self.debug = debug

    def http_req(self, url, post_data=None, digest_user=None, digest_pass=None, output_file_name=None, method_put=False):
        """retrieve information by http protocol, using GET, POST, PUT methods"""
        http_error = None
        http_code = 0
        if output_file_name:
            http_output = open(output_file_name, "w")
        else:
            http_output = StringIO.StringIO()

        # prepare 
        c = pycurl.Curl()
        c.setopt(pycurl.USERAGENT, self.http_useragent)
        c.setopt(pycurl.URL, url)
        c.setopt(pycurl.WRITEFUNCTION, http_output.write)
        if method_put:
            encoded_attrs = urllib.urlencode(post_data)
            request_buffer = StringIO.StringIO(encoded_attrs)
            c.setopt(pycurl.UPLOAD, 1)
            c.setopt(pycurl.INFILESIZE, len(encoded_attrs))
            c.setopt(pycurl.READFUNCTION, request_buffer.read)
            c.setopt(pycurl.HTTPHEADER,['Expect: 100-continue', 'Content-Type: application/x-www-form-urlencoded'])

        if post_data:
            c.setopt(pycurl.POSTFIELDS, urllib.urlencode(post_data))
        if digest_user and digest_pass:
            c.setopt(pycurl.HTTPAUTH, pycurl.HTTPAUTH_DIGEST)
            c.setopt(pycurl.USERPWD, "%s:%s" % (digest_user, digest_pass))
        if self.debug:
            c.setopt(c.VERBOSE, 1)

        # perform
        try:
            c.perform()
        except pycurl.error, e:
            http_error = e
        http_code = c.getinfo(pycurl.HTTP_CODE)
        http_output.seek(0)
        return http_code, http_output

    def post_with_file(self, url, file_t, data = None, digest_user=None, digest_pass=None, output_file_name=None):
        """ 
            file_t: tuple with (field_name, filename)
            data: other post data info dict
            >>> http_client = Client()
            >>> ret = http_client.post_with_file('http://127.0.0.1:8000/api/comment/', ('audio', 'path/to/filename.wav'), {'arg1':'7', 'arg2':'teste'})
        """
        http_error = None
        http_code = 0
        if output_file_name:
            http_output = open(output_file_name, "w")
        else:
            http_output = StringIO.StringIO()
        post_data = [] 
        file_t = (file_t[0], (pycurl.FORM_FILE, file_t[1]))
        post_data.append(file_t)
        if data:
            post_data += data.items()

        # prepare 
        c = pycurl.Curl()
        c.setopt(pycurl.USERAGENT, self.http_useragent)
        c.setopt(pycurl.URL, url)
        c.setopt(pycurl.WRITEFUNCTION, http_output.write)
        c.setopt(c.POST, 1)
        c.setopt(c.HTTPPOST, post_data) 
        if digest_user and digest_pass:
            c.setopt(pycurl.HTTPAUTH, pycurl.HTTPAUTH_DIGEST)
            c.setopt(pycurl.USERPWD, "%s:%s" % (digest_user, digest_pass))
        if self.debug:
            c.setopt(c.VERBOSE, 1)
        # perform
        try:
            c.perform()
        except pycurl.error, e:
            http_error = e
        http_code = c.getinfo(pycurl.HTTP_CODE)
        http_output.seek(0)
        c.close()
        return http_code, http_output
 
            
if __name__ == '__main__':
    c = Client()
    code, content = c.http_req('http://www.google.com.br/')
    print 'code:', code
    print 'content:', content.read()
