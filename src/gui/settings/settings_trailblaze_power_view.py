from typing import Optional, List, Callable

import flet as ft

from basic.i18_utils import gt
from gui import components
from gui.components.character_input import CharacterInput
from gui.settings import gui_config
from gui.settings.gui_config import ThemeColors
from gui.sr_basic_view import SrBasicView
from sr.app.trailblaze_power.trailblaze_power_config import TrailblazePowerPlanItem
from sr.const.character_const import CHARACTER_LIST
from sr.context import Context
from sr.interastral_peace_guide.survival_index_mission import SurvivalIndexCategory, SurvivalIndexCategoryEnum, \
    SurvivalIndexMission, SurvivalIndexMissionEnum


class PlanListItem(ft.Row):

    def __init__(self, item: Optional[TrailblazePowerPlanItem] = None,
                 on_value_changed: Optional[Callable] = None,
                 on_click_up: Optional[Callable] = None,
                 on_click_del: Optional[Callable] = None,
                 on_click_support: Optional[Callable] = None):
        self.value: Optional[TrailblazePowerPlanItem] = item
        if self.value is None:
            self.value = TrailblazePowerPlanItem(
                point_id=SurvivalIndexMissionEnum.BUD_1_YLL_1.value.unique_id,
                mission_id=SurvivalIndexMissionEnum.BUD_1_YLL_1.value.unique_id,
                plan_times=1, run_times=0,
                team_num=1, support='none')
        self.category_dropdown = ft.Dropdown(options=[
            ft.dropdown.Option(text=i.value.ui_cn, key=i.value.ui_cn) for i in SurvivalIndexCategoryEnum if i != SurvivalIndexCategoryEnum.ECHO_OF_WAR
        ],
            label='类目', width=100, on_change=self._on_category_changed)
        self.tp_dropdown = ft.Dropdown(label='挑战关卡', width=180, on_change=self._on_tp_changed)
        self.team_num_dropdown = ft.Dropdown(options=[ft.dropdown.Option(text=str(i), key=str(i)) for i in range(1, 10)],
                                             label='使用配队', width=80, on_change=self._on_team_num_changed)
        self.support_dropdown = ft.Dropdown(label='支援', value='none', disabled=True, width=80,
                                            options=[ft.dropdown.Option(text='无', key='none')])
        for c in CHARACTER_LIST:
            self.support_dropdown.options.append(
                ft.dropdown.Option(text=gt(c.cn, 'ui'), key=c.id)
            )
        self.plan_times_input = ft.TextField(label='计划次数', keyboard_type=ft.KeyboardType.NUMBER,
                                             width=80, on_change=self._on_plan_times_changed)
        self.run_times_input = ft.TextField(label='本轮完成', keyboard_type=ft.KeyboardType.NUMBER,
                                            width=80, on_change=self._on_run_times_changed)
        self.chosen_point: Optional[SurvivalIndexMission] = SurvivalIndexMissionEnum.get_by_unique_id(self.value['mission_id'])

        self.category_dropdown.value = self.chosen_point.cate.ui_cn
        self._update_tp_dropdown_list()
        self.tp_dropdown.value = self.chosen_point.unique_id
        self.team_num_dropdown.value = self.value['team_num']
        self.support_dropdown.value = self.value['support']
        self.plan_times_input.value = self.value['plan_times']
        self.run_times_input.value = self.value['run_times']
        self.value_changed_callback = on_value_changed

        self.up_app_btn = ft.IconButton(icon=ft.icons.ARROW_CIRCLE_UP_OUTLINED, data=id(self), on_click=on_click_up)
        self.del_btn = ft.IconButton(icon=ft.icons.DELETE_FOREVER_OUTLINED, data=id(self), on_click=on_click_del)

        super().__init__(controls=[self.category_dropdown, self.tp_dropdown,
                                   self.team_num_dropdown,
                                   ft.Container(content=self.support_dropdown, on_click=on_click_support, data=id(self)),
                                   self.run_times_input, self.plan_times_input,
                                   self.up_app_btn, self.del_btn])

    def _update_tp_dropdown_list(self):
        cate: SurvivalIndexCategory = SurvivalIndexCategoryEnum.get_by_ui_cn(self.category_dropdown.value)
        point_list: List[SurvivalIndexMission] = SurvivalIndexMissionEnum.get_list_by_category(cate)
        if point_list is None:
            point_list = []
        self.tp_dropdown.options = [ft.dropdown.Option(text=i.ui_cn, key=i.unique_id) for i in point_list]
        self.tp_dropdown.value = self.tp_dropdown.options[0].key

    def _on_category_changed(self, e):
        self._update_tp_dropdown_list()
        self.plan_times_input.value = 1
        self.run_times_input.value = 0
        self._update_value()
        self._update()
        self._on_value_changed()

    def _on_tp_changed(self, e):
        self.plan_times_input.value = 1
        self.run_times_input.value = 0
        self._update_value()
        self._update()
        self._on_value_changed()

    def _on_team_num_changed(self, e):
        self._update_value()
        self._on_value_changed()

    def _on_plan_times_changed(self, e):
        if self.plan_times_input.value == '':
            self.plan_times_input.value = 0
        if int(self.run_times_input.value) > int(self.plan_times_input.value):
            self.run_times_input.value = 0
            self.update()
        self._update_value()
        self._on_value_changed()

    def _on_run_times_changed(self, e):
        if self.run_times_input.value == '':
            self.run_times_input.value = 0
        elif int(self.run_times_input.value) > int(self.plan_times_input.value):
            self.run_times_input.value = 0
            self.update()
        self._update_value()
        self._on_value_changed()

    def _update_value(self):
        self.value['point_id'] = self.tp_dropdown.value
        self.value['mission_id'] = self.tp_dropdown.value
        self.value['team_num'] = int(self.team_num_dropdown.value)
        self.value['plan_times'] = int(self.plan_times_input.value)
        self.value['run_times'] = int(self.run_times_input.value)
        self.value['support'] = self.support_dropdown.value

    def _update(self):
        if self.page is not None:
            self.update()

    def update_support(self, c_id: Optional[str]):
        """
        更新使用的支援角色
        :param c_id: 角色ID
        :return:
        """
        if c_id is None:
            c_id = 'none'
        if self.support_dropdown.value == c_id:
            return
        self.support_dropdown.value = c_id
        self._update()
        self._update_value()
        self._on_value_changed()

    def _on_value_changed(self):
        if self.value_changed_callback is not None:
            self.value_changed_callback()


