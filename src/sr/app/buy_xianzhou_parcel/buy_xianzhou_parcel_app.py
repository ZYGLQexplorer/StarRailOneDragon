from basic.i18_utils import gt
from sr.app.application_base import Application
from sr.const import map_const, game_config_const
from sr.context import Context
from sr.operation import Operation
from sr.operation.combine import CombineOperation
from sr.operation.combine.transport import Transport
from sr.operation.unit.back_to_world import BackToWorld
from sr.operation.unit.interact import Interact, TalkInteract
from sr.operation.unit.move import MoveDirectly
from sr.operation.unit.store.buy_store_item import BuyStoreItem
from sr.operation.unit.store.click_store_item import ClickStoreItem
from sr.operation.unit.wait import WaitInSeconds


class BuyXianzhouParcelApp(Application):

    def __init__(self, ctx: Context):
        super().__init__(ctx, op_name=gt('购买过期邮包', 'ui'),
                         run_record=ctx.buy_xz_parcel_run_record)

    def _execute_one_round(self) -> int:
        ops = [
            Transport(self.ctx, map_const.P03_R02_SP02),
            MoveDirectly(self.ctx,
                         lm_info=self.ctx.ih.get_large_map(map_const.P03_R02_SP02.region),
                         target=map_const.P03_R02_SP08.lm_pos,
                         start=map_const.P03_R02_SP02.tp_pos),
            Interact(self.ctx, '茂贞', single_line=True),
            TalkInteract(self.ctx, '我想买个过期邮包试试手气', lcs_percent=0.55),
            WaitInSeconds(self.ctx, 1),
            ClickStoreItem(self.ctx, '逾期未取的贵重邮包', 0.8),
            WaitInSeconds(self.ctx, 1),
            BuyStoreItem(self.ctx, buy_max=True),
            BackToWorld(self.ctx)
        ]

        op = CombineOperation(self.ctx, ops=ops,
                              op_name=gt('购买过期包裹', 'ui'))

        if op.execute().success:
            return Operation.SUCCESS
        else:
            return Operation.FAIL

    def get_item_name_lcs_percent(self) -> float:
        lang = self.ctx.game_config.lang
        if lang == game_config_const.LANG_CN:
            return 0.8
        elif lang == game_config_const.LANG_EN:
            return 0.8
        return 0.8
