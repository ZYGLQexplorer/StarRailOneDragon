from typing import List, Optional

from basic.i18_utils import gt
from sr.app.app_description import AppDescription, AppDescriptionEnum
from sr.app.app_run_record import AppRunRecord
from sr.app.application_base import Application
from sr.app.assignments.assignments_app import AssignmentsApp
from sr.app.buy_xianzhou_parcel.buy_xianzhou_parcel_app import BuyXianzhouParcelApp
from sr.app.daily_training.daily_training_app import DailyTrainingApp
from sr.app.echo_of_war.echo_of_war_app import EchoOfWarApp
from sr.app.email.email_app import EmailApp
from sr.app.nameless_honor.nameless_honor_app import NamelessHonorApp
from sr.app.support_character.support_character_app import SupportCharacterApp
from sr.app.trailblaze_power.trailblaze_power_app import TrailblazePower
from sr.app.treasures_lightward.treasures_lightward_app import TreasuresLightwardApp
from sr.app.world_patrol.world_patrol_app import WorldPatrol
from sr.context import Context
from sr.operation import Operation


class OneStopServiceApp(Application):

    def __init__(self, ctx: Context):
        super().__init__(ctx, op_name=gt('一条龙', 'ui'))
        self.app_list: List[AppDescription] = []
        run_app_list = ctx.one_stop_service_config.run_app_id_list
        for app_id in ctx.one_stop_service_config.order_app_id_list:
            if app_id not in run_app_list:
                continue
            OneStopServiceApp.update_app_run_record_before_start(app_id, self.ctx)
            record = OneStopServiceApp.get_app_run_record_by_id(app_id, self.ctx)

            if record.run_status_under_now != AppRunRecord.STATUS_SUCCESS:
                self.app_list.append(AppDescriptionEnum[app_id.upper()].value)

        self.app_idx: int = 0

    def _init_before_execute(self):
        super()._init_before_execute()
        self.app_idx = 0

    def _execute_one_round(self) -> int:
        if self.app_idx >= len(self.app_list):  # 有可能刚开始就所有任务都已经执行完了
            return Operation.SUCCESS
        app: Application = self.get_app_by_id(self.app_list[self.app_idx].id)
        app.init_context_before_start = False  # 一条龙开始时已经初始化了
        app.stop_context_after_stop = self.app_idx >= len(self.app_list)  # 只有最后一个任务结束会停止context

        result = app.execute()  # 暂时忽略结果 直接全部运行
        self.app_idx += 1

        if self.app_idx >= len(self.app_list):
            return Operation.SUCCESS
        else:
            return Operation.WAIT

    @property
    def current_execution_desc(self) -> str:
        """
        当前运行的描述 用于UI展示
        :return:
        """
        if self.app_idx >= len(self.app_list):
            return gt('无', 'ui')
        else:
            return gt(self.app_list[self.app_idx].cn, 'ui')

    @property
    def next_execution_desc(self) -> str:
        """
        下一步运行的描述 用于UI展示
        :return:
        """
        if self.app_idx >= len(self.app_list) - 1:
            return gt('无', 'ui')
        else:
            return gt(self.app_list[self.app_idx + 1].cn, 'ui')

    @staticmethod
    def get_app_by_id(app_id: str, ctx: Context) -> Optional[Application]:
        if app_id == AppDescriptionEnum.WORLD_PATROL.value.id:
            return WorldPatrol(ctx)
        elif app_id == AppDescriptionEnum.ASSIGNMENTS.value.id:
            return AssignmentsApp(ctx)
        elif app_id == AppDescriptionEnum.EMAIL.value.id:
            return EmailApp(ctx)
        elif app_id == AppDescriptionEnum.SUPPORT_CHARACTER.value.id:
            return SupportCharacterApp(ctx)
        elif app_id == AppDescriptionEnum.NAMELESS_HONOR.value.id:
            return NamelessHonorApp(ctx)
        elif app_id == AppDescriptionEnum.DAILY_TRAINING.value.id:
            return DailyTrainingApp(ctx)
        elif app_id == AppDescriptionEnum.BUY_XIANZHOU_PARCEL.value.id:
            return BuyXianzhouParcelApp(ctx)
        elif app_id == AppDescriptionEnum.TRAILBLAZE_POWER.value.id:
            return TrailblazePower(ctx)
        elif app_id == AppDescriptionEnum.ECHO_OF_WAR.value.id:
            return EchoOfWarApp(ctx)
        elif app_id == AppDescriptionEnum.TREASURES_LIGHTWARD.value.id:
            return TreasuresLightwardApp(ctx)
        elif app_id == AppDescriptionEnum.SIM_UNIVERSE.value.id:
            return sim_universe_app.SimUniApp(ctx)
        return None

    @staticmethod
    def get_app_run_record_by_id(app_id: str, ctx: Context) -> Optional[AppRunRecord]:
        if app_id == AppDescriptionEnum.WORLD_PATROL.value.id:
            return ctx.world_patrol_run_record
        elif app_id == AppDescriptionEnum.ASSIGNMENTS.value.id:
            return ctx.assignments_run_record
        elif app_id == AppDescriptionEnum.EMAIL.value.id:
            return ctx.email_run_record
        elif app_id == AppDescriptionEnum.SUPPORT_CHARACTER.value.id:
            return ctx.support_character_run_record
        elif app_id == AppDescriptionEnum.NAMELESS_HONOR.value.id:
            return ctx.nameless_honor_run_record
        elif app_id == AppDescriptionEnum.DAILY_TRAINING.value.id:
            return ctx.daily_training_run_record
        elif app_id == AppDescriptionEnum.BUY_XIANZHOU_PARCEL.value.id:
            return ctx.buy_xz_parcel_run_record
        elif app_id == AppDescriptionEnum.TRAILBLAZE_POWER.value.id:
            return ctx.tp_run_record
        elif app_id == AppDescriptionEnum.ECHO_OF_WAR.value.id:
            return ctx.echo_run_record
        elif app_id == AppDescriptionEnum.TREASURES_LIGHTWARD.value.id:
            return ctx.tl_run_record
        elif app_id == AppDescriptionEnum.SIM_UNIVERSE.value.id:
            return ctx.sim_uni_run_record
        return None

    @staticmethod
    def update_app_run_record_before_start(app_id: str, ctx: Context):
        """
        每次开始前 根据外部信息更新运行状态
        :param app_id:
        :return:
        """
        record: Optional[AppRunRecord] = OneStopServiceApp.get_app_run_record_by_id(app_id, ctx)
        if record is not None:
            record.check_and_update_status()