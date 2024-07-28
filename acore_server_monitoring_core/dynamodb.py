# -*- coding: utf-8 -*-

import enum
import pynamodb_mate.api as pm


def make_dynamodb_table_name(env_name: str) -> str:  # pragma: no cover
    return f"wserver-{env_name}-server-monitoring"


class UseCaseEnum(str, enum.Enum):
    worldserver_status = "worldserver_status"
    ec2_rds_status = "ec2_rds_status"


class Measurement(pm.Model):
    """
    Acore server monitoring time series measurement data store.

    :param series_id: the time series id, usually it is in format of
        ``{server_id}-{use_case_id}``, for example ``sbx-blue-worldserver_status``,
        ``sbx-blue-ec2_rds_status``.
    :param create_at: the time when the measurement data is created.
    :param expire_at: the time when the measurement data is expired. DynamoDB
        will automatically delete the expired data in a few days.
    """

    series_id: pm.REQUIRED_STR = pm.NumberAttribute(hash_key=True)
    create_at: pm.REQUIRED_DATETIME = pm.NumberAttribute(range_key=True)
    expire_at: pm.REQUIRED_DATETIME = pm.TTLAttribute()
    is_ec2_exists: pm.OPTIONAL_BINARY = pm.BooleanAttribute(default=None)
    is_rds_exists: pm.OPTIONAL_BINARY = pm.BooleanAttribute(default=None)
    is_ec2_running: pm.OPTIONAL_BINARY = pm.BooleanAttribute(default=None)
    is_rds_running: pm.OPTIONAL_BINARY = pm.BooleanAttribute(default=None)
    ec2_status: pm.OPTIONAL_STR = pm.UnicodeAttribute(default=None)
    rds_status: pm.OPTIONAL_STR = pm.UnicodeAttribute(default=None)
    connected_players: pm.OPTIONAL_INT = pm.NumberAttribute(default=None)
    characters_in_world: pm.OPTIONAL_INT = pm.NumberAttribute(default=None)
    server_uptime: pm.OPTIONAL_INT = pm.NumberAttribute(default=None)
    cpu_usage: pm.OPTIONAL_FLOAT = pm.NumberAttribute(default=None)
    memory_usage: pm.OPTIONAL_FLOAT = pm.NumberAttribute(default=None)
    total_memory: pm.OPTIONAL_INT = pm.NumberAttribute(default=None)
    available_memory: pm.OPTIONAL_INT = pm.NumberAttribute(default=None)


class WorldServerStatusMeasurement(Measurement):
    """
    World server status measurement data.

    :param connected_players: connected players.
    :param characters_in_world: characters in world.
    :param server_uptime: server uptime in seconds.
    :param cpu_usage: 0 ~ 100, float. 50.0 means 50%.
    :param memory_usage: 0 ~ 100, float. 50.0 means 50%.
    :param total_memory: total memory in MB.
    :param available_memory: available memory in MB.
    """

    connected_players: pm.OPTIONAL_INT = pm.NumberAttribute(default=None)
    characters_in_world: pm.OPTIONAL_INT = pm.NumberAttribute(default=None)
    server_uptime: pm.OPTIONAL_INT = pm.NumberAttribute(default=None)
    cpu_usage: pm.OPTIONAL_FLOAT = pm.NumberAttribute(default=None)
    memory_usage: pm.OPTIONAL_FLOAT = pm.NumberAttribute(default=None)
    total_memory: pm.OPTIONAL_INT = pm.NumberAttribute(default=None)
    available_memory: pm.OPTIONAL_INT = pm.NumberAttribute(default=None)


class Ec2RdsStatusMeasurement(Measurement):
    """
    EC2 and RDS status measurement data.

    :param is_ec2_exists:
    :param is_rds_exists:
    :param is_ec2_running:
    :param is_rds_running:
    :param ec2_status:
    :param rds_status:
    """

    is_ec2_exists: pm.OPTIONAL_BINARY = pm.BooleanAttribute(default=None)
    is_rds_exists: pm.OPTIONAL_BINARY = pm.BooleanAttribute(default=None)
    is_ec2_running: pm.OPTIONAL_BINARY = pm.BooleanAttribute(default=None)
    is_rds_running: pm.OPTIONAL_BINARY = pm.BooleanAttribute(default=None)
    ec2_status: pm.OPTIONAL_STR = pm.UnicodeAttribute(default=None)
    rds_status: pm.OPTIONAL_STR = pm.UnicodeAttribute(default=None)
