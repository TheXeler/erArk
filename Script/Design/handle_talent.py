import datetime
from types import FunctionType
from Script.Design import (
    settle_behavior,
    character,
    character_handle,
    map_handle,
    attr_calculation,
    game_time,
    cooking,
    update,
    attr_text,
    handle_instruct,
    character_behavior,
    basement,
)
from Script.Core import cache_control, constant, constant_effect, game_type, get_text
from Script.Config import game_config, normal_config
from Script.UI.Moudle import draw
from Script.UI.Panel import event_option_panel

import random

_: FunctionType = get_text._
""" 翻译api """
cache: game_type.Cache = cache_control.cache
""" 游戏缓存数据 """

line_feed = draw.NormalDraw()
""" 换行绘制对象 """
line_feed.text = "\n"
line_feed.width = 1
window_width = normal_config.config_normal.text_width
""" 屏幕宽度 """

def gain_talent(character_id: int, now_gain_type: int, traget_talent_id = 0):
    """
    结算可以获得的素质\n
    Keyword arguments:
    character_id -- 角色id\n
    now_gain_type -- 素质获得类型(0随时自动，1手动，2指令绑定，3睡觉自动)\n
    """
    character_data: game_type.Character = cache.character_data[character_id]
    # 遍历全素质获得
    for gain_talent_cid in game_config.config_talent_gain:
        gain_talent_data = game_config.config_talent_gain[gain_talent_cid]
        gain_type = gain_talent_data.gain_type
        talent_id = gain_talent_data.talent_id

        # 手动结算的话跳过判断直接获得对应素质
        judge = 0
        if now_gain_type == 1 and traget_talent_id == talent_id:
            judge = 1
        # 需要为对应的结算时机，而且NPC没有该素质
        elif gain_type != 1 and gain_type == now_gain_type and character_data.talent[talent_id] == 0:

            # 以&为分割判定是否有多个需求
            if "&" not in gain_talent_data.gain_need:
                need_list = []
                need_list.append(gain_talent_data.gain_need)
            else:
                need_list = gain_talent_data.gain_need.split('&')
            judge, reason = attr_calculation.judge_require(need_list, character_id)

        # 如果符合获得条件，则获得该素质
        if judge:
            character_data.talent[talent_id] = 1
            talent_name = game_config.config_talent[talent_id].name

            # 触发对应的二段行为结算
            if gain_talent_data.second_behavior_id:
                second_behavior_id = gain_talent_data.second_behavior_id
                character_data.second_behavior[second_behavior_id] = 1

            # 判断是否需要进行替代旧素质
            if gain_talent_data.replace_talent_id:
                old_talent_id = gain_talent_data.replace_talent_id
                character_data.talent[old_talent_id] = 0

            now_draw_succed = draw.WaitDraw()
            now_draw_succed.text = f"\n{character_data.name}获得了{talent_name}\n"
            now_draw_succed.draw()
    # print(f"debug {character_data.name}的睡觉结算素质结束，judge = {judge}")

    # 特殊素质获得
    # if now_gain_type == 0:
    #     npc_gain_hypnosis_talent(character_id)

def have_hypnosis_talent():
    """
    验证是否有催眠系素质\n
    """
    pl_character_data = cache.character_data[0]
    for talent_id in [331,332,333,334]:
        if pl_character_data.talent[talent_id]:
            return talent_id
    return 0

def have_hormone_talent():
    """
    验证是否有激素系素质\n
    """
    pl_character_data = cache.character_data[0]
    for talent_id in [306,305,304]:
        if pl_character_data.talent[talent_id]:
            return talent_id
    return 0

def have_visual_talent():
    """
    验证是否有视觉系素质\n
    """
    pl_character_data = cache.character_data[0]
    for talent_id in [309,308,307]:
        if pl_character_data.talent[talent_id]:
            return talent_id
    return 0

def have_tactile_talent():
    """
    验证是否有触觉系素质\n
    """
    pl_character_data = cache.character_data[0]
    for talent_id in [312,311,310]:
        if pl_character_data.talent[talent_id]:
            return talent_id
    return 0

def npc_gain_hypnosis_talent(character_id: int):
    """
    干员获得被催眠素质\n
    """
    pl_character_data = cache.character_data[0]
    character_data = cache.character_data[character_id]
    if character_data.hypnosis.hypnosis_degree < 1:
        return

    # 初始化催眠字典，分别是催眠深度，前置素质，对应的二段行为
    hypnosis_dict = {}
    hypnosis_dict[71] = [50, 331, 1501]
    hypnosis_dict[72] = [100, 332, 1502]
    hypnosis_dict[73] = [200, 334, 1503]
    for talent_id in hypnosis_dict:
        # 如果已经有该素质则跳过
        if character_data.talent[talent_id]:
            continue
        # 如果玩家没有对应的前置素质则跳过
        if not pl_character_data.talent[hypnosis_dict[talent_id][1]]:
            continue

        if character_data.hypnosis.hypnosis_degree >= hypnosis_dict[talent_id][0]:
            character_data.talent[talent_id] = 1
            talent_name = game_config.config_talent[talent_id].name
            # 触发对应的二段行为结算
            character_data.second_behavior[hypnosis_dict[talent_id][2]] = 1
            # 替换旧素质
            if talent_id > 71:
                old_talent_id = talent_id - 1
                character_data.talent[old_talent_id] = 0
            # 绘制获得素质提示
            now_draw_succed = draw.WaitDraw()
            now_draw_succed.text = f"\n○{character_data.name}的催眠深度达到{hypnosis_dict[talent_id][0]:}%，获得了[{talent_name}]\n"
            now_draw_succed.draw()
            break

