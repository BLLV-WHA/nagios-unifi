import argparse
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
                state = False
                if ap['state'] == 1:
                    state = True
                return [nagiosplugin.Metric('status', state, context='null')]

        raise nagiosplugin.CheckError('unable to find specified device: {}'.format(self._hostname))


@nagiosplugin.guarded
def main():
    argp = argparse.ArgumentParser()
    argp.add_argument('-H', '--hostname', help='name of the unifi device')
    args = argp.parse_args()
    print(args)
    check = nagiosplugin.Check(UnifiDevice(args.hostname))
    check.main()


if __name__ == '__main__':
    main()
