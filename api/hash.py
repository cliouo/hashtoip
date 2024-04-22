from http.server import BaseHTTPRequestHandler
import json
from os.path import join, dirname

# 全局变量，存储倒排索引
inverted_index = {}

# 预处理文本文件并构建倒排索引
def preprocess_and_build_index(file_path):
    global inverted_index
    with open(file_path, 'r') as file:
        offset = 0
        for line in file:
            key, value = line.strip().split()
            if key not in inverted_index:
                inverted_index[key] = []
            inverted_index[key].append((offset, value))
            offset += len(line)

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith('/query'):
            query_params = self.path.split('?')[1]
            query_dict = dict(param.split('=') for param in query_params.split('&'))
            query_key = query_dict.get('key')

            if query_key in inverted_index:
                results = inverted_index[query_key]
                response_data = {'key': query_key, 'results': [{'offset': offset, 'value': value} for offset, value in results]}
            else:
                response_data = {'key': query_key, 'results': []}

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response_data).encode('utf-8'))
        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write('Not Found'.encode('utf-8'))

# 启动应用并创建索引
if __name__ == '__main__':
    current_dir = dirname(__file__)
    file_path = join('data', 'HashToIP.log')
    preprocess_and_build_index(file_path)
