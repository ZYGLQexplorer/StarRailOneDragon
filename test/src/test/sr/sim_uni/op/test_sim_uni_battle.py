import unittest

import test
from sr.context import get_context
from sr.image.sceenshot import screen_state
from sr.screen_area.dialog import ScreenDialog
from sr.sim_uni.op.sim_uni_battle import SimUniEnterFight


class TestSimUniBattle(test.SrTestBase):

    def __init__(self, *args, **kwargs):
        test.SrTestBase.__init__(self, *args, **kwargs)

    def test_get_screen_state(self):
        ctx = get_context()
        ctx.init_ocr_matcher()
        ctx.init_image_matcher()

        op = SimUniEnterFight(ctx)

        screen = self.get_test_image('after_elite_curio')
        self.assertEqual(screen_state.ScreenState.SIM_CURIOS.value,
                         op._get_screen_state(screen))

        screen = self.get_test_image('recover_technique_point')
        self.assertEqual(ScreenDialog.FAST_RECOVER_TITLE.value.text,
                         op._get_screen_state(screen))
