#!/usr/bin/env python3
import argparse
import pprint

import nagiosplugin

from pyunifi.controller import Controller

import config


class UnifiDevice(nagiosplugin.Resource):

    def __init__(self, hostname):
        self._hostname = hostname

    def probe(self):
        c = Controller(config.unifi_controller_addr,
                       config.unifi_controller_user,
                       config.unifi_controller_pass,
                       ssl_verify=False)
        for ap in c.get_aps():
            if ap.get('name') == self._hostname:
                #pp = pprint.PrettyPrinter(indent=4)
                #pp.pprint(ap)
                state = False
                if ap['state'] == 1:
                    state = True
                return [nagiosplugin.Metric('status', state, context='null')]

        raise nagiosplugin.CheckError('unable to find specified device: {}'.format(self._hostname))


@nagiosplugin.guarded
def main():
    argp = argparse.ArgumentParser()
    argp.add_argument('--hostname', help='name of the unifi device', required=True)
    argp.add_argument('--metric', choices=['status', 'cpu', 'memory', 'speed', 'satisfaction'], help='metric to be measured', required=True)
    argp.add_argument('--controller_host', help='address of unifi controller', required=True)
    argp.add_argument('--controller_user', help='login user for the controller', required=True)
    argp.add_argument('--controller_password', help='password for the controller', required=True)

    argp.print_help()
    args = argp.parse_args()
    print(args.hostname)
    print(args.metric)
    print(args.controller_host)
    print(args.controller_user)
    print(args.controller_password)

    check = nagiosplugin.Check(UnifiDevice(args.hostname))
    check.main()


if __name__ == '__main__':
    main()
