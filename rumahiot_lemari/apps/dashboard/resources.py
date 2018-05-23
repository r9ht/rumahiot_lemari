# Object for validating data structure

class UserAdddashBoardChartResource(object):
    def __init__(self, device_uuid, statistic_type, n_last_hour):
        self.device_uuid = device_uuid
        self.statistic_type = statistic_type
        self.n_last_hour = n_last_hour