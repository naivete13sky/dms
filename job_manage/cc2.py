# 自定义排序规则
def my_compare(x, y):
    if x > y:
        return 1
    elif x < y:
        return -1
    return 0

def list_sort_test():
    pass
    import functools
    strs = [3, 4, 1, 2]
    # 分别使用sorted和list.sort
    print(strs)
    print(sorted(strs, key=functools.cmp_to_key(my_compare)))
    print(strs)
    strs.sort(key=functools.cmp_to_key(my_compare))
    print(strs)


def sort(jsonlist):
    t = {}
    addrlist = list()
    for item in jsonlist:
        if item['MODBUS从站ID'] not in t.keys():
            t[item['MODBUS从站ID']] = list()
            t[item['MODBUS从站ID']].append(item)
        else:
            t[item['MODBUS从站ID']].append(item)
    for key in t.keys():
        t[key].sort(key=lambda k: (k.get('起始地址', 0)))
        addrlist += t[key]
    return addrlist

def sort2(jsonlist):#冒泡排序，按地址大小重新排序
    for i in range(len(jsonlist)-1):
        for j in range(len(jsonlist)-1-i):
            if jsonlist[j]['MODBUS从站ID'] == jsonlist[j+1]['MODBUS从站ID']:
                if jsonlist[j]['起始地址'] > jsonlist[j+1]['起始地址']:
                    jsonlist[j],jsonlist[j+1] = jsonlist[j+1],jsonlist[j]
    # print json.dumps(jsonlist,ensure_ascii=False,indent=4)
    return jsonlist

def list_sort2():
    pass
    addrlist = [{"起始地址": 400606, "MODBUS从站ID": 1}, {"起始地址": 400001, "MODBUS从站ID": 1}, {"起始地址": 400002, "MODBUS从站ID": 1},
                {"起始地址": 400003, "MODBUS从站ID": 1}, {"起始地址": 400601, "MODBUS从站ID": 2}, {"起始地址": 400602, "MODBUS从站ID": 2},
                {"起始地址": 400603, "MODBUS从站ID": 2},
                {"起始地址": 400604, "MODBUS从站ID": 2}]
    addrlist = [{"起始地址": 9, "MODBUS从站ID": 1}, {"起始地址": 5, "MODBUS从站ID": 1}, {"起始地址": 1, "MODBUS从站ID": 1},
                {"起始地址": 4, "MODBUS从站ID": 1}, {"起始地址": 3, "MODBUS从站ID": 2}, {"起始地址": 400602, "MODBUS从站ID": 2},
                {"起始地址": 400603, "MODBUS从站ID": 2},
                {"起始地址": 400604, "MODBUS从站ID": 2}]

    t = sort(addrlist)

    print(t)

def list_sort3():
    pass
    lst = [{'level': 19, 'star': 36, 'time': 1},
           {'level': 20, 'star': 40, 'time': 2},
           {'level': 20, 'star': 40, 'time': 3},
           {'level': 20, 'star': 40, 'time': 4},
           {'level': 20, 'star': 40, 'time': 5},
           {'level': 18, 'star': 40, 'time': 1}]

    # 需求:
    # level越大越靠前;
    # level相同, star越大越靠前;
    # level和star相同, time越小越靠前;

    # 先按time排序
    lst.sort(key=lambda k: (k.get('time', 0)))
    print(lst)
    # 再按照level和star顺序
    # reverse=True表示反序排列，默认正序排列
    lst.sort(key=lambda k: (k.get('level', 0), k.get('star', 0)), reverse=True)
    print(lst)


if __name__ == "__main__":
    pass
    # cc=list_sort_test()
    cc=list_sort3()