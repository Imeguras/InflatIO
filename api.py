import sqlalchemy as db
from sqlalchemy.orm import sessionmaker
import models as m
from config import dbconfig
import paramiko
import sshtunnel

try:
	print("Connecting to database...")
	params = dbconfig()
	#print(params)
	engine = db.create_engine('postgresql://'+params["user"]+':'+params["password"]+'@'+params["internal_host"]+':' +params["internal_port"]+'/'+params["database"])

	Session = sessionmaker(bind=engine)
	session = Session()
	
	query = session.query(m.Product).all()
	for product in query:
		print(product)
	
except Exception as e:
	print(e)
#print(params)
# with sshtunnel.SSHTunnelForwarder(
#     (params['ssh_host'] , int(params['ssh_port'])),
#     ssh_username=params['ssh_user'],
#     ssh_password=params['ssh_password'],
#     ssh_host_key="/home/micron/.ssh/known_hosts",
#     ssh_pkey=params['ssh_private_key'],
# 	ssh_proxy_enabled=False, 
#     ssh_private_key_password=params['ssh_password'],
#     remote_bind_address=(params['ssh_host'], int(params['ssh_port']))
# )as server:
# 	print("hello")
# 	conn = sqlalchemy.create_engine("postgres://%s:%s@%s:%s/%s", 
# 										params['user'], 
# 										params['password'],
# 										params['internal_host'],
# 										params['internal_port'],
# 										params['database']