import cv2
import os

def ensure_dir(dir_path):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

def preprocess_debug(input_path, output_dir):
    ensure_dir(output_dir)

    # 讀取原圖
    img = cv2.imread(input_path)
    cv2.imwrite(os.path.join(output_dir, "original.png"), img)

    # 灰階
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cv2.imwrite(os.path.join(output_dir, "gray.png"), gray)

    # 對比增強 (CLAHE)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    contrast = clahe.apply(gray)
    cv2.imwrite(os.path.join(output_dir, "contrast.png"), contrast)

    # 二值化 (Thresholding)
    _, thresh = cv2.threshold(contrast, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    cv2.imwrite(os.path.join(output_dir, "threshold.png"), thresh)

    # 放大圖片（2x）
    scale = 2
    resized = cv2.resize(thresh, None, fx=scale, fy=scale, interpolation=cv2.INTER_LINEAR)
    cv2.imwrite(os.path.join(output_dir, "resized.png"), resized)

    print(f"📁 所有預處理圖片已儲存至：{output_dir}")

if __name__ == "__main__":
    # 使用方式：你可以改這裡的路徑
    input_image = "image/7786a4sd.png"
    output_folder = "preprocess_steps"
    preprocess_debug(input_image, output_folder)