class PlanList(ft.ListView):

    def __init__(self, ctx: Context, on_click_support: Callable):
        self.ctx: Context = ctx
        plan_item_list: List[TrailblazePowerPlanItem] = self.ctx.tp_config.plan_list

        super().__init__(controls=[self._list_view_item(i) for i in plan_item_list])
        self.add_btn = ft.Container(components.RectOutlinedButton(text='+', on_click=self._on_add_click),
                                    margin=ft.margin.only(top=5))
        self.controls.append(self.add_btn)
        self.click_support_callback: Callable = on_click_support

    def refresh_by_config(self):
        plan_item_list: List[TrailblazePowerPlanItem] = self.ctx.tp_config.plan_list
        self.controls = [self._list_view_item(i) for i in plan_item_list]
        self.controls.append(self.add_btn)
        self.update()

    def _list_view_item(self, plan_item: Optional[TrailblazePowerPlanItem] = None) -> ft.Container:
        theme: ThemeColors = gui_config.theme()
        return ft.Container(
                content=PlanListItem(plan_item,
                                     on_value_changed=self._on_list_item_value_changed,
                                     on_click_up=self._on_click_item_up,
                                     on_click_del=self._on_item_click_del,
                                     on_click_support=self._on_click_support),
                border=ft.border.only(bottom=ft.border.BorderSide(1, theme['divider_color'])),
                padding=10
            )

    def _on_add_click(self, e):
        self.controls.append(self._list_view_item())
        last = len(self.controls) - 1
        tmp = self.controls[last - 1]
        self.controls[last - 1] = self.controls[last]
        self.controls[last] = tmp
        self.update()
        self._on_list_item_value_changed()

    def _on_list_item_value_changed(self):
        plan_item_list: List[TrailblazePowerPlanItem] = []
        for container in self.controls:
            item = container.content
            if type(item) == PlanListItem:
                plan_item_list.append(item.value)
        self.ctx.tp_config.plan_list = plan_item_list

    def _on_click_item_up(self, e):
        target_idx = self._get_item_event_idx(e)

        if target_idx <= 0:
            return

        temp = self.controls[target_idx - 1]
        self.controls[target_idx - 1] = self.controls[target_idx]
        self.controls[target_idx] = temp

        self.update()
        self._on_list_item_value_changed()

    def _on_item_click_del(self, e):
        target_idx = self._get_item_event_idx(e)
        if target_idx == - 1:
            return

        self.controls.pop(target_idx)
        self.update()
        self._on_list_item_value_changed()

    def _on_click_support(self, e):
        target_idx = self._get_item_event_idx(e)
        if target_idx == - 1:
            return

        if self.click_support_callback is not None:
            self.click_support_callback(self.controls[target_idx].content)

    def _get_item_event_idx(self, e) -> int:
        """
        获取事件对应的行明细下标
        :param e: 事件
        :return: 下标
        """
        target_idx: int = -1
        for i in range(len(self.controls)):
            item = self.controls[i].content
            if type(item) == PlanListItem and id(item) == e.control.data:
                target_idx = i
                break
        return target_idx


