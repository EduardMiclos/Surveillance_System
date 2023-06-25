import os
import telnetlib
from time import sleep

server_addr = os.environ.get('SERVER_ADDR')

if server_addr is None:
    print('[ERROR] No SERVER_ADDR environment variable! The automatic server-is-alive checker\
will not be able to send pings and receive answers!')
    print("Aborting...")
    exit(1)
    
server_port = os.environ.get('SERVER_PORT')

if server_port is None:
    print('[ERROR] No SERVER_PORT environment variable! The automatic server-is-alive checker\
will not be able to send pings and receive answers!')
    print("Aborting...")
    exit(1)


def check_server(host: str, port: int) -> bool:
    """
    Check if a server is reachable on a specific port.
    
    Args:
        host (str): The server's hostname or IP address.
        port (int): The port number to check.
        
    Returns:
        bool: True if the server is reachable, False otherwise.
    """
    try:
        with telnetlib.Telnet(host, port, timeout=5) as tn:
            return True
    except (ConnectionRefusedError, TimeoutError):
        return False

while True:

    if check_server(server_addr, server_port):
        print('[SUCCESS] Received response from the Central Server!')
        os.system(f'python main.py')
    else:
        print('[FAIL] No response from the Central Server.')
        print('[INFO] Retrying...')
        
    sleep(5)
