import sqlalchemy
from config import dbconfig
import paramiko


params = dbconfig()
#tunnel = sshtunnel.open_tunnel()
# with sshtunnel.SSHTunnelForwarder(
#     #(params['internal_host'] , int(params['internal_port'])),
#     ssh_username=params['ssh_user'],
#     ssh_private_key=params['ssh_private_key'],
#     ssh_private_key_password=params['ssh_password'],
#     remote_bind_address=(params['ssh_host'], int(params['ssh_port']))
# ) as server:
#     conn = sqlalchemy.create_engine("postgres://%s:%s@%s:%s/%s", 
#                                         params['user'], 
#                                         params['password'],
#                                         params['internal_host'],
#                                         params['internal_port'],
#                                         params['database'])

#engine = sqlalchemy.create_engine("postgres://%s:password@server:port/database", params["User"], params["User"])
#Base.metadata.create_all(engine)

#session = sessionmaker(engine)()
