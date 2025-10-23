import socket
import html.parser
import tkinter as tk
from tkinter import scrolledtext
from urllib.parse import urlparse, urljoin

# --- 1. HTTP通信部分（前回と同じ。httpsは非対応） ---
def get_html_content(url):
    """
    指定されたURLから生のHTMLコンテンツをソケット通信で取得します。
    """
    parsed_url = urlparse(url)
    host = parsed_url.netloc
    path = parsed_url.path if parsed_url.path else "/"
    port = 80

    if not host:
        return "Error: 無効なURL形式です。"
        
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(5) # タイムアウト設定
            s.connect((host, port))

            # HTTP GETリクエスト
            request = f"GET {path} HTTP/1.0\r\nHost: {host}\r\nUser-Agent: SimplePythonBrowser\r\nConnection: close\r\n\r\n"
            s.sendall(request.encode('utf-8'))

            response = b""
            while True:
                chunk = s.recv(4096)
                if not chunk:
                    break
                response += chunk

            # ヘッダーとボディの分離
            response_text = response.decode('utf-8', errors='ignore')
            header_end = response_text.find("\r\n\r\n")
            if header_end == -1:
                return "Error: 無効なHTTPレスポンスです。"

            # ステータスコードの確認（例：200 OK以外はエラーとして扱う）
            status_line = response_text.split('\r\n')[0]
            if not status_line.startswith("HTTP/1.") or " 200 " not in status_line:
                 return f"Error: HTTPステータスコードエラー ({status_line})"

            return response_text[header_end + 4:]

    except socket.gaierror:
        return f"Error: ホスト名 {host} の解決に失敗しました。"
    except socket.timeout:
        return "Error: 接続がタイムアウトしました。"
    except Exception as e:
        return f"Error: 通信中にエラーが発生しました。\n{e}"

# --- 2. HTML解析部分（html.parserを使用） ---
class HyperlinkParser(html.parser.HTMLParser):
    """
    HTMLを解析し、Textウィジェットに出力する際、リンク（aタグ）を特別に処理するパーサー。
    """
    def __init__(self, output_text_widget, base_url, load_command):
        super().__init__()
        self.output_widget = output_text_widget
        self.base_url = base_url
        self.load_command = load_command # リンククリック時に実行するコールバック関数
        self.in_body = False
        self.in_link = False
        self.link_url = ""
        self.ignore_tags = ('script', 'style', 'head', 'title', 'meta')

        # tkinter Textウィジェットのタグ設定
        self.output_widget.tag_config("link", foreground="blue", underline=1)
        # リンクをクリックしたときのイベントバインド
        self.output_widget.tag_bind("link", "<Button-1>", self._handle_link_click)
        
    def _handle_link_click(self, event):
        """リンクがクリックされたときに呼び出される処理"""
        # カーソル位置のタグを取得
        index = self.output_widget.index("@%s,%s" % (event.x, event.y))
        
        # 'link_...'タグを取得し、URLを抽出
        tag_names = self.output_widget.tag_names(index)
        for tag in tag_names:
            if tag.startswith("link_"):
                # タグ名に埋め込んだURLを取得
                target_url = tag[5:] 
                # コールバック関数を実行してページをロード
                self.load_command(target_url)
                break


    def handle_starttag(self, tag, attrs):
        if tag == 'body':
            self.in_body = True
        
        # リンクタグの処理
        elif tag == 'a':
            self.in_link = True
            self.link_url = ""
            attrs_dict = dict(attrs)
            href = attrs_dict.get('href')
            if href:
                # 相対パスを絶対パスに変換
                self.link_url = urljoin(self.base_url, href)

        # ブロック要素の開始（簡易的な改行処理）
        elif tag in ('p', 'div', 'br', 'h1', 'h2', 'h3') and self.in_body:
            self.output_widget.insert(tk.END, '\n\n')

    def handle_endtag(self, tag):
        if tag == 'body':
            self.in_body = False
        
        # リンクタグの終了処理
        elif tag == 'a':
            self.in_link = False
            self.link_url = ""
        
        # ブロック要素の終了（簡易的な改行処理）
        elif tag in ('p', 'div') and self.in_body:
            self.output_widget.insert(tk.END, '\n\n')


    def handle_data(self, data):
        if self.in_body and self.current_tag not in self.ignore_tags:
            cleaned_data = ' '.join(data.split())
            if not cleaned_data:
                return

            if self.in_link:
                # リンクの場合は、タグとURLを関連付けてTextウィジェットに挿入
                # URLをエスケープしてタグ名に埋め込む
                tag_name_url = f"link_{self.link_url}"
                
                # リンククリック時に使うタグ(link_URL)を作成しつつ、表示用のタグ(link)を適用
                self.output_widget.tag_config(tag_name_url, foreground="blue", underline=1)
                self.output_widget.tag_bind(tag_name_url, "<Button-1>", self._handle_link_click)
                
                self.output_widget.insert(tk.END, cleaned_data + ' ', ("link", tag_name_url))
            else:
                # 通常のテキスト
                self.output_widget.insert(tk.END, cleaned_data + ' ')

# --- 3. GUIとメインロジック部分（tkinterを使用） ---
class FullBrowserApp:
    def __init__(self, master):
        self.master = master
        master.title("標準ライブラリ製・本格簡易ブラウザ (リンク対応)")

        # URLバーとボタンのフレーム
        top_frame = tk.Frame(master)
        top_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.url_entry = tk.Entry(top_frame, width=70)
        self.url_entry.insert(0, "http://example.com") # テスト用のURL
        self.url_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        self.go_button = tk.Button(top_frame, text="Go", command=lambda: self.load_page(self.url_entry.get()))
        self.go_button.pack(side=tk.RIGHT, padx=5)

        # 表示エリア
        self.text_area = scrolledtext.ScrolledText(master, wrap=tk.WORD, width=80, height=30, font=('Helvetica', 12))
        self.text_area.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
        self.text_area.config(state=tk.DISABLED) # ユーザーによる編集を禁止

        # 最初のページをロード
        self.load_page(self.url_entry.get())


    def load_page(self, url):
        """指定されたURLのページを読み込むメイン処理"""
        # ロード前にUIを更新
        self.url_entry.delete(0, tk.END)
        self.url_entry.insert(0, url)
        self.text_area.config(state=tk.NORMAL)
        self.text_area.delete(1.0, tk.END)
        self.text_area.insert(tk.END, f"接続中: {url}...\n\n")
        self.text_area.update_idletasks() # 即座に画面を更新

        # ページコンテンツを取得
        html_content = get_html_content(url)
        
        self.text_area.delete(1.0, tk.END) # ステータスをクリア
        
        if html_content.startswith("Error:"):
            # エラーの場合はそのまま表示
            self.text_area.insert(tk.END, html_content)
        else:
            # HTMLを解析して表示エリアに出力
            parser = HyperlinkParser(self.text_area, url, self.load_page)
            
            try:
                parser.feed(html_content)
            except Exception as e:
                self.text_area.insert(tk.END, f"致命的なパースエラー:\n{e}")
            finally:
                parser.close()

        self.text_area.config(state=tk.DISABLED) # 編集禁止に戻す


# アプリの実行
if __name__ == "__main__":
    root = tk.Tk()
    app = FullBrowserApp(root)
    root.mainloop()
