from core.database import db, db_connection
import pymysql

db.initialize(db_connection)

connection = pymysql.connect(
    host='140.238.215.73',
    port=3309,
    user='root',
    password='12345',
    database='jl_pdf_db'
)

# connection = pymysql.connect(
#     host='127.0.0.1',
#     port=3309,
#     user='root',
#     password='12345',
#     database='jl_pdf_db'
# )

def execute(query):
    db.execute(query)

user = """
create table if not exists users (
id int auto_increment primary key,
full_name varchar(50),
email varchar(50),
password varchar(255),
created_at bigint,
is_admin bool
)
"""

company = """
create table if not exists companies (
id int auto_increment primary key,
name varchar(50),
email varchar(50),
address varchar(100),
location varchar(100),
tax_id bigint,
created_at bigint
)
"""

project = """
create table if not exists projects(
id int auto_increment primary key,
name varchar(50),
comp_id int,
currency varchar(20),
created_at bigint,
foreign key (comp_id) references companies(id) on delete cascade
)
"""

pdf_data = """
create table if not exists pdf_data(
id int auto_increment primary key,
data text,
comp_id int,
proj_id int,
created_at bigint,
foreign key (comp_id) references companies(id) on delete cascade,
foreign key (proj_id) references projects(id) on delete cascade
)
"""

contracts = """
create table if not exists contracts(
id int auto_increment primary key,
name varchar(100),
data text,
comp_id int,
date varchar(100),
currency varchar(20),
foreign key (comp_id) references companies(id) on delete cascade
)
"""

tta_data = """
create table if not exists tta_data(
id int auto_increment primary key,
name varchar(100),
data text,
comp_id int,
contract_id int,
create_date varchar(50),
created_at bigint,
foreign key (comp_id) references companies(id) on delete cascade,
foreign key (contract_id) references contracts(id) on delete cascade
)
"""

q_list = [user, company, project, pdf_data, contracts, tta_data]


cursor = connection.cursor()

for q in q_list:
    cursor.execute(q)
    connection.commit()
    print(q)
cursor.close()
connection.close()