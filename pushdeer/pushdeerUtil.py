import json
from typing import Optional, Union
import requests


class PushDeer:
    server = 'http://192.168.192.36:8801'
    endpoint = '/message/push'
    pushkey = ''
    method = 'get'
    headers = {'Content-Type': 'application/json;charset=utf-8'}

    def __init__(self, server: Optional[str] = None, pushkey: Optional[str] = None, method: Optional[str] = None):
        if server:
            self.server = server
        if pushkey:
            self.pushkey = pushkey
        if method:
            self.method = method

    def _push(self, method: str, text: str, desp: Optional[str] = None, server: Optional[str] = None,
              pushkey: Optional[str] = None, text_type: Optional[str] = None, **kwargs):

        if not pushkey and not self.pushkey:
            raise ValueError("pushkey must be specified")

        res = self._send_push_request(method, desp, pushkey or self.pushkey, server or self.server, text, text_type, **kwargs)
        if res["content"]["result"]:
            result = json.loads(res["content"]["result"][1])
            if result["success"] == "ok":
                return True
            else:
                return False
        else:
            return False

    def _send_push_request(self, method, desp, key, server, text, type, **kwargs):
        if method == 'get':
            return requests.get(server + self.endpoint, params={
                "pushkey": key,
                "text": text,
                "type": type,
                "desp": desp,
            }, **kwargs).json()
        elif method == 'post':
            body = {'text': text, 'desp': desp, 'pushkey': key, 'type': type}
            response = requests.post(server + self.endpoint, data=json.dumps(body), headers=PushDeer.headers)
            return json.loads(response.text)


    def send_text(self, method: str, text: str, desp: Optional[str] = None, server: Optional[str] = None,
                  pushkey: Union[str, list, None] = None, **kwargs):
        """
        Any text are accepted when type is text.
        @param text: message : text
        @param desp: the second part of the message (optional)
        @param server: server base
        @param pushkey: pushDeer pushkey
        @return: success or not
        """
        return self._push(method=method, text=text, desp=desp, server=server, pushkey=pushkey, text_type='text', **kwargs)

    def send_markdown(self, text: str, desp: Optional[str] = None, server: Optional[str] = None,
                      pushkey: Union[str, list, None] = None, **kwargs):
        """
        Text in Markdown format are accepted when type is markdown.
        @param text: message : text in markdown
        @param desp: the second part of the message in markdown (optional)
        @param server: server base
        @param pushkey: pushDeer pushkey
        @return: success or not
        """
        return self._push(text=text, desp=desp, server=server, pushkey=pushkey, text_type='markdown', **kwargs)

    def send_image(self, image_src: str, desp: Optional[str] = None, server: Optional[str] = None,
                   pushkey: Union[str, list, None] = None, **kwargs):
        """
        Only image src are accepted by API now, when type is image.
        @param image_src: message : image URL
        @param desp: the second part of the message (optional)
        @param server: server base
        @param pushkey: pushDeer pushkey
        @return: success or not
        """
        return self._push(text=image_src, desp=desp, server=server, pushkey=pushkey, text_type='image', **kwargs)


if __name__ == "__main__":
    pushdeer = PushDeer(pushkey="PDU1TtRhwbxSrMmJ38D4aPOduQdG82WcXOHVa")
    pushdeer.send_text(method="post", text="hello world", desp="optional description")
    # pushdeer.send_markdown("# hello world", desp="**optional** description in markdown")
    # pushdeer.send_image("https://github.com/easychen/pushdeer/raw/main/doc/image/clipcode.png")
    # pushdeer.send_image("data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVQYV2NgYAAAAAMAAWgmWQ0AAAAASUVORK5CYII=")
