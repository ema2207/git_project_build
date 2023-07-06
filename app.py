from flask import Flask, render_template, request, redirect, url_for
# from werkzeug.wrappers import Response

import json
import time

import dbm
import gitlab_pro
import mvn_project
import make_print_to_file

dbm.init()

GitlabProject = gitlab_pro.GitlabProject
gitConfig = dbm.get_config()
gp = GitlabProject(gitConfig['gitlab_url'], gitConfig['gitlab_token'])

app = Flask(__name__)

"""
首页
"""
@app.route('/', methods=['GET'])
def index():
    begin_time = time.time()
    gitGroups = gp.get_groups()
    run_time = time.time() - begin_time
    print('查询所有分组耗时:', run_time)
    return render_template('index.html', gitGroups=gitGroups)


"""
根据分组id查询分组下的所有项目
"""
@app.route('/projects_by_group/<int:groupId>', methods=['POST'])
def projects_by_group(groupId):
    begin_time = time.time()
    projects = gp.get_project_by_groupId(groupId)
    print('耗时:{:.2f}秒'.format(time.time() - begin_time))
    res_obj = {'success': True, 'msg': '成功', 'data': projects}
    return json.dumps(res_obj), 200, {'content_type': 'application/json;charset=utf-8'}

"""
根据前端选中项目执行deploy
"""
@app.route('/deploy_project', methods=['POST'])
def deploy_project():
    page_data = request.get_data()
    if page_data is None or page_data == "":
        res_obj = {'success': Flask, 'msg': '请选择项目'}
        return json.dumps(res_obj), 200, {'content_type': 'application/json;charset=utf-8'}
    projects_json = json.loads(page_data)
    print(projects_json)
    mvn_project.mvn_project(projects_json)
    res_obj = {'success': True, 'msg': '成功', 'data': 0}
    return json.dumps(res_obj), 200, {'content_type': 'application/json;charset=utf-8'}


"""
查询所有忽略的项目名称
"""
@app.route('/ignore_projects', methods=['GET'])
def ignore_project():
    projects = dbm.query_all_ignore_projects()
    print(projects)
    return render_template('ignore_project.html', projects=projects, ignore_config=ignore_config('project'))


def ignore_config(type):
    ignore_config = {"add_url": "/add_ignore_project", "type": "project", "title": "忽略项目配置",
                     "sub_title": "GitLab忽略项目配置", "del_url": "/del_ignore_project", "filed_name": "project_name"}
    if type == "group":
        ignore_config = {"add_url": "/add_ignore_group", "type": "group", "title": "忽略群组配置",
                         "sub_title": "GitLab忽略群组配置", "del_url": "/del_ignore_group", "filed_name": "group_name"}
    return ignore_config


"""
保存要忽略的项目名称
"""
@app.route('/add_ignore_project', methods=['POST'])
def add_ignore_project():
    project_name = request.form['project_name']
    if len(project_name) != 0:
        dbm.save_ignore_project(project_name.strip())
    return redirect('ignore_projects')


"""
删除忽略的项目
"""
@app.route('/del_ignore_project/<int:id>', methods=['POST'])
def del_ignore_project(id):
    dbm.del_ignore_project(id)
    res_obj = {'success': True, 'msg': '成功'}
    return json.dumps(res_obj), 200, {'content_type': 'application/json;charset=utf-8'}


"""
查询所有忽略的群组名称
"""
@app.route('/ignore_groups', methods=['GET'])
def ignore_groups():
    projects = dbm.query_all_ignore_groups()
    return render_template('ignore_project.html', projects=projects, ignore_config=ignore_config('group'))


"""
保存要忽略的群组名称
"""
@app.route('/add_ignore_group', methods=['POST'])
def add_ignore_group():
    group_name = request.form['group_name']
    if len(group_name) != 0:
        dbm.save_ignore_group(group_name.strip())
    return redirect('ignore_groups')


"""
删除忽略的项目
"""
@app.route('/del_ignore_group/<int:id>', methods=['POST'])
def del_ignore_group(id):
    dbm.del_ignore_group(id)
    res_obj = {'success': True, 'msg': '成功'}
    return json.dumps(res_obj), 200, {'content_type': 'application/json;charset=utf-8'}


"""
获取git配置
"""
@app.route('/config', methods=['GET'])
def config():
    gitlab_config = dbm.get_config()
    return render_template('config.html', gitlab_config=gitlab_config)


"""
保存或更新git配置(如果数据库已存在git配置，则更新)
"""
@app.route('/save_config', methods=['POST'])
def save_config():
    gitlab_url = request.form['gitlab_url']
    gitlab_token = request.form['gitlab_token']
    dbm.save_config(gitlab_url, gitlab_token)
    return redirect(url_for('config'))


"""
重新加载git中的项目分组以及项目到内存中
"""
@app.route('/reload', methods=['GET'])
def reload():
    global gp
    gp = GitlabProject(gitConfig['gitlab_url'], gitConfig['gitlab_token'])
    res_obj = {'success': True, 'msg': '成功'}
    return json.dumps(res_obj), 200, {'content_type': 'application/json;charset=utf-8'}


"""
公共404错误页面
"""
@app.errorhandler(404)
def err_404(error):
    print(error)
    return render_template("404.html")


if __name__ == '__main__':
    make_print_to_file.make_print_to_file(path='./')
    # 再run()里面加入user_reloader=False参数，就可以解决 Restarting with stat
    app.run(debug=True, host='0.0.0.0', port=9001, use_reloader=False)
