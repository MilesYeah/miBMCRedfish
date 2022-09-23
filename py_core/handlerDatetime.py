#!/usr/bin/python3

import datetime

"""
        python中时间日期格式化符号：
        ------------------------------------
        %y 两位数的年份表示（00-99）
        %Y 四位数的年份表示（000-9999）
        %m 月份（01-12）
        %d 月内中的一天（0-31）
        %H 24小时制小时数（0-23）
        %I 12小时制小时数（01-12）
        %M 分钟数（00=59）
        %S 秒（00-59）
        %a 本地简化星期名称
        %A 本地完整星期名称
        %b 本地简化的月份名称
        %B 本地完整的月份名称
        %c 本地相应的日期表示和时间表示
        %j 年内的一天（001-366）
        %p 本地A.M.或P.M.的等价符
        %U 一年中的星期数（00-53）星期天为星期的开始
        %w 星期（0-6），星期天为星期的开始
        %W 一年中的星期数（00-53）星期一为星期的开始
        %x 本地相应的日期表示
        %X 本地相应的时间表示
        %Z 当前时区的名称  # 乱码
        %% %号本身
"""


def timestamp2datetime(ts):
    """
    将一个timestamp转换成为一个datetime对象
    :param ts: a float number which is a time stamp
    :return:
    """
    return datetime.datetime.fromtimestamp(ts)


def str2datetime(s, fmt="%Y-%m-%d %H_%M_%S"):
    """
    将一个日期时间字符串转换成一个datetime对象
    :param s: a datetime str
    :param fmt: formatter
    :return:
    """
    return datetime.datetime.strptime(s, fmt)


def datetime2str(s, fmt="%Y-%m-%d %H_%M_%S"):
    """
    将一个日期时间字符串转换成一个datetime对象
    :param s: a datetime str
    :param fmt: formatter
    :return:
    """
    return s.strftime(fmt)


class HandlerDatetime(object):

    """

    """
    def __init__(self, dt=None):
        """

        :param dt: 接收一个datetime对象，不然就赋值为当前时间日期
        """
        if dt is None:
            self._dt = datetime.datetime.now()
        elif isinstance(dt, float):
            self._dt = timestamp2datetime(dt)
        elif isinstance(dt, datetime.datetime):
            self._dt = dt
        elif isinstance(dt, str):
            self._dt = str2datetime(dt)
        else:
            self._dt = None

        self.fmt = "%Y-%m-%d %H_%M_%S"

    @property
    def dt(self):
        return self._dt

    @property
    def dt_str(self):
        if self.dt:
            return self.dt.strftime(self.fmt)

    @property
    def dt_timestamp(self):
        if self.dt:
            return datetime.datetime.timestamp(self.dt)

    @property
    def dt_year(self):
        if self.dt:
            return self.dt.year

    @property
    def dt_month(self):
        if self.dt:
            return self.dt.month

    @property
    def dt_day(self):
        if self.dt:
            return self.dt.day

    @property
    def dt_hour(self):
        if self.dt:
            return self.dt.hour

    @property
    def dt_minute(self):
        if self.dt:
            return self.dt.minute

    @property
    def dt_second(self):
        if self.dt:
            return self.dt.second

    def future(self, s=0, m=0, h=0, d=0, w=0):
        """

        :param s:相加减的秒
        :param m:相加减的分
        :param h:相加减的时
        :param d:相加减的日
        :param w:相加减的周
        :return: 计算之后的 datetime 对象
        """
        try:
            return self.dt + datetime.timedelta(seconds=int(s),
                                                minutes=int(m),
                                                hours=int(h),
                                                days=int(d),
                                                weeks=int(w)
                                                )
        except ValueError:
            raise Exception(f"获取时间错误，时间单位w{w}d{d}h{h}m{m}s{s}")


if __name__ == "__main__":
    a = HandlerDatetime("2020-3-2 9:18:00")
    b = HandlerDatetime(datetime.datetime.now())
    c = HandlerDatetime(datetime.datetime.timestamp(datetime.datetime.now()))

    pass
