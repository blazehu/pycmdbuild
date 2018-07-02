# coding=utf-8
import logging
import requests
import json


class Logger(object):
    def __init__(self, name):
        """
        :param name:    日志记录的用例名
        """
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        # 日志格式
        formatter = logging.Formatter('%(asctime)s.%(msecs)03d %(process)d %(name)s - %(levelname)s - %(message)s',
                                      datefmt="%Y-%m-%d %H:%M:%S")
        # 输出到控制台
        cn = logging.StreamHandler()
        cn.setFormatter(formatter)
        # 添加handle
        self.logger.addHandler(cn)

    def get_logger(self):
        return self.logger


logger = Logger(__name__).get_logger()

METHOD_GET = "GET"
METHOD_PUT = "PUT"
METHOD_POST = "POST"
METHOD_DELETE = "DELETE"
INFO = 'CMDBuild python lib version: v0.1'
VERSION = 'v0.1'


class CMDBuild(object):
    """
    CMDBuild interface class. Please see _dir_ for methods
    """

    def __init__(self, host, username, password):
        self.host = host
        self.username = username
        self.password = password
        self.session_id = None
        self.version = VERSION
        self.info = INFO
        self._headers = {
            'Content-type': 'application/json',
            'Accept': '*/*'
        }

    def check_args(self):
        if not self.host:
            raise Exception('CMDBuild - ERROR: No host supplied')
        if not self.username:
            raise Exception('CMDBuild - ERROR: No username supplied')
        if not self.password:
            raise Exception('CMDBuild - ERROR: No password supplied')

    @property
    def headers(self):
        return {
            'Content-type': 'application/json',
            'Accept': '*/*',
            'CMDBuild-Authorization': self.session_id
        }

    @staticmethod
    def json_data(data):
        try:
            if data is None:
                return data
            elif isinstance(data, dict):
                return json.dumps(data)
            else:
                json.load(data)
                return data
        except ValueError:
            raise ValueError("CMDBuild - ERROR: Data is not a valid JSON object")

    @staticmethod
    def error_status_code(status_code):
        return status_code // 100 != 2

    @staticmethod
    def get_session_id(ret):
        data = ret.get('data')
        if isinstance(data, dict):
            session_id = data.get("_id")
            if len(str(session_id)) > 1:
                return session_id
        raise requests.RequestException("CMDBuild - ERROR: Don't Get Session ID")

    def api(self, path):
        return "{host}/services/rest/v2/{path}/".format(host=self.host.strip('/'), path=path.strip())

    def request(self, path, method="GET", data=None, params=None):
        api = self.api(path)
        func = getattr(requests, method.lower())
        data = self.json_data(data)
        resp = func(api, data=data, params=params, headers=self.headers)
        try:
            ret = resp.json()
        except:
            ret = dict(errors=[dict(message=resp.text)])
        if self.error_status_code(resp.status_code):
            logger.error("CMDBuild - INFO: {0} - {1} - Data: {2}".format(method, resp.status_code, data))
            resp.raise_for_status()
        return resp.status_code, ret

    def connect(self):
        data = dict(username=self.username, password=self.password)
        path = "sessions"
        resp_status, ret = self.request(path=path, method=METHOD_POST, data=data)
        self.session_id = self.get_session_id(ret)
        return self.session_id

    def close(self):
        path = "sessions/{0}".format(self.session_id)
        self.session_id = None
        return self.request(path, method='DELETE')

    def session_info(self):
        """
        Return session info
        """
        path = "sessions/{0}".format(self.session_id)
        return self.request(path)

    def lookup_types_info(self):
        """
        Return list of defined lookup types
        """
        path = "lookup_types"
        return self.request(path)

    def lookup_type_values(self, pk):
        """
        Return values for given lookup type
        """
        path = "lookup_types/{0}/values".format(pk)
        return self.request(path)

    def lookup_type_details(self, name, pk):
        """
        Return value for given lookup type id
        """
        path = "lookup_types/{0}/values/{1}".format(name, pk)
        return self.request(path)

    def domain_list(self):
        """
        Return list of domains defined
        """
        path = "domains"
        return self.request(path)

    def domain_relations(self, pk):
        """
        Return relations of specified domain as json object
        """
        path = "domains/{}/relations".format(pk)
        return self.request(path)

    def domain_relation_creation(self, name, data):
        """
        Return relation id of specified domain.
        """
        path = "domains/{}/relations/".format(name)
        return self.request(path=path, method=METHOD_POST, data=data)

    def class_list(self):
        """
        Return json object with list of available classes
        """
        path = "classes"
        return self.request(path)

    def class_details(self, typ):
        """
        Return details of specified class as json object
        """
        path = "classes/{}".format(typ)
        return self.request(path)

    def class_get_attributes_by_type(self, typ):
        path = "classes/{}/attributes".format(typ)
        return self.request(path)

    def class_get_cards_by_type_custom_filter(self, typ, filter_dict=None):
        filter_dict = {} if filter_dict is None else filter_dict
        path = "classes/{0}/cards?filter={1}".format(typ, filter_dict)
        return self.request(path)

    def class_get_cards_by_type(self, typ, filter_list=None):
        """
        filter_list : [{"attribute": "A", "value": "a", "fuzz": True},]
        """
        filter_list = [] if filter_list is None else filter_list
        f_list, attribute_value = [], {}
        for filter_item in filter_list:
            attribute = filter_item.get('attribute')
            value = filter_item.get('value')
            fuzz = filter_item.get('fuzz', False)
            operator = "like" if fuzz else "equal"
            f_list.append({
                "simple": {
                    "attribute": attribute,
                    "operator": operator,
                    "value": [value]
                }})
        if len(filter_list) > 1:
            attribute_value["and"] = f_list
        if len(filter_list) == 1:
            attribute_value = f_list[0]
        filter_data = {
            "attribute": attribute_value
        } if filter_list else {}
        path = "classes/{0}/cards?filter={1}".format(typ, filter_data)
        return self.request(path)

    def class_get_card_details(self, typ, pk):
        path = "classes/{0}/cards/{1}".format(typ, pk)
        return self.request(path)

    def class_insert_card(self, typ, card_object):
        """
        Insert card with name into cmdb
        """
        path = "classes/{0}/cards".format(typ)
        return self.request(path=path, method=METHOD_POST, data=card_object)

    def class_update_card(self, typ, pk, card_object):
        """
        Update card with name into cmdbuild
        """
        path = "classes/{0}/cards/{1}".format(typ, pk)
        return self.request(path=path, method=METHOD_PUT, data=card_object)

    def class_delete_card(self, typ, pk):
        """
        Delete cards of specified class as json object
        """
        path = "classes/{0}/cards/{1}".format(typ, pk)
        return self.request(path=path, method=METHOD_DELETE)

    def create_relation(self, typ, card_object):
        """
        Insert card with name into cmdbuild
        """
        path = "domains/{0}/relations".format(typ)
        return self.request(path, "POST", data=card_object)

    def update_relation(self, typ, card_object, pk):
        """
        Insert card with name into cmdbuild
        """
        path = "domains/{0}/relations/{1}".format(typ, pk)
        return self.request(path, "PUT", data=card_object)

    def delete_relation(self, typ, pk):
        """
        Delete Relation of specified class as json object
        """
        path = "domains/{0}/relations/{1}".format(typ, pk)
        return self.request(path, "DELETE")

    def list_relation(self, typ):
        """
        Delete Relation of specified class as json object
        """
        path = "domains/{0}/relations".format(typ)
        return self.request(path)

    def get_relation_details(self, typ, pk):
        """
        Delete Relation of specified class as json object
        """
        path = "domains/{0}/relations/{1}".format(typ, pk)
        return self.request(path)
