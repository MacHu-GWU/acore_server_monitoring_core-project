How it Works
==============================================================================


Monitoring Data Store
------------------------------------------------------------------------------
我们使用 DynamoDB 作为监控数据的存储后端. 无论我们要采集什么监控数据, 它本质上都是一个时间序列. 它有以下三个属性:

- series_id: 时间序列的 ID, 一般是 server_id 和 use_case_id 的组合. 例如你想要监控 sbx-blue 这台服务器上的游戏的在线人数, 那么 series_id 就是 ``sbx-blue-online-players``. 这是 DynamoDB 的 hash key.
- create_at: 数据采集的时间. 数据一旦被写入就不会被修改了.
- expire_at: 数据的过期时间, 我们启用了 DynamoDB 的 TTL 功能, 一旦数据过期后, 过一段时间就会被自动删除. 关于 TTL 的详情可以参考我写的这篇博文 `DynamoDB Time to Live (TTL) <https://learn-aws.readthedocs.io/search.html?q=DynamoDB+Time+to+Live+%28TTL%29&check_keywords=yes&area=default#>`_.

对于不同的 use case, 我们会额外有不同的 attribute. 由于 DynamoDB 是 NoSQL 是 schemaless 的, 所以我们可以根据情况任意添加 attribute.

下面是 DynamoDB 的表结构源码:

.. dropdown:: dynamodb.py

    .. literalinclude:: ../../../acore_server_monitoring_core/dynamodb.py
       :language: python
       :linenos:


Capture Data
------------------------------------------------------------------------------
我们主要是要采集两类数据:

1. EC2 和 RDS 的状态信息, 比如是否在线, CPU 和 内存使用情况等. 这一功能主要由 `acore_server_metadata <https://github.com/MacHu-GWU/acore_server_metadata-project>`_ 来提供.
2. worldserver 的统计数据, 比如在线人数, 服务器在线时间等. 这一功能主要由 `acore_soap <https://github.com/MacHu-GWU/acore_soap-project>`_ 来提供.


Telemetry
------------------------------------------------------------------------------
对于 EC2 和 RDS 的状态, 我们使用遥测的方式. 一般是用一个 Lambda Function 来调 AWS API 来获取游戏服务器的状态. 这里我们显然不能用 EC2 本身来测量, 因为 EC2 本身可能会挂掉.


Localmetry
------------------------------------------------------------------------------
对于 worldserver 的统计数据, 由于我们必须要通过跟 SOAP API 通信来获取数据. 如果是在 worldserver 所在的 EC2 上跟 SOAP 通信, 一般几百毫秒就完成了. 而如果我们使用 SSM run remote command, 那么就需要花 3-5 秒甚至更长的时间. 如果我们使用的是 Lambda Function 来运行遥测代码, 那么等待的时间也是要花钱的. 而如果放在 EC2 上跑, 内存开销可以忽略不计, 而且速度会更快, 并且从逻辑上如果 EC2 挂掉了, 那么游戏服务器也挂掉了, 你自然也采集不到任何数据. 所以在 EC2 上跑一段程序来采集 worldserver 的统计数据是最佳选择.


Analyze Data
------------------------------------------------------------------------------
todo
