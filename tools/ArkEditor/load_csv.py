import os
import csv
import cache_control

premise_path = "Premise.csv"
status_path = "Status.csv"
effect_path = "Effect.csv"
ability_path = "Ability.csv"
state_path = "CharacterState.csv"
experience_path = "Experience.csv"
juel_path = "Juel.csv"
talent_path = "Talent.csv"


def load_config():
    """载入配置文件"""
    with open(premise_path, encoding="utf-8") as now_file:
        now_read = csv.DictReader(now_file)
        for i in now_read:
            cache_control.premise_data[i["cid"]] = i["premise"]
            cache_control.premise_type_data.setdefault(i["premise_type"], set())
            cache_control.premise_type_data[i["premise_type"]].add(i["cid"])
    with open(status_path, encoding="utf-8") as now_file:
        now_read = csv.DictReader(now_file)
        for i in now_read:
            cache_control.status_data[i["cid"]] = i["status"]
            cache_control.status_type_data.setdefault(i["type"], [])
            cache_control.status_type_data[i["type"]].append(i["cid"])
    with open(effect_path, encoding="utf-8") as now_file:
        now_read = csv.DictReader(now_file)
        for i in now_read:
            cache_control.effect_data[i["cid"]] = i["effect"]
            cache_control.effect_type_data.setdefault(i["effect_type"], set())
            cache_control.effect_type_data[i["effect_type"]].add(i["cid"])
    with open(ability_path, encoding="utf-8") as now_file:
        now_read = csv.DictReader(now_file)
        read_flag = False
        for i in now_read:
            if read_flag == False:
                if i["cid"] != "能力对应类型和文字描述":
                    continue
                else:
                    read_flag = True
                    continue
            cache_control.ability_data[i["cid"]] = i["name"]
    with open(state_path, encoding="utf-8") as now_file:
        now_read = csv.DictReader(now_file)
        read_flag = False
        for i in now_read:
            if read_flag == False:
                if i["cid"] != "角色状态属性表":
                    continue
                else:
                    read_flag = True
                    continue
            cache_control.state_data[i["cid"]] = i["name"]
    with open(experience_path, encoding="utf-8") as now_file:
        now_read = csv.DictReader(now_file)
        read_flag = False
        for i in now_read:
            if read_flag == False:
                if i["cid"] != "经验名字":
                    continue
                else:
                    read_flag = True
                    continue
            cache_control.experience_data[i["cid"]] = i["name"]
    with open(juel_path, encoding="utf-8") as now_file:
        now_read = csv.DictReader(now_file)
        read_flag = False
        for i in now_read:
            if read_flag == False:
                if i["cid"] != "珠名字":
                    continue
                else:
                    read_flag = True
                    continue
            cache_control.juel_data[i["cid"]] = i["name"]
    with open(talent_path, encoding="utf-8") as now_file:
        now_read = csv.DictReader(now_file)
        read_flag = False
        for i in now_read:
            if read_flag == False:
                if i["cid"] != "素质对应类型和文字描述":
                    continue
                else:
                    read_flag = True
                    continue
            cache_control.talent_data[i["cid"]] = i["name"]
