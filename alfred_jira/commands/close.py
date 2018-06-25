from chuda import Command, Parameter


class CloseCommand(Command):
    command_name = "close"
    description = "close jira issue"

    arguments = [
        Parameter("issue_key")
    ]

    def main(self):
        result = self.app.jira.close(self.arguments.issue_key)
        self.logger.info(result)
