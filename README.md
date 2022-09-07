#### Python library to access the REST interface of a CMDBuild server
![Alt text](http://www.cmdbuild.org/logo.png)![Alt text](https://www.python.org/static/opengraph-icon-200x200.png)

---

### Installation & Usage

pip install	

```
pip install pycmdbuild
```

import the package:

```
from cmdbuild.client import CMDBuild
```

### Getting Started

```
from cmdbuild.client import CMDBuild

client = CMDBuild(CMDB_HOST, CMDB_USERNAME, CMDB_PASSWORD)
client.connect()

client.session_info()
client.lookup_types_info()
client.domain_list()
```

### Documentation for API Endpoints

All URIs are relative to https://cmdb_host/services/rest/v3

filter_data: {"simple": {"attribute": attribute,"operator": operator,"value": [value] }

filter_dict: {"attribute": filter_data}}, 多个过滤条件 {"attribute": {"and": [filter1, filter2]}}

filter_list: [{"attribute": "A", "value": "a", "fuzz": True},]

Method | HTTP request | Description
---|---|---
connect| POST   /sessions/ | 
close | DELETE   /sessions/ |
session_info | GET   /sessions/ |
lookup_types_info | GET   /lookup_types/ |
lookup_type_values | GET   /lookup_types/{id}/values/ |
lookup_type_details | GET   /lookup_types/{name}/values/{id}/ |
domain_list | GET   /domains/ |  
domain_relations | GET   /domains/{name}/relations/ |
domain_relation_creation | POST   /domains/{name}/relations/ |
class_list | GET   /classes/ | 
class_details | GET   /classes/{type}/ |
class_get_attributes_by_type | GET   /classes/{type}/attributes/ |
class_get_cards_by_type_custom_filter | GET   /classes/{type}/cards?filter={filter_dict}/ |
class_get_cards_by_type | GET   /classes/{type}/cards?filter={filter_list}/ | 
class_get_card_details | GET   /classes/{type}/cards/{id}/ |
class_insert_card | POST   /classes/{type}/cards/ |
class_update_card | PUT   /classes/{type}/cards/{id}/ |
class_delete_card | DELETE   /classes/{type}/cards/{id}/ |
create_relation | POST   /domains/{typ}/relations/ |
update_relation | PUT   /domains/{type}/relations/{id}/ |
delete_relation | DELETE   /domains/{type}/relations/{id}/ |
list_relation | GET   /domains/{type}/relations/ |
get_relation_details | GET   /domains/{type}/relations/{id}/ | 


### Documentation For Authorization


If you want update or delete your card  you should get pk first. Cmdbuild's api is not restful, we can’t use patch, only update all (put).
So you can do that:
```
def update_card(self, classe, card, description):
    instance = client.class_get_cards_by_type()
    id = instance["_id"]
    client.class_update_card()
```
The same goes for deletion, you can add compare and retry function to guarantee reliability. 


