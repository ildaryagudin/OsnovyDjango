from http.server import HTTPServer, BaseHTTPRequestHandler
import os


class SimpleWebApp(BaseHTTPRequestHandler):

    def do_GET(self):
        """Обработка GET-запросов"""
        try:
            # Определяем, какую страницу вернуть в зависимости от пути
            if self.path == '/' or self.path == '/index.html':
                html_file = 'index.html'
            elif self.path == '/catalog.html':
                html_file = 'catalog.html'
            elif self.path == '/category.html':
                html_file = 'category.html'
            elif self.path == '/contacts.html' or self.path == '/contacts':
                html_file = 'contacts.html'
            else:
                # По умолчанию возвращаем страницу контактов (как в задании)
                html_file = 'contacts.html'

            # Читаем HTML-файл
            with open(html_file, 'r', encoding='utf-8') as file:
                html_content = file.read()

            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(html_content.encode('utf-8'))

        except FileNotFoundError:
            self.send_error(404, f"File not found: {html_file}")
        except Exception as e:
            self.send_error(500, f"Server error: {str(e)}")


def run_server():
    """Запуск сервера"""
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, SimpleWebApp)
    print('Сервер запущен на http://localhost:8000')
    print('Доступные страницы:')
    print('  http://localhost:8000/ - Главная')
    print('  http://localhost:8000/catalog.html - Каталог')
    print('  http://localhost:8000/category.html - Категории')
    print('  http://localhost:8000/contacts.html - Контакты')
    print('  Любой другой путь - Контакты (по умолчанию)')
    httpd.serve_forever()


if __name__ == '__main__':
    run_server()