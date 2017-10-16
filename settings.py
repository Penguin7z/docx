# -*- coding: utf-8 -*-

"""
    eve-demo settings
    ~~~~~~~~~~~~~~~~~
    Settings file for our little demo.
    PLEASE NOTE: We don't need to create the two collections in MongoDB.
    Actually, we don't even need to create the database: GET requests on an
    empty/non-existant DB will be served correctly ('200' OK with an empty
    collection); DELETE/PATCH will receive appropriate responses ('404' Not
    Found), and POST requests will create database and collections when needed.
    Keep in mind however that such an auto-managed database will most likely
    perform poorly since it lacks any sort of optimized index.
    :copyright: (c) 2016 by Nicola Iarocci.
    :license: BSD, see LICENSE for more details.
"""

# We want to seamlessy run our API both locally and on Heroku. If running on
# Heroku, sensible DB connection settings are stored in environment variables.
MONGO_HOST = "localhost"
MONGO_PORT = 27017
MONGO_USERNAME = ''
MONGO_PASSWORD = ''
MONGO_DBNAME = 'docx'

URL_PREFIX = 'api'
API_VERSION = 'v1'

# X_DOMAINS = ['http://localhost:8000',  # The domain where Swagger UI is running
#              'http://editor.swagger.io',
#              'http://petstore.swagger.io']
X_HEADERS = ['Content-Type', 'If-Match']  # Needed for the "Try it out" buttons


# Enable reads (GET), inserts (POST) and DELETE for resources/collections
# (if you omit this line, the API will default to ['GET'] and provide
# read-only access to the endpoint).
RESOURCE_METHODS = ['GET', 'POST']

# Enable reads (GET), edits (PATCH) and deletes of individual items
# (defaults to read-only item access).
ITEM_METHODS = ['GET', 'PATCH', 'DELETE']

# We enable standard client cache directives for all resources exposed by the
# API. We can always override these global settings later.
CACHE_CONTROL = 'max-age=20'
CACHE_EXPIRES = 20

# Our API will expose two resources (MongoDB collections): 'people' and
# 'works'. In order to allow for proper data validation, we define beaviour
# and structure.
people = {
    # 'title' tag used in item links.
    'item_title': 'person',

    # by default the standard item entry point is defined as
    # '/people/<ObjectId>/'. We leave it untouched, and we also enable an
    # additional read-only entry point. This way consumers can also perform GET
    # requests at '/people/<lastname>/'.
    'additional_lookup': {
        'url': 'regex("[\w]+")',
        'field': 'lastname'
    },

    # Schema definition, based on Cerberus grammar. Check the Cerberus project
    # (https://github.com/pyeve/cerberus) for details.
    'schema': {
        'firstname': {
            'type': 'string',
            'minlength': 1,
            'maxlength': 10,
        },
        'lastname': {
            'type': 'string',
            'minlength': 1,
            'maxlength': 15,
            'required': True,
            # talk about hard constraints! For the purpose of the demo
            # 'lastname' is an API entry-point, so we need it to be unique.
            'unique': True,
        },
        # 'role' is a list, and can only contain values from 'allowed'.
        'role': {
            'type': 'list',
            'allowed': ["author", "contributor", "copy"],
        },
        # An embedded 'strongly-typed' dictionary.
        'location': {
            'type': 'dict',
            'schema': {
                'address': {'type': 'string'},
                'city': {'type': 'string'}
            },
        },
        'born': {
            'type': 'datetime',
        },
    }
}

works = {
    # if 'item_title' is not provided Eve will just strip the final
    # 's' from resource name, and use it as the item_title.
    #'item_title': 'work',

    # We choose to override global cache-control directives for this resource.
    'cache_control': 'max-age=10,must-revalidate',
    'cache_expires': 10,

    'schema': {
        'title': {
            'type': 'string',
            'required': True,
        },
        'description': {
            'type': 'string',
        },
        'owner': {
            'type': 'objectid',
            'required': True,
            # referential integrity constraint: value must exist in the
            # 'people' collection. Since we aren't declaring a 'field' key,
            # will default to `people._id` (or, more precisely, to whatever
            # ID_FIELD value is).
            'data_relation': {
                'resource': 'people',
                # make the owner embeddable with ?embedded={"owner":1}
                'embeddable': True
            },
        },
    }
}

