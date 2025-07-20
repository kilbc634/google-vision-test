import os
from openai import OpenAI

# 讀取 API 金鑰
with open("api_key/deepseek-api-key.txt", "r") as f:
    api_key = f.read().strip()

# 建立 client（使用 openai 的官方用法）
client = OpenAI(
    api_key=api_key,
    base_url="https://api.deepseek.com"  # DeepSeek 的 API endpoint
)

# ✅ 全域 Prompt（可以隨時修改）
SYSTEM_PROMPT = """
你是一個文字資料修復助手，負責修復來自 OCR 擷取的錯誤文字，並將其轉換為標準的 JSON 結構。請根據以下規則進行處理並直接回傳 JSON，**不要有任何額外對話或文字解釋**。

輸入內容是從遊戲中擷取的交易市場所顯示的表格畫面，通常包括 "AVAILABLE TRADES" 與 "COMPETING TRADES" 區塊，每一區塊皆包含：

- Ratio（格式為 "XXX:1"，其中冒號":"有時會被誤辨為數字如 "8" 或 "1"，或者完全遺失）
- Stock（數量，通常為整數或加上千分位逗號）

請修復字串錯誤後輸出如下格式的 JSON：
```json
{
  "repaired_text": "（修復後的乾淨字串，包含完整表格資訊）",
  "available_trades": [
    { "ratio": "XXX:1", "stock": 數字 },
    ...
  ],
  "competing_trades": [
    { "ratio": "XXX:1", "stock": 數字 },
    ...
  ]
}
```

處理規則：
- 若同一 Ratio 出現多次，請一併列出
- 冒號 `:` 若被誤判成數字（如 "8", "1"）或缺失，請修復為 `:`
- 不要包含 `<` 或 `>` 的比值符號（代表後續還有資料），只保留顯示的條目
- Stock 可含逗號，例如 `"19,500"` 應轉為 `19500`（純數字）
- 回應內容**只能是 JSON**，不需要其他說明或回饋

請開始處理並輸出 JSON。
"""

# ✅ 模擬 OCR 擷取的文字輸入
ocr_text = """
AVAILABLE TRADES
Ratio
Stock
657 : 1
657
656.67 8 1 1,970
656 1
15,088
651 : 1
5,20
8
650: 1
19,500
< 650 : 1
10,870
COMPETING TRADES
Ratio
Stock
690 : 1
5
695 : 1
5
696: 1
3
697: 1
2
698:
 1
4
> 698 : 1
25
"""

# ✅ 呼叫 DeepSeek API
response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": ocr_text}
    ],
    # temperature=1.0,
    stream=False
)

# ✅ 印出 JSON 回應
print(response['choices'][0]['message']['content'])
