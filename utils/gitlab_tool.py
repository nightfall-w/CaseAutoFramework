import os
import time
import gitlab

from automation.settings import logger


class GitlabAPI(object):

    def __init__(self, gitlab_url, private_token, *args, **kwargs):
        self.gitlab_url = gitlab_url
        self.token = private_token
        self.gl = gitlab.Gitlab(url=self.gitlab_url, private_token=self.token) # 参数为gitlab仓库地址和个人private_token

    def get_user_id(self, username):
        """
        通过用户名获取用户id
        :param username:
        :return:
        """
        user = self.gl.users.get_by_username(username)
        return user.id

    def get_project_id(self, id):
        project = self.gl.projects.get(id)
        return project

    def get_group_id(self, groupname):
        """
        通过组名获取组id
        :param groupname:
        :return:
        """
        group = self.gl.groups.get(groupname, all=True)
        return group.id

    def get_user_projects(self, userid):
        """
        获取用户所拥有的项目
        :param userid:
        :return:
        """
        projects = self.gl.projects.owned(userid=userid, all=True)
        result_list = []
        for project in projects:
            result_list.append(project.http_url_to_repo)
        return result_list

    def get_group_projects(self, groupname):
        """
        获取组内项目！！！！！！！其他博客也有类似方法，实测不能拿到群组内项目，现经过小改动，亲测可满足要求
        :param groupname:
        :return:
        """
        group = self.gl.groups.get(groupname, all=True)
        projects = group.projects.list(all=True)
        return projects

    # 由于是递归方式下载的所以要先创建项目相应目录
    def create_dir(self, dir_name):
        if not os.path.isdir(dir_name):
            logger.info("\033[0;32;40m开始创建目录: \033[0m{0}".format(dir_name))
            os.makedirs(dir_name)
            time.sleep(0.1)

    def get_content(self, project_id):
        """
        通过项目id获取文件内容
        :param projectID:
        :return:
        """
        projects = self.gl.projects.get(project_id)
        f = projects.files.get(file_path='指定项目中的文件路径', ref='master')
        content = f.decode()
        return content.decode('utf-8')

    def get_all_group(self):
        """
        获取所有群组
        :return:
        """
        return self.gl.groups.list(all=True)

    def pull(self, project_id, branch, root_path):

        project = self.get_project_id(project_id)
        info = project.repository_tree(all=True, recursive=True, as_list=True)
        file_list = []
        if not os.path.isdir(root_path):
            os.makedirs(root_path)
        os.chdir(root_path)
        # 调用创建目录的函数并生成文件名列表
        for info_dir in range(len(info)):
            if info[info_dir]['type'] == 'tree':
                dir_name = info[info_dir]['path']
                self.create_dir(dir_name)
            else:
                file_name = info[info_dir]['path']
                file_list.append(file_name)
        for info_file in range(len(file_list)):
            # 开始下载
            getf = project.files.get(file_path=file_list[info_file], ref=branch)
            content = getf.decode()
            with open(file_list[info_file], 'wb') as code:
                logger.info("\033[0;32;40m开始下载文件: \033[0m{0}".format(file_list[info_file]))
                code.write(content)
