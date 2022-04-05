from http.server import BaseHTTPRequestHandler, HTTPServer
import re
import numpy as np
import Predictor

def match_then_insert(filename, match, content):
    lines = open(filename).read().splitlines()
#    print(type(lines), lines)
    index = lines.index(match)
#    print(index)
    lines[index-1] = content
    open(filename, mode='w').write('\n'.join(lines))

class myHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)  # код возврата, 200 это успешное подключение
        self.send_header('Content-type','text/html') # заголовок ответа, указываем тип контента html
        self.end_headers() # завершаем передачу заголовков и отправляем их для установления соединения
        path = self.path     # получаем url адрес введенный пользователем
        if path == "/":
            path = "/index"

        try:
            file  = open("pages"+path + ".html", 'r')
        except FileNotFoundError:              # Если  шаблон не найден
            file  = open("pages/404.html", 'r')

        message = file.read()
        file.close()
        self.wfile.write(bytes(message, "utf8"))  # с помощью данной строчки мы отдаем ответ от сервера, а именно в качестве ответа будет значение переменной message. Функция bytes() кодирует строку в определенную кодировку, в нашем случае это utf8.
        return

    def do_POST(self):

        global model

        self.send_response(301) # код перенаправления
        self.send_header('Location', '/') # заголовок редиректа, то есть при завершении этого запроса я хочу вернуться на страницу support.html
        self.end_headers()  #  завершаем передачу заголовков и отправляем их для установления соединения
        path = self.path   #  получаем url адрес введенный пользователем

        # Обработчик чек боксов
        if path == "/check":
            content_len = int(self.headers.get('Content-Length'))
            click = self.rfile.read(content_len)  # получаем наши переданные данные
            click = re.split(r'=on&|=on',str(click)) # убираем лишнее
            skills_list = [re.sub(r"b\'", "", skill) for skill in click ]  # удалям b\'
            print(skills_list[:-1])
            skills_list = skills_list[:-1]
#            Salary = np.random.choice([111,222,333])
            sample = model.get_sample(skills_list)
            predict = model.get_predict(sample)
            print(predict)
            match_then_insert('pages/index.html', match='   </form>', content=f'Salary is {predict}')

        # Обработчик отправки
        if path == "/skill":
            content_len = int(self.headers.get('Content-Length'))
            post = self.rfile.read(content_len)   # получаем наши переданные данные
            pattern = r"\'|b|skill=|salaries="
            post = re.sub(pattern, "", str(post))
            pattern = r"\+|&"
            post = re.split(pattern, post)
            print(post)
        return

model = Predictor.Model()
server = HTTPServer(('127.0.0.1', 8081), myHandler) # обращаемся к серверу
server.serve_forever() # запускаем