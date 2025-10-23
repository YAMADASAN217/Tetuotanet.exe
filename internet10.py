Server ready at http://localhost:56636/
Server commands: [b]rowser, [q]uit
server> import socket
Server commands: [b]rowser, [q]uit
server> import html.parser
Server commands: [b]rowser, [q]uit
server> import tkinter as tk
Server commands: [b]rowser, [q]uit
server> from tkinter import scrolledtext
Server commands: [b]rowser, [q]uit
server> from urllib.parse import urlparse, urljoin
Server commands: [b]rowser, [q]uit
server> from socket import gaierror, timeout, error as socket_error
Server commands: [b]rowser, [q]uit
server>
Server commands: [b]rowser, [q]uit
server> # --- 1. HTTP通信部分（socketを使用） ---
Server commands: [b]rowser, [q]uit
server> def get_html_content(url):
Server commands: [b]rowser, [q]uit
server>     """指定されたURLから生のHTMLコンテンツをソケット通信で取得します。"""
Server commands: [b]rowser, [q]uit
server>     parsed_url = urlparse(url)
Server commands: [b]rowser, [q]uit
server>     host = parsed_url.netloc
Server commands: [b]rowser, [q]uit
server>     path = parsed_url.path if parsed_url.path else "/"
Server commands: [b]rowser, [q]uit
server>     port = 80 # HTTPのデフォルトポート
Server commands: [b]rowser, [q]uit
server>
Server commands: [b]rowser, [q]uit
server>     if not host:
Server commands: [b]rowser, [q]uit
server>         return "Error: 無効なURL形式です。ホスト名が含まれていません。"
Server commands: [b]rowser, [q]uit
server>
Server commands: [b]rowser, [q]uit
server>     try:
Server commands: [b]rowser, [q]uit
server>         with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
Server commands: [b]rowser, [q]uit
server>             s.settimeout(5) # タイムアウトを5秒に設定
Server commands: [b]rowser, [q]uit
server>
Server commands: [b]rowser, [q]uit
server>             ip_address = socket.gethostbyname(host)
Server commands: [b]rowser, [q]uit
server>             s.connect((ip_address, port))
Server commands: [b]rowser, [q]uit
server>
Server commands: [b]rowser, [q]uit
server>             # HTTP GETリクエストを作成し送信 (Hostヘッダーと\r\n\r\nは必須)
Server commands: [b]rowser, [q]uit
server>             request = (
Server commands: [b]rowser, [q]uit
server>                 f"GET {path} HTTP/1.0\r\n"
Server commands: [b]rowser, [q]uit
server>                 f"Host: {host}\r\n"
Server commands: [b]rowser, [q]uit
server>                 f"User-Agent: SimplePythonBrowser/1.0\r\n"
Server commands: [b]rowser, [q]uit
server>                 f"Connection: close\r\n"
Server commands: [b]rowser, [q]uit
server>                 f"\r\n"
Server commands: [b]rowser, [q]uit
server>             )
Server commands: [b]rowser, [q]uit
server>             s.sendall(request.encode('utf-8'))
Server commands: [b]rowser, [q]uit
server>
Server commands: [b]rowser, [q]uit
server>             response = b""
Server commands: [b]rowser, [q]uit
server>             while True:
Server commands: [b]rowser, [q]uit
server>                 chunk = s.recv(4096)
Server commands: [b]rowser, [q]uit
server>                 if not chunk:
Server commands: [b]rowser, [q]uit
server>                     break
Server commands: [b]rowser, [q]uit
server>                 response += chunk
Server commands: [b]rowser, [q]uit
server>
Server commands: [b]rowser, [q]uit
server>             response_text = response.decode('utf-8', errors='ignore')
Server commands: [b]rowser, [q]uit
server>             header_end = response_text.find("\r\n\r\n")
Server commands: [b]rowser, [q]uit
server>
Server commands: [b]rowser, [q]uit
server>             if header_end == -1:
Server commands: [b]rowser, [q]uit
server>                 return "Error: 無効なHTTPレスポンス形式です。"
Server commands: [b]rowser, [q]uit
server>
Server commands: [b]rowser, [q]uit
server>             status_line = response_text.split('\r\n')[0]
Server commands: [b]rowser, [q]uit
server>             if not status_line.startswith("HTTP/1.") or " 200 " not in status_line:
Server commands: [b]rowser, [q]uit
server>                  return f"Error: HTTPステータスコードエラー\n\n--- レスポンスヘッダー --- \n{response_text[:header_end]}"
Server commands: [b]rowser, [q]uit
server>
Server commands: [b]rowser, [q]uit
server>             return response_text[header_end + 4:]
Server commands: [b]rowser, [q]uit
server>
Server commands: [b]rowser, [q]uit
server>     except gaierror:
Server commands: [b]rowser, [q]uit
server>         return f"Error: ホスト名 ({host}) の解決に失敗しました。"
Server commands: [b]rowser, [q]uit
server>     except timeout:
Server commands: [b]rowser, [q]uit
server>         return "Error: 接続またはデータ受信がタイムアウトしました。"
Server commands: [b]rowser, [q]uit
server>     except socket_error as e:
Server commands: [b]rowser, [q]uit
server>         return f"Error: ソケット通信中にエラーが発生しました。\n詳細: {e}"
Server commands: [b]rowser, [q]uit
server>     except Exception as e:
Server commands: [b]rowser, [q]uit
server>         return f"Error: 予期せぬエラーが発生し、通信が中断されました。\n詳細: {e}"
Server commands: [b]rowser, [q]uit
server>
Server commands: [b]rowser, [q]uit
server> # --- 2. HTML解析部分（html.parserを使用） ---
Server commands: [b]rowser, [q]uit
server> class HyperlinkParser(html.parser.HTMLParser):
Server commands: [b]rowser, [q]uit
server>     """HTMLを解析し、Textウィジェットに出力し、リンクを処理するパーサー。"""
Server commands: [b]rowser, [q]uit
server>     def __init__(self, output_text_widget, base_url, load_command):
Server commands: [b]rowser, [q]uit
server>         super().__init__()
Server commands: [b]rowser, [q]uit
server>         self.output_widget = output_text_widget
Server commands: [b]rowser, [q]uit
server>         self.base_url = base_url
Server commands: [b]rowser, [q]uit
server>         self.load_command = load_command
Server commands: [b]rowser, [q]uit
server>         self.in_body = False
Server commands: [b]rowser, [q]uit
server>         self.in_link = False
Server commands: [b]rowser, [q]uit
server>         self.link_url = ""
Server commands: [b]rowser, [q]uit
server>         self.ignore_tags = ('script', 'style', 'head', 'title', 'meta')
Server commands: [b]rowser, [q]uit
server>
Server commands: [b]rowser, [q]uit
server>         self.output_widget.tag_config("link", foreground="blue", underline=1)
Server commands: [b]rowser, [q]uit
server>
Server commands: [b]rowser, [q]uit
server>     def _handle_link_click(self, event):
Server commands: [b]rowser, [q]uit
server>         """リンククリック時の処理"""
Server commands: [b]rowser, [q]uit
server>         index = self.output_widget.index("@%s,%s" % (event.x, event.y))
Server commands: [b]rowser, [q]uit
server>
Server commands: [b]rowser, [q]uit
server>         for tag in self.output_widget.tag_names(index):
Server commands: [b]rowser, [q]uit
server>             if tag.startswith("link_"):
Server commands: [b]rowser, [q]uit
server>                 target_url = tag[5:]
Server commands: [b]rowser, [q]uit
server>                 self.load_command(target_url)
Server commands: [b]rowser, [q]uit
server>                 break
Server commands: [b]rowser, [q]uit
server>
Server commands: [b]rowser, [q]uit
server>     def handle_starttag(self, tag, attrs):
Server commands: [b]rowser, [q]uit
server>         if tag == 'body':
Server commands: [b]rowser, [q]uit
server>             self.in_body = True
Server commands: [b]rowser, [q]uit
server>
Server commands: [b]rowser, [q]uit
server>         elif tag == 'a':
Server commands: [b]rowser, [q]uit
server>             self.in_link = True
Server commands: [b]rowser, [q]uit
server>             self.link_url = ""
Server commands: [b]rowser, [q]uit
server>             attrs_dict = dict(attrs)
Server commands: [b]rowser, [q]uit
server>             href = attrs_dict.get('href')
Server commands: [b]rowser, [q]uit
server>             if href:
Server commands: [b]rowser, [q]uit
server>                 self.link_url = urljoin(self.base_url, href)
Server commands: [b]rowser, [q]uit
server>
Server commands: [b]rowser, [q]uit
server>         elif tag in ('p', 'div', 'br', 'h1', 'h2', 'h3') and self.in_body:
Server commands: [b]rowser, [q]uit
server>             self.output_widget.insert(tk.END, '\n\n')
Server commands: [b]rowser, [q]uit
server>
Server commands: [b]rowser, [q]uit
server>     def handle_endtag(self, tag):
Server commands: [b]rowser, [q]uit
server>         if tag == 'body':
Server commands: [b]rowser, [q]uit
server>             self.in_body = False
Server commands: [b]rowser, [q]uit
server>
Server commands: [b]rowser, [q]uit
server>         elif tag == 'a':
Server commands: [b]rowser, [q]uit
server>             self.in_link = False
Server commands: [b]rowser, [q]uit
server>             self.link_url = ""
Server commands: [b]rowser, [q]uit
server>
Server commands: [b]rowser, [q]uit
server>         elif tag in ('p', 'div') and self.in_body:
Server commands: [b]rowser, [q]uit
server>             self.output_widget.insert(tk.END, '\n\n')
Server commands: [b]rowser, [q]uit
server>
Server commands: [b]rowser, [q]uit
server>
Server commands: [b]rowser, [q]uit
server>     def handle_data(self, data):
Server commands: [b]rowser, [q]uit
server>         if self.in_body and self.current_tag not in self.ignore_tags:
Server commands: [b]rowser, [q]uit
server>             cleaned_data = ' '.join(data.split())
Server commands: [b]rowser, [q]uit
server>             if not cleaned_data:
Server commands: [b]rowser, [q]uit
server>                 return
Server commands: [b]rowser, [q]uit
server>
Server commands: [b]rowser, [q]uit
server>             if self.in_link and self.link_url:
Server commands: [b]rowser, [q]uit
server>                 tag_name_url = f"link_{self.link_url}"
Server commands: [b]rowser, [q]uit
server>                 self.output_widget.tag_bind(tag_name_url, "<Button-1>", self._handle_link_click)
Server commands: [b]rowser, [q]uit
server>                 self.output_widget.insert(tk.END, cleaned_data + ' ', ("link", tag_name_url))
Server commands: [b]rowser, [q]uit
server>             else:
Server commands: [b]rowser, [q]uit
server>                 self.output_widget.insert(tk.END, cleaned_data + ' ')
Server commands: [b]rowser, [q]uit
server>
Server commands: [b]rowser, [q]uit
server>     def error(self, message):
Server commands: [b]rowser, [q]uit
server>         pass
Server commands: [b]rowser, [q]uit
server>
Server commands: [b]rowser, [q]uit
server> # --- 3. GUIとメインロジック部分（tkinterを使用） ---
Server commands: [b]rowser, [q]uit
server> class FullBrowserApp:
Server commands: [b]rowser, [q]uit
server>     def __init__(self, master):
Server commands: [b]rowser, [q]uit
server>         self.master = master
Server commands: [b]rowser, [q]uit
server>         # ユーザー指定のタイトル
Server commands: [b]rowser, [q]uit
server>         master.title("鉄オタインターネット ")
Server commands: [b]rowser, [q]uit
server>
Server commands: [b]rowser, [q]uit
server>         top_frame = tk.Frame(master)
Server commands: [b]rowser, [q]uit
server>         top_frame.pack(fill=tk.X, padx=10, pady=5)
Server commands: [b]rowser, [q]uit
server>
Server commands: [b]rowser, [q]uit
server>         self.url_entry = tk.Entry(top_frame, width=70)
Server commands: [b]rowser, [q]uit
server>         self.url_entry.insert(0, "http://example.com")
Server commands: [b]rowser, [q]uit
server>         self.url_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
Server commands: [b]rowser, [q]uit
server>
Server commands: [b]rowser, [q]uit
server>         self.go_button = tk.Button(top_frame, text="Go", command=lambda: self.load_page(self.url_entry.get()))
Server commands: [b]rowser, [q]uit
server>         self.go_button.pack(side=tk.RIGHT, padx=5)
Server commands: [b]rowser, [q]uit
server>
Server commands: [b]rowser, [q]uit
server>         self.text_area = scrolledtext.ScrolledText(master, wrap=tk.WORD, width=80, height=30, font=('Helvetica', 12))
Server commands: [b]rowser, [q]uit
server>         self.text_area.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
Server commands: [b]rowser, [q]uit
server>         self.text_area.config(state=tk.DISABLED)
Server commands: [b]rowser, [q]uit
server>
Server commands: [b]rowser, [q]uit
server>         self.text_area.config(state=tk.NORMAL)
Server commands: [b]rowser, [q]uit
server>         self.text_area.insert(tk.END, "URLを入力してGoボタンを押してください（HTTPSは非対応です）。")
Server commands: [b]rowser, [q]uit
server>         self.text_area.config(state=tk.DISABLED)
Server commands: [b]rowser, [q]uit
server>
Server commands: [b]rowser, [q]uit
server>
Server commands: [b]rowser, [q]uit
server>     def load_page(self, url):
Server commands: [b]rowser, [q]uit
server>         """指定されたURLのページを読み込むメイン処理"""
Server commands: [b]rowser, [q]uit
server>
Server commands: [b]rowser, [q]uit
server>         self.url_entry.delete(0, tk.END)
Server commands: [b]rowser, [q]uit
server>         self.url_entry.insert(0, url)
Server commands: [b]rowser, [q]uit
server>
Server commands: [b]rowser, [q]uit
server>         self.text_area.config(state=tk.NORMAL)
Server commands: [b]rowser, [q]uit
server>         self.text_area.delete(1.0, tk.END)
Server commands: [b]rowser, [q]uit
server>         self.text_area.insert(tk.END, f"接続中: {url}...\n\n", "status")
Server commands: [b]rowser, [q]uit
server>         self.text_area.update_idletasks() # UIの強制更新
Server commands: [b]rowser, [q]uit
server>
Server commands: [b]rowser, [q]uit
server>         html_content = get_html_content(url)
Server commands: [b]rowser, [q]uit
server>
Server commands: [b]rowser, [q]uit
server>         self.text_area.delete(1.0, tk.END)
Server commands: [b]rowser, [q]uit
server>
Server commands: [b]rowser, [q]uit
server>         if html_content.startswith("Error:"):
Server commands: [b]rowser, [q]uit
server>             self.text_area.tag_config("error", foreground="red")
Server commands: [b]rowser, [q]uit
server>             self.text_area.insert(tk.END, html_content, "error")
Server commands: [b]rowser, [q]uit
server>         else:
Server commands: [b]rowser, [q]uit
server>             parser = HyperlinkParser(self.text_area, url, self.load_page)
Server commands: [b]rowser, [q]uit
server>
Server commands: [b]rowser, [q]uit
server>             try:
Server commands: [b]rowser, [q]uit
server>                 parser.feed(html_content)
Server commands: [b]rowser, [q]uit
server>             except Exception as e:
Server commands: [b]rowser, [q]uit
server>                 self.text_area.tag_config("error", foreground="red")
Server commands: [b]rowser, [q]uit
server>                 self.text_area.insert(tk.END, f"致命的なパースエラー:\n{e}", "error")
Server commands: [b]rowser, [q]uit
server>             finally:
Server commands: [b]rowser, [q]uit
server>                 parser.close()
Server commands: [b]rowser, [q]uit
server>
Server commands: [b]rowser, [q]uit
server>         self.text_area.config(state=tk.DISABLED)
Server commands: [b]rowser, [q]uit
server>
Server commands: [b]rowser, [q]uit
server> # アプリの実行
Server commands: [b]rowser, [q]uit
server> if __name__ == "__main__":
Server commands: [b]rowser, [q]uit
server>     root = tk.Tk()
Server commands: [b]rowser, [q]uit
server>     app = FullBrowserApp(root)
Server commands: [b]rowser, [q]uit
server>     # これがウィンドウを維持するメインループです
Server commands: [b]rowser, [q]uit
server>     root.mainloop()