class SettingsTrailblazePowerView(SrBasicView, ft.Row):

    def __init__(self, page: ft.Page, ctx: Context):
        SrBasicView.__init__(self, page, ctx)
        plan_title = components.CardTitleText(gt('体力规划', 'ui'))
        self.plan_list = PlanList(ctx, self.show_choose_support_character)
        plan_card = components.Card(self.plan_list, plan_title, width=800)

        self.character_card = CharacterInput(ctx.ih, max_chosen_num=1, on_value_changed=self._on_choose_support)
        self.character_card.visible = False

        ft.Row.__init__(self, controls=[plan_card, self.character_card], spacing=10)

        self.chosen_plan_item: Optional[PlanListItem] = None

    def handle_after_show(self):
        self.plan_list.refresh_by_config()

    def show_choose_support_character(self, target: PlanListItem):
        self.chosen_plan_item = target
        chosen_point: Optional[SurvivalIndexMission] = SurvivalIndexMissionEnum.get_by_unique_id(target.value['mission_id'])
        self.character_card.update_title('%s %s' % (gt('支援角色', 'ui'), chosen_point.ui_cn))
        chosen_list: List[str] = []
        if target.support_dropdown.value is not None and target.support_dropdown.value != 'none':
            chosen_list.append(target.support_dropdown.value)
        self.character_card.update_chosen_list(chosen_list)
        self.character_card.visible = True
        self.character_card.update()

    def _on_choose_support(self, chosen_id_list: List[str]):
        """
        选中角色后的回调 更新计划中的支援角色
        :param chosen_id_list:
        :return:
        """
        if self.chosen_plan_item is None:
            return

        self.chosen_plan_item.update_support(chosen_id_list[0] if len(chosen_id_list) > 0 else None)
        self.chosen_plan_item = None
        self.character_card.visible = False
        self.character_card.update()


_settings_trailblaze_power_view: Optional[SettingsTrailblazePowerView] = None


def get(page: ft.Page, ctx: Context) -> SettingsTrailblazePowerView:
    global _settings_trailblaze_power_view
    if _settings_trailblaze_power_view is None:
        _settings_trailblaze_power_view = SettingsTrailblazePowerView(page, ctx)
    return _settings_trailblaze_power_view
