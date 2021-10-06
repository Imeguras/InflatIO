import getpass
import os
import socket
import select
try:
    import SocketServer
except ImportError:
    import socketserver as SocketServer
import sys
from optparse import OptionParser
import paramiko
from config import dbconfig


def main():
    params = dbconfig()
    password = params['ssh_password']
    if !password:
        password = getpass.getpass("Enter SSH Key password: ")

    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.WarningPolicy())

    verbose("Connecting to ssh host %s:%s ..." % (params['local_host'], params['local_port']))
    try:
        client.connect(
            params['local_host'],
            params['local_port'],
            username=params['local_user'],
            key_filename=params['ssh_private_key'],
            look_for_keys=True,
            password=params['ssh_password'],
        )
    except Exception as e:
        print("*** Failed to connect to %s:%d: %r" % (params['local_host'], params['local_port'], e))
        sys.exit(1)
    verbose(
        "Now forwarding port %d to %s:%d ..."
        % (options.port, remote[0], remote[1])
    )

    try:
        forward_tunnel(
            options.port, remote[0], remote[1], client.get_transport()
        )
    except KeyboardInterrupt:
        print("C-c: Port forwarding stopped.")
        sys.exit(0)


if __name__ == "__main__":
    main()