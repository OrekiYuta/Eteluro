import os
import subprocess
import sys
import webbrowser
from http.server import HTTPServer, CGIHTTPRequestHandler


def open_browser_link(post):
    webbrowser.open("http://localhost:" + post)


if __name__ == '__main__':
    current_path = os.getcwd()
    # print(current_path)
    http_path = current_path + '\\' + sys.argv[1]
    # print(http_path)
    http_post = sys.argv[2]

    # main process
    open_browser_link(http_post)

    # to target path then start http server
    os.chdir(http_path)
    # subprocess
    subprocess.check_call(
        HTTPServer(("localhost", int(http_post)), CGIHTTPRequestHandler).serve_forever()
    )

'''
python main.py dist 9090
'''