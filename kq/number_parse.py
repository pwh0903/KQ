import os
import cv2
import numpy as np


def get_board_money(board_window):
    dot_name = 'dot'
    img_folder = 'pot_number'
    nums_list = dict()
    imgs = os.listdir(img_folder)
    for img in imgs:
        if not img.endswith('.png'):
            continue
        file_name, file_extension = os.path.splitext(img)
        template = cv2.imread('{}/{}'.format(img_folder, img), 0)
        res = cv2.matchTemplate(board_window, template, cv2.TM_CCOEFF_NORMED)
        threshold = 0.95
        loc = np.where(res >= threshold)
        row, col = loc
        if len(row) > 0 and len(col) > 0:
            start_c = 0
            for c in col:
                diff_c = c - start_c
                if diff_c < 5:
                    start_c = c
                    continue
                start_c = c
                nums_list[c] = file_name
    num_position = [p for p in nums_list]
    num_position.sort()
    parsed_number = ''

    # find dot position in numbers
    find_dot = False
    count = 0
    for p in num_position[::-1]:
        if nums_list[p] == dot_name:
            find_dot = True
            continue
        if not find_dot:
            count += 1

    for p in num_position:
        if nums_list[p] == dot_name:
            continue
        parsed_number += nums_list[p]
    try:
        if find_dot:
            parsed_number = float(parsed_number) / 10 ** count
        else:
            parsed_number = float(parsed_number)
    except Exception as e:
        parsed_number = None
    return parsed_number


if __name__ == '__main__':
    x = 1000
    y = 435
    end_x = 1360
    end_y = 475
    test_imgs = os.listdir('poker')
    for img in test_imgs:
        print(img)
        if not img.endswith('png'):
            continue
        im = cv2.imread('poker/{}'.format(img), 0)
        pot_window = im[y:end_y, x:end_x]
        # ret, pot_window = cv2.threshold(pot_window, 160, 255, cv2.THRESH_BINARY)
        nums = get_board_money(pot_window)
        print(nums)
        cv2.imshow('option_window', pot_window)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

# im = cv2.imread('pot_num/7.png', 0)
# print(im)
# h, w = im.shape
# pot_window = im[int(148*h/543): int(165*h/543), int(650*w/1580): int(960*w/1580)]
# ret, im = cv2.threshold(im, 160, 255, cv2.THRESH_BINARY)
# nums = get_nums(pot_window)
# print(nums)

# ret, im = cv2.threshold(pot_window, 100, 255, cv2.THRESH_BINARY)


# r_start = 0
# for i in im:
#     if np.sum(i) == 0:
#         r_start += 1
#     else:
#         break
#
# im = im[r_start:]
#
# r_end = 0
# for i in im:
#     if np.sum(i) != 0:
#         r_end += 1
#     else:
#         break
#
# im = im[:r_end]
#
# count = 0
# while len(im.T) > 1:
#     c_start = 0
#     for c in im.T:
#         if np.sum(c) == 0:
#             c_start += 1
#         else:
#             break
#     im = im[:, c_start:]
#
#     c_end = 0
#     for c in im.T:
#         if np.sum(c) != 0:
#             c_end += 1
#         else:
#             break
#     num_img = im[:, :c_end]
#     cv2.imwrite('{}t.png'.format(count), num_img)
#     im = im[:, c_end:]
#     count += 1


# cv2.imshow('num', im)
# cv2.waitKey(0)
# cv2.destroyAllWindows()