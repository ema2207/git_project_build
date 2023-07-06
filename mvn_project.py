
import os
import sys
import subprocess, shlex
import time

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

import lconfig

POM_NS = "{http://maven.apache.org/POM/4.0.0}"

## 当前项目根目录
current_path = os.getcwd()

def mvn_project(projects):
    group_name = projects['group_name']
    # print("执行%s分组下%s项目的deploy" % (group_name,projects['projects']))
    project_stroage_path = lconfig.TMP_PATH + "/" + lconfig.PROJECT_PATH +"/"
    project_path_array = []
    for pro in projects['projects']:
        thisProjectPath = project_stroage_path + pro['path_with_namespace']
        print(thisProjectPath)
        branch = pro['branch']
        git_url = pro['ssh_url_to_repo']
        # git_url = pro['http_url_to_repo']
        subprocess_cmd = ['git','clone','-b',branch,'--single-branch',git_url,thisProjectPath]
        # clone_command = shlex.split('git clone -b %s --single-branch %s %s' % (branch,git_url, thisProjectPath))
        if os.path.exists(thisProjectPath):
            # command = shlex.split('rm -rf "%s" ' % (thisProjectPath))
            # subprocess.Popen(command)
            del_command_str = "rm -rf %s" %(thisProjectPath)
            os.system(del_command_str)
            print("先删除项目，删除成功....")
        
        # clone_cmd_str = 'git clone -b %s --single-branch %s %s' % (branch,pro['http_url_to_repo'], thisProjectPath)
        # os.system(clone_cmd_str)
        print("克隆命令:%s" %(subprocess_cmd))
        p = subprocess.Popen(subprocess_cmd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        stdout, sdterr = p.communicate()
        print(stdout.decode('utf-8'))
        # print(sdterr.decode('utf-8'))
        p.wait()
        print(p.poll())
        # print("克隆命令:%s" %(clone_cmd_str))
        parse_pom(thisProjectPath)
        # subprocess.Popen(clone_command)
    #     project_path_array.append(thisProjectPath)
    # parse_base_pom(project_path_array)

def parse_pom(project_path):
    pom_path = os.path.join(project_path,"pom.xml")
    print("pom_path = %s " % (pom_path))
    pom_path_exists = os.path.exists(pom_path)
    print('-----------------------------')
    print(pom_path_exists)
    print('-----------------------------')
    if(bool(pom_path_exists) is False):
        print("项目：%s ,未clone完成，重新执行parse_pom" % (pom_path))
        time.sleep(1)
        parse_pom(project_path)

    tree = ET.ElementTree(file=pom_path)
    root = tree.getroot()
    el_moudules = root.find('%smodules' % POM_NS)
    print('解析到pom.xml文件中modules节点 : %s' % (el_moudules))
    if el_moudules is not None:
        for child in root.iter('%smodule' % POM_NS):
            moudle_project = child.text
            if "-api" in moudle_project:
            # if(moudle_project.find("-api") > 0):
                print(os.system('pwd'))
                tmp_project_path = os.path.join(project_path,moudle_project)
                # print(project_path)
                mvn_deploy(tmp_project_path)
    else:
        mvn_deploy(project_path)

def parse_base_pom(project_path_array):
    for project_path in project_path_array:
        parse_pom(project_path)
            
def mvn_deploy(project_path):
    print(os.system('pwd'))
    
    print('进入目录 : %s'%(project_path))
    api_pom_path = os.path.join(project_path,"pom.xml")
    print('项目的pom路径:%s' % (api_pom_path))

    pom_path_exists = os.path.exists(api_pom_path)
    print('============================')
    print(pom_path_exists)
    print('============================')
    if(pom_path_exists):
        os.chdir(project_path)
        print("执行 %s 项目 mvn deploy 命令" % (project_path))
        # os.system('mvn deploy -DskipTests=true ')
        deploy_command = shlex.split('mvn deploy -DskipTests=true')
        p = subprocess.Popen(deploy_command,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        stdout, sdterr = p.communicate()
        print(stdout.decode('utf-8'))
        # print(sdterr.decode('utf-8'))
        # p.wait()
        print(p.poll())
        os.chdir(current_path)
    else:
        time.sleep(1)
        print("项目路径:%s 还未克隆完到本地，重新执行deploy" % (project_path))
        mvn_deploy(project_path)

if __name__ == '__main__':
    tree = ET.ElementTree(file='tmp/project/common-service/zcckj-live-common/pom.xml')
    root = tree.getroot()
    el_moudules = root.find('%smodules' % POM_NS)
    print('解析到pom.xml文件中modules节点 : %s' % (el_moudules))