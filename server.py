import socket
import ipaddress

def hex_to_ip(hex_ip):
    return '.'.join([str(int(hex_ip[i:i+2], 16)) for i in range(0, 8, 2)])

def hex_to_port(hex_port):
    return int(hex_port, 16)

def main():
    SERVER_IP = '0.0.0.0'
    SERVER_PORT = 1720

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind((SERVER_IP, SERVER_PORT))
        server.listen(5) # Allow a backlog of 5 connections
        print(f"Listening on {SERVER_IP}:{SERVER_PORT}...")

        while True: 
            conn, addr = server.accept()
            with conn:
                client_ip, client_port = addr # Parse the client's connecting IP and port
                print(f"Connected by: {client_ip}:{client_port}")
                
                data = conn.recv(4096)
                if data:
                    payload_hex = data.hex()
                    local_ip_hex = payload_hex[50:58]
                    local_port_hex = payload_hex[58:62]

                    local_ip_str = hex_to_ip(local_ip_hex) # Keep as string for printing
                    local_port = hex_to_port(local_port_hex)

                    print(f"Received Remote IP (from payload): {local_ip_str}")
                    print(f"Received Remote Port (from payload): {local_port}")

                    try:
                        ip_obj = ipaddress.ip_address(local_ip_str)
                        if ip_obj.is_private:
                            print(f"*** WARNING: Received Remote IP {local_ip_str} is a PRIVATE IP address! ( H.323 traversal failed! ) ***")
                    except ipaddress.AddressValueError:
                        print(f"Error: Invalid IP address format received: {local_ip_str}")          
                    print("-" * 30)
                    conn.sendall(b"Server received your data!")
                else:
                    print(f"No data received from {client_ip}:{client_port}")
                    print("-" * 30)

if __name__ == '__main__':
    main()