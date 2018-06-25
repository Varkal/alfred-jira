from chuda import Command, Parameter
from passepartout import WorkflowItem


class UrlCommand(Command):
    command_name = "url"
    description = "preprend url to issue"

    arguments = [
        Parameter("issue_key", nargs="?")
    ]

    def main(self):
        if self.arguments.issue_key:
            self.logger.info("https://happnapp.atlassian.net/browse/{}".format(str(self.arguments.issue_key).rstrip()))
        else:
            self.logger.info("https://happnapp.atlassian.net/")
