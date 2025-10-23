import tkinter as tk
from tkinter import messagebox
import webbrowser

# ブラウザを開く関数
def navigate():
    # エントリーに入力されたURLを取得
    url = url_entry.get()

    # URLが空でないことを確認
    if not url:
        messagebox.showerror("エラー", "URLを入力してください")
        return

    # URLの先頭に「http://」または「https://」がない場合は追加
    if not url.startswith("http://") and not url.startswith("https://"):
        url = "http://" + url
    
    # デフォルトのWebブラウザでURLを開く
    try:
        webbrowser.open_new_tab(url)
    except Exception as e:
        messagebox.showerror("エラー", f"ブラウザを開けませんでした: {e}")

# メインウィンドウの設定
root = tk.Tk()
root.title("簡易ブラウザ")
root.geometry("400x150") # ウィンドウサイズを設定

# URL入力用のEntryウィジェット
url_entry = tk.Entry(root, width=50)
url_entry.pack(padx=10, pady=10)
url_entry.insert(0, "https://www.google.com") # 初期値を設定

# 「Go」ボタン
go_button = tk.Button(root, text="Go!", command=navigate)
go_button.pack(pady=10)

# Enterキーでnavigate関数を実行するようバインド
root.bind('<Return>', lambda event=None: navigate())

# GUIのメインループを開始
root.mainloop()
