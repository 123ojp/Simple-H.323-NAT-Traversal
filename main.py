import socket
import argparse

def ip_to_hex(ip):
    return ''.join([format(int(x), '02x') for x in ip.split('.')])

def port_to_hex(port):
    # Pad to 4 characters (2 bytes)
    return format(int(port), '04x')

def main():
    parser = argparse.ArgumentParser(description='Forward IP and Port to Remote Server')
    parser.add_argument('-d', '--local-ip', required=True, help='Local IP to forward')
    parser.add_argument('-p', '--port', required=True, type=int, help='Local port to forward')
    parser.add_argument('-s', '--target-ip', required=True, help='Remote server IP')
    parser.add_argument('--target-port', type=int, default=1720, help='Remote server port (default: 1720)')
    args = parser.parse_args()

    payload_hex = (
        "0300003c08028a9c621c007e002e0526c0060008914a000700"
        + ip_to_hex(args.local_ip)
        + port_to_hex(args.port)
        + "22603011009c5b1a4e1a98eb1188be3464a92054580100010002800180"
    )
    payload = bytes.fromhex(payload_hex)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((args.target_ip, args.target_port))
        s.sendall(payload)
        response = s.recv(4096)
        print("Send!")

if __name__ == '__main__':
    main()