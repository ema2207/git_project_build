# -*- coding: utf-8 -*-

import sqlite3
import os

import lconfig

"""
初始化数据库，数据库不存在则创建
"""
def init():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS t_gitlab_config (id INTEGER PRIMARY KEY AUTOINCREMENT, gitlab_url varchar(255) NOT NULL, gitlab_token varchar(255) NOT NULL)"
    )

    cursor.execute(
        "CREATE TABLE IF NOT EXISTS t_ignore_projects (id INTEGER PRIMARY KEY AUTOINCREMENT, project_name varchar(255) NOT NULL)"
    )

    cursor.execute(
        "CREATE TABLE IF NOT EXISTS t_ignore_groups (id INTEGER PRIMARY KEY AUTOINCREMENT, group_name varchar(255) NOT NULL)"
    )

    conn.commit()
    conn.close()

"""
获取数据库连接
"""
def get_db_connection():
    db_abs_path = os.path.abspath(os.path.join(lconfig.DB_PATH, lconfig.DB_NAME))
    print('数据库地址:'+db_abs_path)
    conn = sqlite3.connect(db_abs_path)
    return conn


def get_ignore_gorups():
    ignore_groups = query_all_ignore_groups()
    ignore_group_array = []
    for group in ignore_groups:
        ignore_group_array.append(group[1])
    # print(ignore_group_array)
    return ignore_group_array

"""
查询要忽略的组名
"""
def query_all_ignore_groups():
    conn = get_db_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM t_ignore_groups")
    ignoreGroups = cursor.fetchall()
    conn.close()
    return ignoreGroups
    
"""
保存忽略的项目名
"""
def save_ignore_group(group_name):
    conn = get_db_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT count(1) FROM t_ignore_groups where group_name = ?", (group_name,))
    result = cursor.fetchone()
    if result[0] == 0 :
        cursor.execute("insert into t_ignore_groups (group_name) values (?)", (group_name,))
        conn.commit()
    conn.close()

def del_ignore_group(project_id):
    conn = get_db_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('delete from t_ignore_groups where id=?', (project_id,))
    conn.commit()
    conn.close()


def get_ignore_projects():
    ignore_projects = query_all_ignore_projects()
    ignore_project_array = []
    for project in ignore_projects:
        ignore_project_array.append(project[1])
    
    return ignore_project_array
"""
查询要忽略的项目名
"""
def query_all_ignore_projects():
    conn = get_db_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM t_ignore_projects")
    ignoreGroups = cursor.fetchall()
    conn.close()
    return ignoreGroups
    
"""
保存忽略的项目名
"""
def save_ignore_project(project_name):
    conn = get_db_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT count(1) FROM t_ignore_projects where project_name = ?", (project_name,))
    result = cursor.fetchone()
    if result[0] == 0 :
        # print("项目"+project_name+"不存在表中，执行保存...")
        cursor.execute("insert into t_ignore_projects (project_name) values (?)", (project_name,))
        conn.commit()
    conn.close()

def del_ignore_project(project_id):
    conn = get_db_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('delete from t_ignore_projects where id=?', (project_id,))
    conn.commit()
    conn.close()

"""
执行脚本
"""
def exe_sql(sql):
    conn = get_db_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(sql)
    cursor.close()
    conn.commit()
    conn.close()
    

"""
保存或更新gitlab配置
"""
def save_config(gitlab_url,gitlab_token):
    conn = get_db_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM t_gitlab_config")
    config_exists = cursor.fetchone()

    if config_exists:
        cursor.execute("UPDATE t_gitlab_config SET gitlab_url=?, gitlab_token=?", (gitlab_url, gitlab_token))
    else:
        cursor.execute("INSERT INTO t_gitlab_config (gitlab_url, gitlab_token) VALUES (?, ?)", (gitlab_url, gitlab_token))

    conn.commit()
    conn.close()

"""
查询gitlab配置
"""
def get_config():
    conn = get_db_connection()
    conn.row_factory = dict_factory
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM t_gitlab_config")
    gitlab_config = cursor.fetchone()
    # print(gitlab_config)
    conn.close()
    return gitlab_config

def dict_factory(cursor,row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

if __name__ == '__main__':
    # get_ignore_gorups()
    # print(get_config())
    # save_config("", "" )
    pass