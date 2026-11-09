# Chrome 小恐龍自動遊玩機器人開發與除錯紀錄

## 1. 專案背景與需求
- **目標**：修改 `dino.ipynb`，透過 `pyautogui` 自動截取畫面並控制 Chrome 小恐龍 (`chrome://dino`) 自動跳躍與避開障礙物（地面仙人掌、空中飛鳥）。
- **環境**：Windows, Python 3.12 (`iem_python`), Jupyter Notebook, Chrome 瀏覽器（使用**深色模式**，背景顏色為 `(32, 33, 36)`，障礙物顏色為 `(161, 161, 161)`）。

---

## 2. 遭遇的問題與演進過程

### 問題一：預設座標與深色模式不適配
- **現象**：初始程式碼是針對舊版亮色模式設計，在深色模式下完全無法運作。
- **解決**：
  - 加入**即時滑鼠座標與顏色追蹤器（Calibration Tool）**，讓使用者能夠隨時將滑鼠移到畫面上取得真實的 `x`、`y` 座標與 RGB 顏色。
  - 將亮度門檻反轉：背景為深色（亮度低），障礙物為亮色（亮度高），改用大於門檻值（`LIGHT_PIXEL_THRESHOLD = 100` 或 `120`）來判定障礙物。

### 問題二：小恐龍起初跳不起來 / 撞到障礙物
- **原因**：
  - `pyautogui` 的 `is_pressed('esc')` 屬性不存在，導致程式執行 2 秒後拋出 `AttributeError` 提早終止。
  - 偵測區域的 X、Y 座標與寬高未對準實際遊戲中的障礙物通過位置。
- **解決**：
  - 修正迴圈邏輯，移除錯誤的 `is_pressed`，改用無限迴圈搭配 `KeyboardInterrupt` / Jupyter 停止按鈕。
  - 透過使用者提供的全螢幕截圖與滑鼠追蹤器，將偵測區域逐步修正為精準的座標（最終定案為 **`X = 110, Y = 480`** 開始，寬度 `140`、高度 `85`）。

### 問題三：亮色像素數固定在 300 左右，判定永遠為 True
- **原因**：原本使用「固定計算亮像素總數」的方法，但偵測區域稍微涵蓋到了地面線或跑道裝飾，導致未出現障礙物時就有約 300 個亮像素。
- **解決**：
  - 改用**「動態亮度差偵測法」**：
    1. 程式啟動時先截取當下畫面計算背景的**基準亮度** (`base_brightness`)。
    2. 隨時計算當前畫面的平均亮度，只要亮度差 (`brightness_diff`) 大於設定的門檻值，就代表有亮色的仙人掌或鳥類進入偵測區。

### 問題四：遇到鳥（翼龍）會漏判
- **原因**：鳥的飛行高度比地面仙人掌高，原本設定的狹窄偵測區抓不到空中的鳥。
- **解決**：
  - 擴大偵測區域的垂直範圍，改用**「全高度合併大方框」**：`DETECTION_REGION = (110, 480, 140, 85)`，同時涵蓋低處仙人掌與高處飛鳥。

### 問題五：遊戲分數變高、速度加快時容易撞到
- **原因**：速度變快後，原本的偵測距離和反應時間來不及。
- **解決**：
  - **拉寬偵測區**：將寬度從 `90` 擴大到 `140`，讓小恐龍能更早（距離更遠）看到障礙物並提前起跳。
  - **加快 FPS**：將迴圈延遲 `LOOP_DELAY` 從 `0.01` 縮短為 `0.005`，提升每秒檢測頻率。

---

## 3. 最終定案核心程式碼邏輯 (`dino.ipynb`)

```python
import time
import warnings
import pyautogui as pyg

warnings.filterwarnings('ignore', category=DeprecationWarning)

# 偵測區域：(X, Y, 寬度, 高度) - 涵蓋地面與空中，並向右延伸以提早預判高速障礙物
DETECTION_REGION = (110, 480, 140, 85)
LOOP_DELAY = 0.005  # 高速運行時縮短延遲，提升反應幀數

def get_average_brightness(image):
    \"\"\"計算偵測區域內的平均亮度（0~255）。\"\"\"
    total = 0
    pixels = list(image.convert('RGB').getdata())
    for red, green, blue in pixels:
        total += (red + green + blue) / 3
    return total / len(pixels)

pyg.PAUSE = 0
print('請在 2 秒內點擊切換到遊戲視窗...')
pyg.sleep(2)
pyg.press('space')  # 開始遊戲

# 記錄背景基準亮度
base_brightness = get_average_brightness(pyg.screenshot(region=DETECTION_REGION))
print(f'背景基準亮度: {base_brightness:.2f}')

was_obstacle_near = False
print('高速自適應恐龍機器人運行中...')
try:
    while True:
        screen = pyg.screenshot(region=DETECTION_REGION)
        current_brightness = get_average_brightness(screen)
        
        # 動態比較亮度差
        brightness_diff = current_brightness - base_brightness
        obstacle_near = brightness_diff > 1.5

        print(f'亮度差: {brightness_diff:.2f} | 判定跳躍: {obstacle_near}', end='\\r')

        if obstacle_near and not was_obstacle_near:
            pyg.press('space')
        was_obstacle_near = obstacle_near
        time.sleep(LOOP_DELAY)
except KeyboardInterrupt:
    print('\n使用者手動停止。')
finally:
    pyg.keyUp('space')
    print('恐龍機器人已停止。')
```
