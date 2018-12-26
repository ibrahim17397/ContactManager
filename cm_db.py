import sqlite3



class database():
    dbcon = None



    def __init__(self):
        create_table_stmt = '''CREATE TABLE IF NOT EXISTS contact
                     (id INTEGER PRIMARY KEY AUTOINCREMENT, first_name text, last_name text, phone_number text, address text)'''

        self.exec_sql(create_table_stmt)



    def insert_contact(self, params):
        query = "INSERT INTO contact (first_name,last_name,phone_number,address) VALUES (?,?,?,?)"
        return self.exec_sql(query,params)



    def update_contact(self,params = ()):
        query = 'UPDATE contact SET first_name = ? , last_name = ? , phone_number = ?, address = ?  WHERE id = ?'
        return self.exec_sql(query,params)



    def delete_contact(self, contact_id):
        query = "DELETE FROM contact WHERE id = {}".format(contact_id)
        return self.exec_sql(query)



    def get_all_contacts(self,order_filter):
        query = "SELECT * FROM contact ORDER BY {} ASC".format(order_filter)
        return self.exec_sql(query)



    def get_contact(self,contact_id):
        query = "SELECT * FROM contact WHERE id = {}".format(contact_id)
        return self.exec_sql(query)



    def exec_sql(self, query, params=()):
        with sqlite3.connect('contacts.db') as self.dbcon:
            cursor=self.dbcon.cursor()
            query_result=cursor.execute(query,params)
            self.dbcon.commit()
            return query_result
