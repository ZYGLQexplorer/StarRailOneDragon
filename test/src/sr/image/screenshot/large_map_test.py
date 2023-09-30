import cv2

from basic.img import cv2_utils
from basic.img.os import get_test_image
from sr.image.cnocr_matcher import CnOcrMatcher
from sr.image.image_holder import ImageHolder
from sr.image.sceenshot import large_map, LargeMapInfo
from sr.image.sceenshot.icon import save_template_image


def _test_get_planet_name():
    screen = get_test_image('large_map_1')
    cv2_utils.show_image(screen[30:100, 90:250], win_name='cut', wait=0)
    ocr = CnOcrMatcher()
    print(large_map.get_planet(screen, ocr))


def _test_cut_minus():
    screen = get_test_image('large_map_1')

    cut, mask = large_map.cut_minus_or_plus(screen)
    cv2.waitKey(0)
    save_template_image(cut, 'minus', 'origin')
    save_template_image(mask, 'minus', 'mask')

    cut, mask = large_map.cut_minus_or_plus(screen, minus=False)
    cv2.waitKey(0)
    save_template_image(cut, 'plus', 'origin')
    save_template_image(mask, 'plus', 'mask')

def _test_get_sp_mask_by_template_match():
    ih = ImageHolder()
    screen = get_test_image('large_map_htbgs')
    lm_info = LargeMapInfo()
    lm_info.origin = screen
    sp_mask, _ = large_map.get_sp_mask_by_template_match(lm_info, ih, show=True)
    cv2_utils.show_image(sp_mask, win_name='sp_mask', wait=0)


if __name__ == '__main__':
    _test_get_sp_mask_by_template_match()