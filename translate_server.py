from flask import Flask, jsonify, request
#from transformers import AutoModelForCausalLM, AutoTokenizer
import requests
import json
import time
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
from  prompt import  trasnalte_prompt


# 设置请求的头部信息
url = "http://localhost:11434/api/generate"
headers = {
    "Content-Type": "application/json"
}

#pipe = pipeline("translation", model="google-t5/t5-base")
app = Flask(__name__)

pattern = r'"response":"(.*?)"'

# 繁体中文(中国香港) (zh-hk) 英语(马来西亚) (en-my) 英语(中国香港) (en-hk) 英语(新加坡) (en-sg) 英语(菲律宾) (en-ph) 繁体中文(中国台湾) (zh-tw)
# 示例数据
locals = {"zh-hk": '繁体中文(中国香港)', 'en-my': '英语(马来西亚)', 'en-hk': '英语(中国香港)',  'en-sg': '英语(新加坡)', 'en-ph': '英语(菲律宾)', 'zh-tw': '繁体中文(中国台湾)'}

def t5_translate(text):
    pass
    # tokenizer = AutoTokenizer.from_pretrained("/Users/wangweiyi/.ollama/models/blobs")
    # model = AutoModelForCausalLM.from_pretrained("/Users/wangweiyi/.ollama/models/blobs")
    # input_ids = tokenizer(f"translate to English:{text}", return_tensors="pt").input_ids
    # outputs = model.generate(input_ids, max_length=512, num_beams=4, early_stopping=True)
    # print(tokenizer.decode(outputs[0], skip_special_tokens=True))
    # return  tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    

    
    
def llama_translate(text, local): 
   
    response = requests.post(url, headers=headers, json=trasnalte_prompt(text, local), stream=True)
    timestamp = time.time()
    # 检查响应状态
    if response.status_code == 200:
        # 逐块读取响应
        for line in response.iter_lines():
            if line:
                decoded_line = line.decode('utf-8')
                print(decoded_line)
                save_stream_to_file(decoded_line, str(timestamp) + local)
    else:
        print(f"Error: {response.status_code}, {response.text}")
    





@app.route('/translate', methods=['POST'])
def post_translate():
    print(str(request.args.keys()))
    # 检查请求的 Content-Type 是否为 application/json
    if request.is_json:
        # 获取 JSON 数据
        data = request.get_json()
        print(data)

        # # 解析数据
        texts = data.get('text')
        # for local in locals.keys():
        #     llama_translate(texts, local) # 同步执行 stream 结果
            
        # 提交任务
        with ThreadPoolExecutor(max_workers=3) as executor:
            futures = [executor.submit(llama_translate, texts, local) for local in locals.keys()]

            # 等待任务完成并获取结果
            for future in as_completed(futures):
                result = future.result()
                print(result)

        # 处理数据并生成响应
        # response_data = {
        #     "message": f"Received model: {model} with prompt: {prompt}"
        # }

        # 返回 JSON 响应
        return jsonify([]), 200
    else:
        return jsonify({"error": "Request must be JSON"}), 400


@app.route('/translateLocals', methods=['POST']) 
def get_locals():
    return jsonify(locals)


def save_stream_to_file(decoded_line, key):
    # 搜索匹配
    match = re.search(pattern, decoded_line)
    # 提取匹配的内容
    if match:
        extracted_text = match.group(1)
        print(f"Extracted text: {extracted_text}")
    else:
        print("No match found.")

    with open(f"{key}_output.txt", "a") as f:
        f.write(extracted_text)

   

# # 获取特定书籍
# @app.route('/books/<int:book_id>', methods=['GET'])
# def get_book(book_id):
#     book = next((book for book in books if book['id'] == book_id), None)
#     if book is not None:
#         return jsonify(book)
#     else:
#         return jsonify({'error': 'Book not found'}), 404

# # 添加新书籍
# @app.route('/books', methods=['POST'])
# def add_book():
#     new_book = request.get_json()
#     books.append(new_book)
#     return jsonify(new_book), 201

# # 更新书籍
# @app.route('/books/<int:book_id>', methods=['PUT'])
# def update_book(book_id):
#     book = next((book for book in books if book['id'] == book_id), None)
#     if book is not None:
#         updated_data = request.get_json()
#         book.update(updated_data)
#         return jsonify(book)
#     else:
#         return jsonify({'error': 'Book not found'}), 404

# # 删除书籍
# @app.route('/books/<int:book_id>', methods=['DELETE'])
# def delete_book(book_id):
#     global books
#     books = [book for book in books if book['id'] != book_id]
#     return jsonify({'message': 'Book deleted'}), 204


    

if __name__ == '__main__':
    app.run(debug=True)
