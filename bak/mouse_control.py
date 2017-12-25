import pyautogui

control_map = {
    'fold': (450, 565),
    'call': (590, 565),
    'check': (590, 565),
    'raise': (720, 565),
    'slider': (640, 520),
    'min': (550, 488),
    'pot': (690, 488),
    'max': (750, 488),
}


# screenWidth, screenHeight = pyautogui.size()
# print(screenHeight, screenWidth)
# pyautogui.moveTo(screenWidth / 2, screenHeight / 2)
# pyautogui.press('x', presses=2)

row, col = control_map.get('fold')
click_count = 2
pyautogui.click(row, col, clicks=click_count, interval=0.2)