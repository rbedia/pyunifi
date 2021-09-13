import argparse
import sys

from pyunifi.controller import Controller


class UnifiNrpe:

    OK = 0
    WARNING = 1
    CRITICAL = 2
    UNKNOWN = 3
    nagios_prefixes = {
        OK: 'OK',
        WARNING: 'WARNING',
        CRITICAL: 'CRITICAL',
        UNKNOWN: 'UNKNOWN'
    }

    def parse_args(self):
        parser = argparse.ArgumentParser()
        parser.add_argument(
            '-H', '--hostname', default='unifi',
            help='the controller address (default "unifi")')
        parser.add_argument(
            '-u', '--username', default='admin',
            help='the controller username (default("admin")')
        parser.add_argument(
            '-p', '--password', default='',
            help='the controller password')
        parser.add_argument(
            '-b', '--port', default='8443',
            help='the controller port (default "8443")')
        parser.add_argument(
            '-v', '--version', default='v5',
            help='the controller base version (default "v5")')
        parser.add_argument(
            '-s', '--siteid', default='default',
            help='the site ID, UniFi >=3.x only (default "default")')
        parser.add_argument(
            '-V', '--no-ssl-verify', default=False, action='store_true',
            help='Don\'t verify ssl certificates')
        parser.add_argument(
            '-C', '--certificate', default='',
            help='verify with ssl certificate pem file')
        self.additional_args(parser)
        args = parser.parse_args()
        return args

    def additional_args(self, parser):
        pass

    def start(self):
        args = self.parse_args()
        self.args = args
        ssl_verify = (not args.no_ssl_verify)

        if ssl_verify and len(args.certificate) > 0:
                ssl_verify = args.certificate

        unifi = Controller(
            args.hostname,
            args.username,
            args.password,
            args.port,
            args.version,
            args.siteid,
            ssl_verify=ssl_verify
        )
        code, message = self.check(unifi)
        self.nrpe_response(code, message)

    def nrpe_response(self, code, message):
        code_text = self.nagios_prefixes[code]
        print(f'{code_text}: {message}')
        sys.exit(code)
