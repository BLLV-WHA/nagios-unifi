#!/usr/bin/env python3
import argparse
import nagiosplugin

from enum import Enum
from pyunifi.controller import Controller


class Metrics(Enum):
    STATUS = 'status'
    CPU = 'cpu'
    MEMORY = 'memory'
    SPEED = 'speed'
    SATISFACTION = 'satisfaction'


class UnifiDevice(nagiosplugin.Resource):

    def __init__(self, hostname, ctrl_addr, ctrl_user, ctrl_passwd, metric):
        self._hostname = hostname
        self._ctrl_addr = ctrl_addr
        self._ctrl_user = ctrl_user
        self._ctrl_passwd = ctrl_passwd
        self._metric = metric

    def probe(self):
        c = Controller(self._ctrl_addr,
                       self._ctrl_user,
                       self._ctrl_passwd,
                       ssl_verify=False)
        for ap in c.get_aps():
            if ap.get('name') == self._hostname:
                if self._metric == Metrics.STATUS:
                    return [nagiosplugin.Metric('status', self._get_state(ap), context='null')]
                elif self._metric == Metrics.CPU:
                    return [nagiosplugin.Metric('cpu', self._get_cpu(ap), context='cpu')]
                elif self._metric == Metrics.MEMORY:
                    return [nagiosplugin.Metric('memory', self._get_mem(ap), context='memory')]
                elif self._metric == Metrics.SPEED:
                    return [nagiosplugin.Metric('speed', self._get_speed(ap), context='speed')]
                elif self._metric == Metrics.SATISFACTION:
                    return [nagiosplugin.Metric('satisfaction', self._get_satisfaction(ap), context='satisfaction')]

        raise nagiosplugin.CheckError('unable to find specified device: {}'.format(self._hostname))

    def _get_state(self, ap):
        state = False
        if ap['state'] == 1:
            state = True
        return state

    def _get_cpu(self, ap):
        return float(ap['system-stats']['cpu'])

    def _get_mem(self, ap):
        return float(ap['system-stats']['mem'])

    def _get_speed(self, ap):
        return ap['uplink']['speed']

    def _get_satisfaction(self, ap):
        print(ap['satisfaction'])
        return ap['satisfaction']


@nagiosplugin.guarded
def main():
    argp = argparse.ArgumentParser()
    argp.add_argument('--hostname', help='name of the unifi device', required=True)
    argp.add_argument('--metric',
                      choices=[Metrics.STATUS.value, Metrics.CPU.value, Metrics.MEMORY.value,
                               Metrics.SPEED.value, Metrics.SATISFACTION.value],
                      help='metric to be measured', required=True)
    argp.add_argument('--controller_host', help='address of unifi controller', required=True)
    argp.add_argument('--controller_user', help='login user for the controller', required=True)
    argp.add_argument('--controller_password', help='password for the controller', required=True)
    argp.add_argument('-w', '--warning')
    argp.add_argument('-c', '--critical')

    args = argp.parse_args()

    metric = Metrics[args.metric.upper()]
    unifi_device = UnifiDevice(args.hostname, args.controller_host, args.controller_user, args.controller_password,
                               metric)

    if metric == Metrics.STATUS:
        check = nagiosplugin.Check(unifi_device)
        check.main()

    elif metric == Metrics.CPU:
        check = nagiosplugin.Check(
            unifi_device,
            nagiosplugin.ScalarContext('cpu', args.warning, args.critical)
        )
        check.main()
    elif metric == Metrics.MEMORY:
        check = nagiosplugin.Check(
            unifi_device,
            nagiosplugin.ScalarContext('memory', args.warning, args.critical)
        )
        check.main()
    elif metric == Metrics.SPEED:
        check = nagiosplugin.Check(
            unifi_device,
            nagiosplugin.ScalarContext('speed', args.warning, args.critical)
        )
        check.main()
    elif metric == Metrics.SATISFACTION:
        check = nagiosplugin.Check(
            unifi_device,
            nagiosplugin.ScalarContext('satisfaction', args.warning, args.critical)
        )
        check.main()

if __name__ == '__main__':
    main()
