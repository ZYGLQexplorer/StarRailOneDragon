import unittest
from typing import List

import test
from sr.sim_uni.sim_uni_challenge_config import SimUniChallengeConfig
from sr.context import get_context
from sr.sim_uni.op.sim_uni_choose_curio import SimUniChooseCurio, SimUniDropCurio
from sr.sim_uni.sim_uni_const import SimUniCurioEnum, SimUniCurio
from sr.sim_uni.sim_uni_challenge_config import SimUniChallengeConfig


class TestChooseSimUniCurio(test.SrTestBase):

    def __init__(self, *args, **kwargs):
        test.SrTestBase.__init__(self, *args, **kwargs)

    def test_get_curio_pos(self):
        ctx = get_context()
        ctx.init_ocr_matcher()
        screen = self.get_test_image('1')

        op = SimUniChooseCurio(ctx)

        curio_list = op._get_curio_pos_2(screen)

        self.assertEqual(3, len(curio_list))

        answer: List[SimUniCurio] = [
            SimUniCurioEnum.CURIO_011.value,
            SimUniCurioEnum.CURIO_024.value,
            SimUniCurioEnum.CURIO_022.value,
        ]
        for i in range(3):
            self.assertTrue(curio_list[i].data in answer)

    def test_drop_get_curio_pos(self):
        ctx = get_context()
        ctx.init_ocr_matcher()

        op = SimUniDropCurio(ctx)

        screen = self.get_test_image('drop_2')
        curio_list = op._get_curio_pos(screen)
        answer: List[SimUniCurio] = [
            SimUniCurioEnum.CURIO_011.value,
            SimUniCurioEnum.CURIO_006.value,
        ]
        self.assertEqual(len(answer), len(curio_list))
        for i in range(len(answer)):
            self.assertTrue(curio_list[i].data in answer)

        screen = self.get_test_image('drop_1')
        curio_list = op._get_curio_pos(screen)
        answer: List[SimUniCurio] = [
            SimUniCurioEnum.CURIO_026.value,
        ]
        self.assertEqual(len(answer), len(curio_list))
        for i in range(len(answer)):
            self.assertTrue(curio_list[i].data in answer)

    def test_drop_get_curio_by_priority(self):
        ctx = get_context()
        ctx.init_ocr_matcher()
        screen = self.get_test_image('drop_2')

        config = SimUniChallengeConfig(9, mock=True)
        op = SimUniDropCurio(ctx, config)
        config.curio_priority = [SimUniCurioEnum.CURIO_011.name, SimUniCurioEnum.CURIO_006.name]

        curio_list = op._get_curio_pos(screen)
        mr = op._get_curio_to_choose(curio_list)

        self.assertEqual(SimUniCurioEnum.CURIO_006.value, mr.data)

    def test_op(self):
        ctx = get_context()
        ctx.start_running()

        op = SimUniChooseCurio(ctx)
        op.execute()

    def test_drop_op(self):
        ctx = get_context()
        ctx.start_running()
        config = SimUniChallengeConfig(8)

        op = SimUniDropCurio(ctx, config)
        op.execute()