# 模块表
module_x = {
    'cache_control': 'max-age=10,must-revalidate',
    'cache_expires': 10,

    'schema': {
        # 模块名
        'name': {
            'type': 'string',
            'required': True,
        },
    }
}


# 字段表
field_type = {
    'cache_control': 'max-age=10,must-revalidate',
    'cache_expires': 10,

    'schema': {
        # 字段名
        'name': {
            'type': 'string',
            'required': True,
        },
        # 字段别名
        'alias': {
            'type': 'string',
            'required': True,
        },
    }
}


# 接口表
api_x = {
    'cache_control': 'max-age=10,must-revalidate',
    'cache_expires': 10,

    'schema': {
        'name': {
            'type': 'string',
            'required': True,
        },
        'alias': {
            'type': 'string',
            'required': True,
        },
    }
}


# 入参表
api_in_x = {
    'cache_control': 'max-age=10,must-revalidate',
    'cache_expires': 10,

    'schema': {
        # 接口id
        'api_id': {
            'type': 'objectid',
            'required': True,
            'data_relation': {
                'resource': 'api_x',
                'embeddable': True
            },
        },
        # 字段类型id
        'filed_type_id': {
            'type': 'objectid',
            'required': True,
            'data_relation': {
                'resource': 'field_type',
                'embeddable': True
            },
        },
        # 字段名
        'name': {
            'type': 'string',
            'required': True,
        },
        # 字段描述
        'desc': {
            'type': 'string',
            'required': True,
        },
        # 补充信息
        'memo': {
            'type': 'string',
        },
        # 最小值
        'min_v': {
            'type': 'number',
        },
        # 最大值
        'max_v': {
            'type': 'number',
        },
        # 最小长度
        'min_len': {
            'type': 'number',
        },
        # 最大长度
        'max_len': {
            'type': 'number',
        },
        # 是否必填
        'is_required': {
            'type': 'string',
        },
        # 是否唯一
        'is_unique': {
            'type': 'string',
        },
        # 允许取值范围
        'allow_list': {
            'type': 'list',
        },
        # 正则表达式
        'regex_str': {
            'type': 'string',
        },
        # 作者
        'author': {
            'type': 'string',
        },
        # 版本
        'version': {
            'type': 'string',
        },
    }
}


# 出参表
api_out_x = {
    'cache_control': 'max-age=10,must-revalidate',
    'cache_expires': 10,

    'schema': {
        # 接口id
        'api_id': {
            'type': 'objectid',
            'required': True,
            'data_relation': {
                'resource': 'api_x',
                'embeddable': True
            },
        },
        # 字段类型id
        'filed_type_id': {
            'type': 'objectid',
            'required': True,
            'data_relation': {
                'resource': 'field_type',
                'embeddable': True
            },
        },
        # 字段名
        'name': {
            'type': 'string',
            'required': True,
        },
        # 字段描述
        'desc': {
            'type': 'string',
            'required': True,
        },
        # 补充信息
        'memo': {
            'type': 'string',
        },
        # 最小值
        'min_v': {
            'type': 'number',
        },
        # 最大值
        'max_v': {
            'type': 'number',
        },
        # 最小长度
        'min_len': {
            'type': 'number',
        },
        # 最大长度
        'max_len': {
            'type': 'number',
        },
        # 是否必填
        'is_required': {
            'type': 'string',
        },
        # 是否唯一
        'is_unique': {
            'type': 'string',
        },
        # 允许取值范围
        'allow_list': {
            'type': 'list',
        },
        # 正则表达式
        'regex_str': {
            'type': 'string',
        },
        # 作者
        'author': {
            'type': 'string',
        },
        # 版本
        'version': {
            'type': 'string',
        },
    }
}


# The DOMAIN dict explains which resources will be available and how they will
# be accessible to the API consumer.
DOMAIN = {
    'people': people,
    'works': works,
    'module_x': module_x,
    'field_type': field_type,
    'api_x': api_x,
    'api_in_x': api_in_x,
    'api_out_x': api_out_x,
}