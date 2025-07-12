from google.cloud import vision
from google.oauth2 import service_account

# 替換成你的金鑰路徑
key_path = "api_key/game-server-387707-5af02280f56c.json"

# 載入憑證
credentials = service_account.Credentials.from_service_account_file(key_path)

# 建立 Vision API 客戶端
client = vision.ImageAnnotatorClient(credentials=credentials)

# 使用範例：讀圖進行 OCR
def extract_text(image_path):
    with open(image_path, "rb") as image_file:
        content = image_file.read()

    image = vision.Image(content=content)
    response = client.text_detection(image=image)

    texts = response.text_annotations
    if not texts:
        return ""

    return texts[0].description.strip()

# 範例呼叫
text = extract_text("image/4a5s6d.png")
print(text)
