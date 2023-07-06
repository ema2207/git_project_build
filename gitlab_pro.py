# -*- coding: utf-8 -*-

import gitlab
import time

import dbm

class GitlabProject:
    def __init__(self,gitlab_url,gitlab_token):
        begin_time = time.time()
        self.__gitlab_url__ = gitlab_url
        self.__gitlab_token__ = gitlab_token
        self.__gl = gitlab.Gitlab(gitlab_url,gitlab_token)
        # 获取数据库配置需要排除的组名称
        ignore_group_array = dbm.get_ignore_gorups()
        # print(ignore_group_array)
        self.__groups = [g for g in self.__gl.groups.list(all=True) if g.name not in ignore_group_array]

        project_group_dict = {}
        ignore_project_array = dbm.get_ignore_projects()
        for group in self.__groups:
            projects = group.projects.list(all=True)
            projects = [p for p in projects if p.name not in ignore_project_array]
            tmpProjectArray = []
            for project in projects:
                tmpProject = self.__gl.projects.get(project.id)
                # print(tmpProject)
                tmpProject = GitlabProject.project_transfer(tmpProject)
                tmpProjectArray.append(tmpProject)
            project_group_dict[group.id] = tmpProjectArray
        self.__project_group_dict = project_group_dict
        print('初始化gitlab项目组以及项目耗时:{:.2f}秒'.format(time.time() - begin_time))

    def get_groups(self):
        return GitlabProject.groups_transfer(self.__groups)

    def get_gl(self):
        return self.__gl
    
    def get_project_by_groupId(self,group_id):
        # print(self.__project_group_dict)
        return self.__project_group_dict[group_id]

    def get_projects_by_group(self,gorup_id):
        begin_time = time.time()
        group = self.__gl.groups.get(gorup_id)
        projects = group.projects.list(all=True)
        print('获取当前组所有项目耗时:{:.2f}秒'.format(time.time() - begin_time))
        # 获取数据库配置需要排除的项目名称
        ignore_project_array = dbm.get_ignore_projects()
        # 排除需要忽略的项目名称
        projects = [p for p in projects if p.name not in ignore_project_array]
        print('排除项目耗时:{:.2f}秒'.format(time.time() - begin_time))
        project_array = []
        for pro in projects:
            project_id = pro.id
            begin_time1 = time.time()
            tmpProject =  self.__gl.projects.get(project_id)
            branch_list = tmpProject.branches.list()
            # 如果项目没有分支则丢弃
            if (len(branch_list) == 0):
                print("当前项目[{}]的分支数量[{}] ,跳过".format(pro.name,len(branch_list)))
                continue
            branchs = [b.name for b in branch_list]
            # branchs = GitlabProject.get_project_branchs(tmpProject)
            project_obj = {'id':tmpProject.id,
                'group_name':tmpProject.namespace['name'],
                'project_name':tmpProject.name,
                'ssh_url_to_repo':tmpProject.ssh_url_to_repo,
                'http_url_to_repo':tmpProject.http_url_to_repo,
                'path_with_namespace':tmpProject.path_with_namespace,
                'branchs':branchs}
            print('拼装项目耗时:{:.2f}秒'.format(time.time() - begin_time1))
            project_array.append(project_obj)
            
        run_time = time.time() - begin_time
        print('查询所有[%s]分组下所有项目耗时:%s' %(group.name,run_time))
        return project_array


    @staticmethod
    def groups_transfer(groups):
        groupArray = []
        for group in groups:
            tmp_group = {'id':group.id,'name':group.name,'web_url':group.web_url,'description':group.description}
            groupArray.append(tmp_group)
        return groupArray


    @staticmethod
    def get_project_branchs(project):
        branch_array = []
        branchs = project.branches.list()
        for b in branchs:
            branch_array.append(b.name)
        # return ','.join(branch_array)
        return branch_array

    @staticmethod
    def project_transfer(git_project):
        return {'id':git_project.id,
                'group_name':git_project.namespace['name'],
                'project_name':git_project.name,
                'ssh_url_to_repo':git_project.ssh_url_to_repo,
                'http_url_to_repo':git_project.http_url_to_repo,
                'path_with_namespace':git_project.path_with_namespace,
                'branchs':GitlabProject.get_project_branchs(git_project)}



if __name__ == '__main__':
    gitlab_url = 'http://aaa'
    gitlab_token = '1111'
    gp = GitlabProject(gitlab_url,gitlab_token)

    projects = gp.get_project_by_groupId(93)
    print(projects)

    # group_projectIds = gp.get_projects_by_group(88)
    # for pro in group_projectIds:
    #     project = gp.get_project_by_id(pro.id)
    #     print(GitlabProject.project_transfer(pro))
    #     break

    # for group in gp.get_groups():
    #     print(group)