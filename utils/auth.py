import streamlit as st
import aiomysql
import asyncio
import mysql.connector
from decouple import config
from passlib.context import CryptContext

pwd_context = CryptContext(
    schemes=["django_pbkdf2_sha256"],
    deprecated="auto"
)
#async def get_db_connection():
#    return await aiomysql.connect(
#        host=config('DATABASE_HOST_MYSQL'),
#        user=config('DATABASE_USER_MYSQL'),
#        password=config('DATABASE_PASSWORD_MYSQL'),
#        db=config('DATABASE_NAME_MYSQL'),
#        port = 25060
        
#    )

def get_db_connection():
    return mysql.connector.connect(
        host=config('DATABASE_HOST_MYSQL'),
        user=config('DATABASE_USER_MYSQL'),
        password=config('DATABASE_PASSWORD_MYSQL'),
        database=config('DATABASE_NAME_MYSQL'),
        port = 25060
        
    )
    
def authenticate(username, password):
    conn = get_db_connection()
    cursor = conn.cursor(buffered=True)
    cursor.execute('SELECT username, password FROM auth_user WHERE username = %s', (username,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    print(user)
    if user:
        stored_username, stored_password_hash = user
        print(stored_username)
        if pwd_context.verify(password, stored_password_hash):
            print(stored_username)
            return stored_username
    
    return None

def get_data_user(username):
    conn = get_db_connection()
    cursor = conn.cursor(buffered=True)
    cursor.execute(
                f"""
                select
                    u.username,
                    p.avatar_profile as "image_profile",
                    c.ruc,
                    cate.description as "rubro",
                    c.description as "empresa",
                    c.avatar_profile as "image_company",
                    c.ip,
                    c.token,
                    c.type_con,
                    c.parquet,
                    r.description
                from auth_user as u 
                    inner join management_profile as p on u.id = p.user_id
                    inner join management_role as r on p.role_id = r.id
                    inner join management_company as c on p.company_id = c.id
                    inner join management_category as cate on c.category_id = cate.id
                where u.username = '{username}'
                """
            )
    data = cursor.fetchone()
    cursor.close()  
    conn.close()
    return data


"""
async def authenticate(username, password):
    conn = await get_db_connection()
    async with conn.cursor() as cursor:
        await cursor.execute(f'SELECT username, password FROM auth_user WHERE username = %s', (username,))
        user = await cursor.fetchone()
    await conn.ensure_closed()
    
    if user:
        stored_username, stored_password_hash = user
        if pwd_context.verify(password, stored_password_hash):
            return stored_username
    return None
"""
"""
def authenticate(username, password):
    conn = get_db_connection()
    cursor = conn.cursor(buffered=True)
    cursor.execute('SELECT username, password FROM auth_user WHERE username = %s', (username,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    
    if user:
        stored_username, stored_password_hash = user
        if pwd_context.verify(password, stored_password_hash):
            cursor2 = conn.cursor(buffered=True)
            cursor2.execute(
                
                select
                    u.username,
                    p.avatar_profile as "image_profile",
                    c.ruc,
                    cate.description as "rubro",
                    c.description as "empresa",
                    c.avatar_profile as "image_company",
                    c.ip,
                    c.token,
                    c.type_con,
                    c.parquet,
                    r.description
                from auth_user as u 
                    inner join management_profile as p on u.id = p.user_id
                    inner join management_role as r on p.role_id = r.id
                    inner join management_company as c on p.company_id = c.id
                    inner join management_category as cate on c.category_id = cate.id
                where u.username = '{username}'
                
            )

            data = cursor2.fetchone()
            cursor2.close()  
            cursor2.close()
            #print()
            return data
    return None


"""
