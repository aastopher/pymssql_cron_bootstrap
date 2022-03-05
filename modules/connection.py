from cryptography.fernet import Fernet
import pymssql
import socket

from modules.setup import *

# Instantiate loggers
DL = DeepLogger('connection',['decrypt','socket','connect'])
decryptLogger = DL.getLogger('decrypt')
socketLogger = DL.getLogger('socket')
connectLogger = DL.getLogger('connect')
infoLogger = DL.getLogger('console')

# PORT LOOKUP SERVICE
# Error Classes
class Error(Exception):
    """Base class for exceptions in this module."""
    pass

class BrowserError(Error):
    """Problem communicating with the SQL Browser service.
    """
    def __init__(self, message):
        self.message = message

class NoTcpError(Error):
    """Instance not configured for TCP/IP connections.
    """
    def __init__(self, message):
        self.message = message

# Query the SQL Browser service and extract the port number
def lookup(server, instance):
    """Query the SQL Browser service and extract the port number
    :type server: str
    :type instance: str
    """
    udp_port = 1434
    # define message type per SQL Server Resolution Protocol
    udp_message_type = b"\x04"  # CLNT_UCAST_INST (client, unicast, instance)

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.settimeout(5)

    # create isntance message
    udp_message = udp_message_type + instance.encode()
    try:
        socketLogger.info('establishing connection to SQL Browser Service...')

        # send message to server
        sock.sendto(udp_message, (server, udp_port))
        response = sock.recv(1024)  # max 1024 bytes for CLNT_UCAST_INST

        socketLogger.info('SUCCESSFUL connection to SQL Browser Service')

        # decode response
        response_list = response[3:].decode().split(";")
        response_dict = {
            response_list[i]: response_list[i + 1]
            for i in range(0, len(response_list), 2)
        }

        # return port
        return int(response_dict["tcp"])

    except KeyError as no_tcp:
        raise NoTcpError(
            r"Instance \{} is not configured to accept TCP/IP connections.".format(
                instance
            )
        )
        socketLogger.info(f'FAILED connection to SQL Browser Service: {NoTcpError}')
    except socket.timeout as no_response:
        raise BrowserError(
            r"No response from the SQL Browser service. "
            r"Verify that the service is available on "
            r"{0} and \{1} is a valid instance name on it.".format(
                server, instance
            )
        )
        socketLogger.info(f'FAILED connection to SQL Browser Service: {BrowserError}')
    except ConnectionResetError as no_connect:
        raise BrowserError(
            "Cannot connect to the SQL Browser service on {} .".format(server)
        )
        socketLogger.info(f'FAILED connection to SQL Browser Service: {BrowserError}')

# CONNECTION PROCESS
# input files
key_file = 'CFG/key.txt'
input_file = 'CFG/en_conn.cfg'
try:
    decryptLogger.info('attempting to decrypt configuration files...')

    with open(key_file,'rb') as k:
        key = k.read()

    with open(input_file,'rb') as f:
        data = f.read()

    # decrypt file and pass values to variables
    fernet = Fernet(key)
    decrypted = fernet.decrypt(data)

    cfg = str(decrypted)[2:-1].split(',')
    server=cfg[0]
    user=cfg[1]
    password=cfg[2]
    database=cfg[3]
    instance_name=cfg[4][:-4]

    decryptLogger.info('SUCCESSFUL decryption')
except Exception as e:
    decryptLogger.info(f'FAILED decryption: {e}')
    print(f'FAILED decryption: {e}')

# use sockets to discover IP of server
try:
    socketLogger.info('attempting ip discovery...')
    server_ip = socket.gethostbyname(server)
    socketLogger.info('SUCCESSFUL ip discovery')
except Exception as e:
    socketLogger.info(f'FAILED ip discovery: {e}')
    print(f'FAILED ip discovery: {e}')
    exit(1)
# establish socket connection to SQL browser service to discover tcp port of the named instance
try:
    socketLogger.info('attempting port discovery...')
    port = lookup(server, instance_name)
    socketLogger.info('SUCCESSFUL port discovery')
except Exception as e:
    port = -1
    socketLogger.info(f'FAILED port discovery: {e}')
    print(f'FAILED port discovery: {e}')
    exit(1)

server_ip_port = f'{server_ip}:{port}'

# Attempt a connection to the server\instance
try:
    connectLogger.info(f'attempting a connection to DB: {database} via {server}\\{instance_name} using IP: {server_ip} and PORT: {port}')
    conn = pymssql.connect(server=server_ip_port, user=user, password=password, database=database)
    cursor = conn.cursor()
    connectLogger.info(f'SUCCESSFUL connection to DB: {database} via {server}\\{instance_name} using IP: {server_ip} and PORT: {port}')
except Exception as e:
    connectLogger.info(f'FAILED connection to DB: {database} via {server}\\{instance_name} using IP: {server_ip} and PORT: {port}')
    print(f'FAILED connection to DB: {database} via {server}\\{instance_name} using IP: {server_ip} and PORT: {port}')
    exit(1)
