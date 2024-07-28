# -*- coding: utf-8 -*-

from acore_server_monitoring_core import api


def test():
    _ = api
    _ = api.make_dynamodb_table_name
    _ = api.UseCaseEnum
    _ = api.Measurement
    _ = api.WorldServerStatusMeasurement
    _ = api.Ec2RdsStatusMeasurement


if __name__ == "__main__":
    from acore_server_monitoring_core.tests import run_cov_test

    run_cov_test(__file__, "acore_server_monitoring_core.api", preview=False)
