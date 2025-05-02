# encoding:utf-8
# 根据您选择的AK已为您生成调用代码
# 检测到您当前的AK设置了IP白名单校验
# 您的IP白名单中的IP非公网IP，请设置为公网IP，否则将请求失败
# 请在IP地址为0.0.0.0/0 外网IP的计算发起请求，否则将请求失败
import requests
import json
from weather.district_search import get_district_id


# 服务地址
host = "https://api.map.baidu.com"

# 接口地址
uri = "/weather/v1/"

# 此处填写你在控制台-应用管理-创建应用后获取的AK
ak = "ICbCuMnbV9i8A3AoH0r0HiB7zw9YiIOp"


def get_weather(district_id):
    """
    district_id: 行政区划代码
    """
    params = {
        "district_id": district_id,
        "data_type": "all",
        "ak": ak,
    }
    response = requests.get(url=host + uri, params=params)
    if response:
        return json.dumps(response.json(), ensure_ascii=False, indent=4)
    else:
        return "Error: Unable to fetch data from API"


def get_weather_by_location(location):
    district_id = get_district_id(location)
    if district_id:
        return get_weather(district_id)
    else:
        return "Error: Unable to find district ID for the given location"


print(get_weather_by_location("上海浦东新区"))
