import os
from HWSystem import HWSystem

access_key = os.environ.get('ACCESS_KEY')
base_route = os.environ.get('BASE_ROUTE')
sudo_pwd = os.environ.get('SUDO_PWD')

if access_key is None:
    print('[ERROR] No ACCES_KEY environment variable! The HW System will\
 not be able to connect to the Central Server!')
    print("Aborting...")
    exit(1)

if base_route is None:
    print('[ERROR] No BASE_ROUTE environment variable! The HW System doesn\'t\
 know what is the address of the Central Server!')
    print("Aborting...")
    exit(1)
    
if sudo_pwd is None:
    print('[ERROR] No SUDO_PWD environment variable! The HW System will not\
 be able to perform automatic updates!')
    print("Aborting...")
    exit(1)

hw_system = HWSystem(access_key, base_route, sudo_pwd)
hw_system.start_module()

