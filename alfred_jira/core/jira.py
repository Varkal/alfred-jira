import requests
import json


class Jira:
    base_url = ""
    auth = ()

    ignored_statuses = ""
    watched_projects = ""
    closed_statuses = {}

    def __init__(self, config):
        self.base_url = config["base_url"]
        self.auth = (config["auth"]["mail"], config["auth"]["token"])
        self.ignored_statuses = ",".join(config["ignored_statuses"])
        self.watched_projects = ",".join([project["name"] for project in config["watched_projects"]])
        self.closed_statuses = {
            project.get("name", ""): project.get("closed_status", "") for project
            in config["watched_projects"] if project.get("closed_status", False)
        }

    def __request(self, **kwargs):
        response = requests.request(
            auth=self.auth,
            **kwargs
        )

        try:
            response = response.json()
        except json.JSONDecodeError:
            response = response.text

        return response

    def close(self, issue_key):
        try:
            self.__request(
                method="POST",
                url="{}issue/{}/transitions".format(self.base_url, issue_key),
                headers={"Content-type": "application/json"},
                data=json.dumps({
                    "transition": {
                        "id": self.closed_statuses[str(issue_key).split("-")[0]]
                    }
                })
            )
            return "Issue {} has been closed".format(issue_key)
        except KeyError:
            return "Issue {} cannot be closed".format(issue_key)

    def search(self, pattern):
        return self.__request(
            method="GET",
            url="{}{}".format(self.base_url, "search"),
            params={
                "jql": "(summary ~ \"{pattern}\" or description ~ \"{pattern}\") "
                       "and (status not in ({ignored_statuses})) "
                       "and (project in ({watched_projects})) "
                       "ORDER BY updated"
                       .format(
                           pattern=pattern,
                           ignored_statuses=self.ignored_statuses,
                           watched_projects=self.watched_projects
                       )
            },
        )
