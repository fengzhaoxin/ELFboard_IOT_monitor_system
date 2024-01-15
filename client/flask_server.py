import json

from flask import Flask, jsonify, request
from flask import render_template

from alibabacloud_tea_openapi.client import Client as OpenApiClient
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_tea_util import models as util_models
from alibabacloud_openapi_util.client import Client as OpenApiUtilClient

web = Flask(__name__)

access_key_id = "xxxxxxxxxxxxxx"
access_key_secret = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"


class Sample:
    def __init__(self):
        pass

    @staticmethod
    def create_client(
            access_key_id: str,
            access_key_secret: str,
    ) -> OpenApiClient:
        """
        使用AK&SK初始化账号Client
        @param access_key_id:
        @param access_key_secret:
        @return: Client
        @throws Exception
        """
        config = open_api_models.Config(
            # 必填，您的 AccessKey ID,
            access_key_id=access_key_id,
            # 必填，您的 AccessKey Secret,
            access_key_secret=access_key_secret
        )
        # Endpoint 请参考 https://api.aliyun.com/product/Iot
        config.endpoint = f'iot.cn-shanghai.aliyuncs.com'
        return OpenApiClient(config)

    @staticmethod
    def create_set_info() -> open_api_models.Params:
        """
        API 相关
        @param path: params
        @return: OpenApi.Params
        """
        params = open_api_models.Params(
            # 接口名称,
            action='SetDeviceProperty',
            # 接口版本,
            version='2018-01-20',
            # 接口协议,
            protocol='HTTPS',
            # 接口 HTTP 方法,
            method='POST',
            auth_type='AK',
            style='RPC',
            # 接口 PATH,
            pathname=f'/',
            # 接口请求体内容格式,
            req_body_type='formData',
            # 接口响应体内容格式,
            body_type='json'
        )
        return params

    @staticmethod
    def create_get_info() -> open_api_models.Params:
        """
        API 相关
        @param path: params
        @return: OpenApi.Params
        """
        params = open_api_models.Params(
            # 接口名称,
            action='QueryDeviceOriginalPropertyStatus',
            # 接口版本,
            version='2018-01-20',
            # 接口协议,
            protocol='HTTPS',
            # 接口 HTTP 方法,
            method='POST',
            auth_type='AK',
            style='RPC',
            # 接口 PATH,
            pathname=f'/',
            # 接口请求体内容格式,
            req_body_type='formData',
            # 接口响应体内容格式,
            body_type='json'
        )
        return params

    @staticmethod
    def main():
        client = Sample.create_client(access_key_id, access_key_secret)
        params = Sample.create_get_info()
        # query params
        queries = {}
        queries['PageSize'] = 10
        queries['ProductKey'] = 'xxxxxxxxxxxxxx'
        queries['DeviceName'] = 'xxxxxx'
        queries['Asc'] = 0
        # body params
        body = {}
        body['ApiProduct'] = None
        body['ApiRevision'] = None
        # runtime options
        runtime = util_models.RuntimeOptions()
        request = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(queries),
            body=body
        )
        # 复制代码运行请自行打印 API 的返回值
        # 返回值为 Map 类型，可从 Map 中获得三类数据：响应体 body、响应头 headers、HTTP 返回的状态码 statusCode。
        response = client.call_api(params, request, runtime)
        body = response['body']
        Data = body['Data']
        List = Data['List']
        Proper = List['PropertyStatusDataInfo']
        Temp = json.loads(Proper[0]['Value'])
        Volt = json.loads(Proper[1]['Value'])
        Led2 = json.loads(Proper[2]['Value'])
        Led1 = json.loads(Proper[3]['Value'])
        Humi = json.loads(Proper[4]['Value'])
        message = {
            'humi': Humi['data'],
            'temp': Temp['data'],
            'volt': Volt['data'],
            'led1': Led1['data'],
            'led2': Led2['data'],
        }
        return jsonify(message)

    @staticmethod
    def main_set(item: str):
        client = Sample.create_client(access_key_id, access_key_secret)
        params = Sample.create_set_info()
        # query params
        queries = {}
        queries['ProductKey'] = 'xxxxxxxx'
        queries['DeviceName'] = 'xxxxx'
        queries['Items'] = item  # '{"LEDSwitch":0}'
        # body params
        body = {}
        body['ApiProduct'] = None
        body['ApiRevision'] = None
        # runtime options
        runtime = util_models.RuntimeOptions()
        request = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(queries),
            body=body
        )
        # 复制代码运行请自行打印 API 的返回值
        # 返回值为 Map 类型，可从 Map 中获得三类数据：响应体 body、响应头 headers、HTTP 返回的状态码 statusCode。
        resp = client.call_api(params, request, runtime)
        body = resp['body']
        data = body['Success']
        return str(data)


@web.route('/')
def movie_list():
    return render_template('index.html')


@web.route('/get_data', methods=['GET', 'POST'])
def mqtt_data():
    message = Sample.main()
    return message


@web.route('/set_data', methods=['GET', 'POST'])
def mqtt_set():
    name = request.form.get('name')
    state = request.form.get('state')

    request_info = {}
    data = json.loads(json.dumps(request_info))
    data[name] = int(state)
    request_data = json.dumps(data, ensure_ascii=False)
    print(request_data)

    message = Sample.main_set(request_data)
    return message


web.run(debug=True)
