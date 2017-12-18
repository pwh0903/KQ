import pyautogui

screenWidth, screenHeight = pyautogui.size()
pyautogui.moveTo(screenWidth / 2, screenHeight / 2)
while True:
    pyautogui.press('x', presses=2)
