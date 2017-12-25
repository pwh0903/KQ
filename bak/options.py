import cv2
import numpy as np
import os


def cut_blank(im):
    r_start = 0
    for i in im:
        if np.sum(i) == 0:
            r_start += 1
        else:
            break

    im = im[r_start:]

    r_end = 0
    for i in im:
        if np.sum(i) != 0:
            r_end += 1
        else:
            break

    im = im[:r_end]

    c_start = 0
    for c in im.T:
        if np.sum(c) == 0:
            c_start += 1
        else:
            break
    im = im[:, c_start:]

    # c_end = 0
    # for c in im.T[::-1]:
    #     if np.sum(c) == 0:
    #         c_end += 1
    #     else:
    #         break
    # if c_end != 0:
    #     im = im[:, :c_end]

    return im


# get options from option window
def get_options(option_img):
    print(option_img.shape)
    options_list = []
    imgs = os.listdir('controls')
    for img in imgs:
        if not img.endswith('png'):
            continue
        file_name, file_extension = os.path.splitext(img)
        template = cv2.imread('controls/{}'.format(img), 0)
        # print(template.shape)
        res = cv2.matchTemplate(option_img, template, cv2.TM_CCOEFF_NORMED)
        threshold = 0.7
        loc = np.where(res >= threshold)
        a1, a2 = loc
        if len(a1) > 0 and len(a2) > 0:
            options_list.append(file_name)
    return options_list


if __name__ == '__main__':
    test_imgs = os.listdir('poker')
    for img in test_imgs:
        if not img.endswith('.png'):
            continue
        im = cv2.imread('poker/{}'.format(img), 0)
        control_start_x = 140
        control_start_y = 1370
        control_end_x = 1930
        control_end_y = 1650
        control_window = im[control_start_y:control_end_y, control_start_x:control_end_x]
        # ret, control_window = cv2.threshold(control_window, 95, 255, cv2.THRESH_BINARY)
        option_list = get_options(control_window)
        print(option_list)
        cv2.imshow('option_window', control_window)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

# get option screenshot and save them
# im = cv2.imread('poker/1.png', 0)
#
# option_start_x = 145
# option_start_y = 465
# option_w = 510
# option_h = 105
#
# option_window = im[option_start_y:option_start_y+option_h, option_start_x:option_start_x+option_w]
#
# print(type(im))
# print(im.shape)
#
# cv2.imshow('option', option_window)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

# control_imgs = os.listdir('tmp')
# print(control_imgs)
# for img in control_imgs:
#     if not img.endswith('.PNG'):
#         continue
#     im_name = img.strip('.PNG')
#     im = cv2.imread('tmp/{}'.format(img), 0)
#     ret, im = cv2.threshold(im, 95, 255, cv2.THRESH_BINARY)
#     im = cut_blank(im)
#     cv2.imwrite('controls/{}.png'.format(im_name), im)
# cv2.write('controls/{}.png'.format(control_name))

# print(im)
# cv2.imshow('option', im)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
