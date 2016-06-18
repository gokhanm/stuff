#!/usr/bin/env python3
"""
gitlab: https://github.com/pyapi-gitlab/pyapi-gitlab
jira  : https://github.com/pycontribs/jira

"""
import datetime
import requests
import re
import sys
import gitlab
from jira import JIRA

from config import git_server_url
from config import git_token
from config import jira_url
from config import jira_user
from config import jira_passwd

__author__ = 'Gokhan MANKARA'
__email__ = 'gokhan@mankara.org'


refs = sys.argv[1]
repo_path = sys.argv[2]

project_name = repo_path.split('/')[-1].split('.')[0]
g_name = repo_path.split('/')[-2]

requests.packages.urllib3.disable_warnings()


class Gitlab:
    def __init__(self):
        self.git = gitlab.Gitlab(git_server_url, token=git_token, verify_ssl=False)


    def main(self):

        for i in self.git.getprojectsall(page=1, per_page=200):
            if i["namespace"]["name"] == g_name and i['path'] == project_name:
                group_name = i['namespace']['name']
                project_id = i["id"]
                commit_dict = self.git.getrepositorycommit(project_id, refs)

                return commit_dict, group_name



class Jira:
    def __init__(self):

        options = {
                'server': jira_url, 'verify': False, 'check_update': False
                    }

        self.jira = JIRA(options, basic_auth=(jira_user, jira_passwd))

    def main(self, comment, group_name):
        message = comment['message'].split('\n')[0]
        commit_sha1 = comment['id']
        author = comment['author_name']
        commited_date = comment['committed_date'].split('+')[0]

        date = datetime.datetime.strptime(commited_date, "%Y-%m-%dT%H:%M:%S.%f")

        projects = self.jira.projects()
        project_keys = sorted([project.key for project in projects])

        for keys in project_keys:
            if message.startswith(keys):

                issue_id = message.split(' ')[0]

                try:
                    comment_msg = ' '.join(message.split(' ')[1:])
                except IndexError:
                    comment_msg = issue_id
    
                compare_url = "%s/%s/%s/commit/%s" % (git_server_url, group_name, project_name, refs)

                msg = '%s\n\nProject Repo: %s\nUser: %s\nCommit Time: %s\nCommit SHA1: [%s | %s]\n\n' %\
                        (comment_msg, project_name, author, date, commit_sha1, compare_url)

                comment = self.jira.add_comment(issue_id, msg)


if __name__ == "__main__":

    g = Gitlab()
    j = Jira()
    cmm, grp_name = g.main()

    j.main(cmm, grp_name)
