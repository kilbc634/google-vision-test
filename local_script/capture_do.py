import configparser
from ahk import AHK
import mss
from PIL import Image
import requests

# 初始化 AHK（手動指定 AutoHotkey.exe 路徑）
Ahk = AHK(executable_path='C:\\Program Files\\AutoHotkey\\AutoHotkey.exe')

# 讀取截圖區域
def read_capture_region(config_path="config.ini"):
    config = configparser.ConfigParser()
    config.read(config_path)
    rect = config["Rectangle"]
    return {
        "top": int(rect["y"]),
        "left": int(rect["x"]),
        "width": int(rect["width"]),
        "height": int(rect["height"]),
    }

# 執行截圖
def capture_screen(region, output_file="temp.png"):
    with mss.mss() as sct:
        img = sct.grab(region)
        im = Image.frombytes("RGB", img.size, img.rgb)
        im.save(output_file, format="PNG")
        print(f"[✓] 截圖已保存：{output_file}")

# F2 熱鍵對應的動作
def on_f2_hotkey():
    print("[*] F2 被按下，開始截圖...")
    region = read_capture_region()
    capture_screen(region)

    api_url = "http://tsukumonet.ddns.net:19862/upload"
    with open("temp.png", "rb") as img_file:
        files = {'file': ("temp.png", img_file, "image/png")}
        try:
            response = requests.post(api_url, files=files)
            print(f"[→] API 回應狀態：{response.status_code}")
            print(f"[→] API 回應內容：{response.text}")
        except Exception as e:
            print(f"[!] 傳送圖片失敗：{e}")

# 註冊熱鍵
Ahk.add_hotkey('F2', callback=on_f2_hotkey)

if __name__ == "__main__":
    Ahk.start_hotkeys()
    print("[*] 熱鍵 F2 已綁定，等待觸發...")
    Ahk.block_forever()
