from typing import Any, Dict, List
from flask import Flask, render_template, request
import os
import math
from collections import Counter

app = Flask(__name__)


def calculate_tf_idf(word, documents) -> List:
    len_docs: int = len(documents)
    count_word = sum(1 for document in documents if word in document)
    if count_word == 0:
        return 0
    print(count_word)
    tf: float = round(count_word / len_docs, 2)
    idf: float = round(math.log(len_docs / count_word), 2)
    result: list = [tf, idf]

    return result


def process_file(file_path) -> Any:
    with open(file_path, 'r') as file:
        text = file.read()

    words: list = text.split()
    tf: Counter = Counter(words)
    idf: dict = {word: calculate_tf_idf(word, words) for word in tf.keys()}
    sorted_words: list = sorted(idf.items(), key=lambda x: x[1][1], reverse=True)

    return sorted_words[:50]


@app.route('/app', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            file_path = os.path.join('uploads', file.filename)
            file.save(file_path)
            words = process_file(file_path)
            return render_template('result.html', words=words)

    return render_template('upload.html')


if __name__ == '__main__':
    app.run(debug=True)
