import json
from urllib.parse import urljoin, urlencode
from hashlib import md5
import requests
from collections import defaultdict
from treelib import Tree
from collections import Counter



def get_addres_info_gaodei():
    key = '33b90739da0440c6ba77debb0db31879'

    url='https://restapi.amap.com/v3/config/district?'
    params = dict(key=key)
    params = {k: v for k, v in sorted(params.items())}  # 升序排序

    print((params))
    response = requests.get(url=url, params=params,verify=False)
    data = response.json()
    print(data)

def get_addres_info_qq():
    key = 'VTQBZ-KLBY5-UJDID-QDB25-XMWLO-RJBFC'
    secret_key = 'gqMp9tSXyCf3zMIFAhCPmmGtgHIbzfh'
    path = '/ws/district/v1/list'
    base = 'https://apis.map.qq.com/'
    url = urljoin(base, path)
    params = dict(key=key)
    params = {k: v for k, v in sorted(params.items())}  # 升序排序
    sig = md5('{}?{}{}'.format(path, urlencode(params), secret_key).encode()).hexdigest()  # 签名计算
    params['sig'] = sig  # 放回请求
    response = requests.get(url=url, params=params)
    data = response.json()
    print(data)
    open('data.json', mode='w', encoding='utf-8').write(json.dumps(data))

def info_show():
    data = json.load(open('data.json'))
    data_version = data['data_version']
    print(data_version)
    provinces = data['result'][0]
    citys = data['result'][1]
    districts = data['result'][2]
    for province in provinces:
        cidx = province['cidx']
        province_citys = citys[cidx[0]:cidx[1]]
        print(province['fullname'])
        for city in province_citys:
            print('\t', city['fullname'])
            cidx = city.get('cidx')
            if cidx:
                city_districts = districts[cidx[0]:cidx[1]]
                for district in city_districts:
                    print('\t\t', district['fullname'])


def info_to_dict():
    data = json.load(open('data.json'))
    provinces = data['result'][0]
    citys = data['result'][1]
    districts = data['result'][2]
    province_city_district_map = defaultdict(lambda: defaultdict(list))
    for province in provinces:
        cidx = province['cidx']
        province_citys = citys[cidx[0]:cidx[1]]
        for city in province_citys:
            if city['fullname'] not in province_city_district_map[province['fullname']]:
                province_city_district_map[province['fullname']][city['fullname']] = list()
            cidx = city.get('cidx')
            if cidx:
                city_districts = districts[cidx[0]:cidx[1]]
                for district in city_districts:
                    province_city_district_map[province['fullname']][city['fullname']].append(district['fullname'])
    print(province_city_district_map)

#树结构展示
def info_show_tree():
    data = json.load(open('data.json'))
    data_version = data['data_version']
    provinces = data['result'][0]
    citys = data['result'][1]
    districts = data['result'][2]
    tree = Tree()
    tree.create_node('中国省市区列表', data_version)  # 根节点
    for province in provinces:
        cidx = province['cidx']
        province_citys = citys[cidx[0]:cidx[1]]
        tree.create_node(province['fullname'], province['id'], parent=data_version)
        for city in province_citys:
            tree.create_node(city['fullname'], city['id'], parent=province['id'])
            cidx = city.get('cidx')
            if cidx:
                city_districts = districts[cidx[0]:cidx[1]]
                for district in city_districts:
                    tree.create_node(district['fullname'], district['id'], parent=city['id'])
    tree.show()

    # 统计，有某些区名是重复的
    counter = Counter([tree[node].tag for node in tree.expand_tree(mode=Tree.DEPTH, sorting=False)])
    print("统计，有某些区名是重复的:",counter)


def cc():
    pass
    data = json.load(open('data.json'))
    data_version = data['data_version']
    provinces = data['result'][0]
    provinces_tuple=()
    for province in provinces:
        pass
        print(province)
        print(province["fullname"])
        provinces_tuple = provinces_tuple + ((province["id"],province["fullname"]),)
    print(provinces_tuple)
    print(type(provinces_tuple))

    citys = data['result'][1]
    # print(provinces[9])
    cidx = provinces[9]['cidx']
    province_citys_js = citys[cidx[0]:cidx[1]]
    # print(province_citys_js)
    for city in province_citys_js:
        pass
        # print(city["fullname"])


def cc2():
    pass
    region_dict={}
    data = json.load(open('data.json'))
    data_version = data['data_version']
    provinces = data['result'][0]
    citys = data['result'][1]
    for province in provinces:
        pass
        # print(province["fullname"])


        cidx=province['cidx']
        province_citys_js = citys[cidx[0]:cidx[1]]
        one_province_city_list = []
        for city in province_citys_js:
            pass
            # print(city["fullname"])
            one_province_city_list.append(city["fullname"])
        region_dict[province["fullname"]] = one_province_city_list

    print(region_dict)





if __name__ == "__main__":
    pass
    # get_addres_info_gaodei()
    # get_addres_info_qq()
    # info_show()
    # info_to_dict()
    # info_show_tree()

    cc2()


