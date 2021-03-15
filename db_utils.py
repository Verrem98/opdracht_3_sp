import psycopg2


def get_sql_connection(psycopg2):
    connection = psycopg2.connect(user="postgres",
                                  password="emiel.verhoef@student.hu.nl",
                                  host="localhost",
                                  port="5432",
                                  database="AI_group_project")
    return connection


def open_db_connection():
    'opens db connection'

    global connection, cursor
    try:
        connection = get_sql_connection(psycopg2)
        cursor = connection.cursor()
    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)


def close_db_connection():
    'closes DB connection and commits'

    # closing database connection.
    if connection:
        connection.commit()
        cursor.close()
        connection.close()


def create_category_recs_table(category_type):
    'Creates a table for category recommendations'
    open_db_connection()

    cursor.execute(
        f"select distinct {category_type} from product_categories pc where {category_type} is not null")

    data = cursor.fetchall()

    # create table
    cursor.execute(
        f"create table {category_type}_recs(category varchar primary key, rec_1 varchar, rec_2 varchar, rec_3 varchar, rec_4 varchar)"
    )

    # make a list of all categories
    category_list = []
    for category in data:
        category = str(category[0])
        category_list.append(category)

    category_list = [x.replace("'", "''") for x in category_list]

    # make a list of all recs
    id_list = []
    for category in category_list:
        cursor.execute(
            f"""select p.product_id from products p inner join product_categories pc on p.product_id = pc.product_id where pc.{category_type} like '{category}' limit 4""")
        data = cursor.fetchall()
        temp_id_list = []
        for id in data:
            temp_id_list.append(id[0])
        id_list.append(temp_id_list)

    # make sure that when there are less than 4 recs, to fill it with None
    for x in range(len(id_list)):
        for i in range(4 - (len(id_list[x]))):
            id_list[x].append('NULL')

    # insert recs + category in DB
    for x in range(len(category_list)):

        for i in range(4):
            if (id_list[x][i] != 'NULL'):
                id_list[x][i] = f"'{id_list[x][i]}'"

        cursor.execute(
            f"insert into {category_type}_recs(category,rec_1,rec_2,rec_3,rec_4) values('{category_list[x]}',{id_list[x][0]},{id_list[x][1]},{id_list[x][2]},{id_list[x][3]})"
        )

    close_db_connection()


def create_user_orders_rec(name):
    open_db_connection()

    # create table
    cursor.execute(
        f"create table {name}(product_id varchar primary key, rec_1 varchar, rec_2 varchar, rec_3 varchar, rec_4 varchar)"
    )

    cursor.execute(
        "select product_id from products"
    )
    data = cursor.fetchall()
    id_list = []

    # replacing ' with '' so LIKE in the sql statement doesn't fuck up
    id_list = [id[0].replace("'", "''") for id in data]

    rec_list = []
    for count, product_id in enumerate(id_list):
        # using a subquery to fetch the 4 products most often bought together with product "product_id" that don't share the same sub_sub_category

        if name == 'order_recs':

            q = f"""select product_id ,count(product_id) as product_id_count 
                    from product_in_order pio2  
                    where session_id in (select session_id  from product_in_order pio  where product_id like '{product_id}')
                    and product_id not like '{product_id}' 
                    group by product_id  
                    order by product_id_count desc limit 4"""

        elif name == 'order_recs_dif_cat':
            q = f"""select pio2.product_id ,count(pio2.product_id) as product_id_count
                    from product_in_order pio2 inner join product_categories pc on pc.product_id = pio2.product_id
                    where session_id in (select session_id  from product_in_order pio  where product_id like '{product_id}')
                    and sub_sub_category is not null and pio2.product_id not like '{product_id}'
                    and pc.sub_sub_category not in (select sub_sub_category from product_categories pc2 where product_id like '{product_id}')
                    group by pio2.product_id , pc.sub_sub_category
                    order by product_id_count
                    desc limit 4"""

        cursor.execute(q)

        data = cursor.fetchall()
        id_recs = [x[0] for x in data]

        for i in range(4 - (len(id_recs))):
            id_recs.append('NULL')

        for i in range(len(id_recs)):
            if (id_recs[i] != 'NULL'):
                id_recs[i] = f"'{id_recs[i]}'"

        rec_list.append(id_recs)
        cursor.execute(
            f"insert into {name}(product_id,rec_1,rec_2,rec_3,rec_4) values('{product_id}',{id_recs[0]},{id_recs[1]},{id_recs[2]},{id_recs[3]})"
        )

        # commit every 2000 rows
        if count % 2000 == 0:
            close_db_connection()
            open_db_connection()

    close_db_connection()


def create_rec_tables():

    create_category_recs_table('category')
    create_category_recs_table('sub_category')
    create_category_recs_table('sub_sub_category')

    create_user_orders_rec('order_recs')
    create_user_orders_rec('order_recs_dif_cat')



