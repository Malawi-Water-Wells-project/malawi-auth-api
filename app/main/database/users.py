# from .db_connection import get_db


# def create_users_table():
#     """
#     Creates the users table
#     """
#     db = get_db()

#     with db.cursor() as cur:
#         cur.execute("""
#             CREATE TABLE users IF NOT EXISTS (
#                 id SERIAL PRIMARY KEY,
#                 name VARCHAR(255),
#                 age INTEGER,
#                 role VARCHAR(5)
#             )
#         """)


# # create a user
# class User:
#     def __init__(self, name=None, age=None, role=None):
#         self.id = None
#         self.name = name
#         self.age = age
#         self.role = role

#     def save(self):
#         if self.id == None:
#             self._insert_user()
#         else:
#             self._update_user()

#     def _insert_user(self):
#         with get_cursor() as cur:
#             cur.execute("""
#                 INSERT INTO users (name, age, role)
#                 VALUES(%s, %d, %s)
#                 RETURNING id
#             """, (self.name, self.age, self.role))
#             last_added_id = cur.fetchone()[0]
#             return last_added_id

#     def _update_user(self):
#         with get_cursor() as cur:
#             cur.execute("""
#                 UPDATE users SET (
#                     name=%s,
#                     age=%d,
#                     role=%s,
#                 ) WHERE id=%d
#             """, (self.name, self.age, self.role, self.id))
