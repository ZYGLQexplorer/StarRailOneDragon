import time

from cv2.typing import MatLike

from basic import str_utils
from basic.i18_utils import gt
from sr.context import Context
from sr.image.sceenshot import battle
from sr.operation import Operation


class WaitBattleReward(Operation):

    """
    需要已经在进入战斗了才能用
    等待战斗结束领取奖励的页面 - 出现【挑战成功】或【挑战失败】
    """

    def __init__(self, ctx: Context, timeout_seconds: int = 1200):
        super().__init__(ctx, try_times=3, op_name=gt('等待战斗结束领取奖励', 'ui'))
        self.start_time: float = 0
        self.timeout_seconds: int = timeout_seconds

    def _init_before_execute(self):
        self.start_time = time.time()

    def _execute_one_round(self) -> int:
        screen: MatLike = self.screenshot()

        battle_status = battle.get_battle_status(screen, self.ctx.im)
        if battle_status == battle.IN_WORLD:  # 以防有什么特殊情况退出战斗了卡住 这里判断到不在战斗就退出
            return Operation.FAIL

        battle_result: str = battle.get_battle_result_str(screen, self.ctx.ocr)

        if str_utils.find_by_lcs(gt('挑战成功', 'ocr'), battle_result, 0.5) or \
            str_utils.find_by_lcs(gt('挑战失败', 'ocr'), battle_result, 0.5):
            return Operation.SUCCESS

        if time.time() - self.start_time > self.timeout_seconds:  # 应该没有需要真么久的战斗吧
            return Operation.FAIL

        time.sleep(1)
        return Operation.WAIT

    def on_resume(self):
        self.start_time = self.pause_end_time - (self.pause_start_time - self.start_time)