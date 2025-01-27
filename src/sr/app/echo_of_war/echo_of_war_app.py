from typing import Optional

from cv2.typing import MatLike

from basic import str_utils
from basic.i18_utils import gt
from basic.img import cv2_utils
from basic.log_utils import log
from sr.app.application_base import Application
from sr.app.echo_of_war.echo_of_war_config import EchoOfWarPlanItem
from sr.app.echo_of_war.echo_of_war_run_record import EchoOfWarRunRecord
from sr.context import Context
from sr.image.sceenshot import large_map
from sr.interastral_peace_guide.survival_index_mission import SurvivalIndexMission, SurvivalIndexMissionEnum
from sr.operation import Operation
from sr.operation.combine.challenge_ehco_of_war import ChallengeEchoOfWar
from sr.operation.unit.open_map import OpenMap


class EchoOfWarApp(Application):

    def __init__(self, ctx: Context):
        super().__init__(ctx, op_name=gt('历战余响', 'ui'),
                         run_record=ctx.echo_run_record)
        self.phase: int = 2
        self.power: int = 160

    def _execute_one_round(self) -> int:
        if self.phase == 0:  # 打开大地图
            op = OpenMap(self.ctx)
            if not op.execute().success:
                return Operation.FAIL
            else:
                self.phase += 1
                return Operation.WAIT
        elif self.phase == 1:  # 查看剩余体力
            screen: MatLike = self.screenshot()
            part, _ = cv2_utils.crop_image(screen, large_map.LARGE_MAP_POWER_RECT)
            ocr_result = self.ctx.ocr.ocr_for_single_line(part, strict_one_line=True)
            self.power = str_utils.get_positive_digits(ocr_result)
            log.info('当前体力 %d', self.power)
            self.phase += 1
            return Operation.WAIT
        elif self.phase == 2:  # 使用体力
            config = self.ctx.echo_config
            config.check_plan_finished()
            plan: Optional[EchoOfWarPlanItem] = config.next_plan_item
            if plan is None:
                return Operation.SUCCESS

            point: Optional[SurvivalIndexMission] = SurvivalIndexMissionEnum.get_by_unique_id(plan['mission_id'])

            run_times: int = self.power // point.power

            record: EchoOfWarRunRecord = self.run_record
            if record.left_times < run_times:
                run_times = record.left_times

            if run_times == 0:
                return Operation.SUCCESS

            if run_times + plan['run_times'] > plan['plan_times']:
                run_times = plan['plan_times'] - plan['run_times']

            def on_battle_success():
                self.power -= point.power
                log.info('消耗体力: %d, 剩余体力: %d', point.power, self.power)
                plan['run_times'] += 1
                log.info('副本完成次数: %d, 计划次数: %d', plan['run_times'], plan['plan_times'])
                record.left_times = record.left_times - 1
                log.info('本周历战余响剩余次数: %d', record.left_times)
                config.save()
                record.update_status(AppRunRecord.STATUS_RUNNING)

            op = ChallengeEchoOfWar(self.ctx, point.tp, plan['team_num'], run_times,
                                    support=plan['support'] if plan['support'] != 'none' else None,
                                    on_battle_success=on_battle_success)
            if op.execute().success:
                return Operation.WAIT
            else:  # 挑战
                return Operation.RETRY
