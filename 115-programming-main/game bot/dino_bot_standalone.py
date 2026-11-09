
import time
import warnings
import pyautogui as pyg

warnings.filterwarnings('ignore', category=DeprecationWarning)

# 偵測區域格式：(螢幕 x, 螢幕 y, 寬度, 高度)
DETECTION_REGION = (165, 585, 85, 30)
LIGHT_PIXEL_THRESHOLD = 100
MIN_OBSTACLE_PIXELS = 3
LOOP_DELAY = 0.01

def get_obstacle_pixels(image):
    obstacle_pixels = 0
    for red, green, blue in image.convert('RGB').getdata():
        if (red + green + blue) / 3 > LIGHT_PIXEL_THRESHOLD:
            obstacle_pixels += 1
    return obstacle_pixels

pyg.PAUSE = 0
print('========================================')
print(' 恐龍機器人已啟動！請將此視窗與遊戲左右並排。')
print(' 關閉此視窗或按下 Ctrl+C 即可停止。')
print('========================================')
print('請在 2 秒內點擊遊戲視窗...')
pyg.sleep(2)
pyg.press('space')

was_obstacle_near = False
try:
    while True:
        screen = pyg.screenshot(region=DETECTION_REGION)
        pixel_count = get_obstacle_pixels(screen)
        obstacle_near = pixel_count >= MIN_OBSTACLE_PIXELS

        print(f'亮色像素數: {pixel_count} | 判定跳躍: {obstacle_near}', end='')

        if obstacle_near and not was_obstacle_near:
            pyg.press('space')
        was_obstacle_near = obstacle_near
        time.sleep(LOOP_DELAY)
except KeyboardInterrupt:
    print('
機器人已手動停止。')
