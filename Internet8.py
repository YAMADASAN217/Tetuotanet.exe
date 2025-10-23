Server ready at http://localhost:59759/
Server commands: [b]rowser, [q]uit
server> pip install PyQt6 PyQt6-WebEngine
Server commands: [b]rowser, [q]uit
server> import sys
Server commands: [b]rowser, [q]uit
server> from PyQt6.QtCore import QUrl
Server commands: [b]rowser, [q]uit
server> from PyQt6.QtWidgets import (
Server commands: [b]rowser, [q]uit
server>     QApplication, QMainWindow, QToolBar, QLineEdit, QWidget, QVBoxLayout
Server commands: [b]rowser, [q]uit
server> )
Server commands: [b]rowser, [q]uit
server> from PyQt6.QtWebEngineWidgets import QWebEngineView # Webページを表示する核となる部分
Server commands: [b]rowser, [q]uit
server>
Server commands: [b]rowser, [q]uit
server> class SimpleWebBrowser(QMainWindow):
Server commands: [b]rowser, [q]uit
server>     def __init__(self):
Server commands: [b]rowser, [q]uit
server>         super().__init__()
Server commands: [b]rowser, [q]uit
server>         self.setWindowTitle("鉄オタインターネット (PyQtWebEngine)")
Server commands: [b]rowser, [q]uit
server>         self.setGeometry(100, 100, 1200, 800)
Server commands: [b]rowser, [q]uit
server>
Server commands: [b]rowser, [q]uit
server>         # 1. ブラウザエンジン（Webページを表示するウィジェット）
Server commands: [b]rowser, [q]uit
server>         self.browser = QWebEngineView()
Server commands: [b]rowser, [q]uit
server>         self.browser.setUrl(QUrl("https://www.google.com")) # 初期ページを設定
Server commands: [b]rowser, [q]uit
server>
Server commands: [b]rowser, [q]uit
server>         # 2. メインレイアウトとブラウザの設定
Server commands: [b]rowser, [q]uit
server>         container = QWidget()
Server commands: [b]rowser, [q]uit
server>         layout = QVBoxLayout()
Server commands: [b]rowser, [q]uit
server>         layout.setContentsMargins(0, 0, 0, 0)
Server commands: [b]rowser, [q]uit
server>         layout.addWidget(self.browser)
Server commands: [b]rowser, [q]uit
server>         container.setLayout(layout)
Server commands: [b]rowser, [q]uit
server>         self.setCentralWidget(container)
Server commands: [b]rowser, [q]uit
server>
Server commands: [b]rowser, [q]uit
server>         # 3. ツールバーの作成
Server commands: [b]rowser, [q]uit
server>         self.toolbar = QToolBar("Navigation")
Server commands: [b]rowser, [q]uit
server>         self.addToolBar(self.toolbar)
Server commands: [b]rowser, [q]uit
server>
Server commands: [b]rowser, [q]uit
server>         # 戻るボタン
Server commands: [b]rowser, [q]uit
server>         back_button = self.toolbar.addAction("← 戻る")
Server commands: [b]rowser, [q]uit
server>         back_button.triggered.connect(self.browser.back)
Server commands: [b]rowser, [q]uit
server>
Server commands: [b]rowser, [q]uit
server>         # 進むボタン
Server commands: [b]rowser, [q]uit
server>         forward_button = self.toolbar.addAction("→ 進む")
Server commands: [b]rowser, [q]uit
server>         forward_button.triggered.connect(self.browser.forward)
Server commands: [b]rowser, [q]uit
server>
Server commands: [b]rowser, [q]uit
server>         # リロードボタン
Server commands: [b]rowser, [q]uit
server>         reload_button = self.toolbar.addAction("↻ 更新")
Server commands: [b]rowser, [q]uit
server>         reload_button.triggered.connect(self.browser.reload)
Server commands: [b]rowser, [q]uit
server>
Server commands: [b]rowser, [q]uit
server>         # アドレスバー（QLineEdit）
Server commands: [b]rowser, [q]uit
server>         self.url_bar = QLineEdit()
Server commands: [b]rowser, [q]uit
server>         self.url_bar.returnPressed.connect(self.navigate_to_url) # Enterキーで移動
Server commands: [b]rowser, [q]uit
server>         self.toolbar.addWidget(self.url_bar)
Server commands: [b]rowser, [q]uit
server>
Server commands: [b]rowser, [q]uit
server>         # 4. イベント接続
Server commands: [b]rowser, [q]uit
server>         # ページがロードされたらアドレスバーのURLを更新
Server commands: [b]rowser, [q]uit
server>         self.browser.urlChanged.connect(self.update_url_bar)
Server commands: [b]rowser, [q]uit
server>
Server commands: [b]rowser, [q]uit
server>     def navigate_to_url(self):
Server commands: [b]rowser, [q]uit
server>         # アドレスバーからURLを取得
Server commands: [b]rowser, [q]uit
server>         url = self.url_bar.text()
Server commands: [b]rowser, [q]uit
server>
Server commands: [b]rowser, [q]uit
server>         # QUrlオブジェクトに変換し、ブラウザにセット
Server commands: [b]rowser, [q]uit
server>         if not url.startswith("http://") and not url.startswith("https://"):
Server commands: [b]rowser, [q]uit
server>             url = "http://" + url
Server commands: [b]rowser, [q]uit
server>
Server commands: [b]rowser, [q]uit
server>         self.browser.setUrl(QUrl(url))
Server commands: [b]rowser, [q]uit
server>
Server commands: [b]rowser, [q]uit
server>     def update_url_bar(self, qurl):
Server commands: [b]rowser, [q]uit
server>         # ブラウザのURLが変更されたら、アドレスバーも更新
Server commands: [b]rowser, [q]uit
server>         # QUrlを文字列に変換して表示
Server commands: [b]rowser, [q]uit
server>         self.url_bar.setText(qurl.toString())
Server commands: [b]rowser, [q]uit
server>
Server commands: [b]rowser, [q]uit
server>
Server commands: [b]rowser, [q]uit
server> if __name__ == "__main__":
Server commands: [b]rowser, [q]uit
server>     # QApplicationインスタンスの作成
Server commands: [b]rowser, [q]uit
server>     app = QApplication(sys.argv)
Server commands: [b]rowser, [q]uit
server>
Server commands: [b]rowser, [q]uit
server>     # メインウィンドウの作成と表示
Server commands: [b]rowser, [q]uit
server>     window = SimpleWebBrowser()
Server commands: [b]rowser, [q]uit
server>     window.show()
Server commands: [b]rowser, [q]uit
server>
Server commands: [b]rowser, [q]uit
server>     # アプリケーションの実行
Server commands: [b]rowser, [q]uit
server>     sys.exit(app.exec())
