from chuda import Command, Parameter
from passepartout import WorkflowItem


class SearchCommand(Command):
    command_name = "search"
    description = "search jira issues"

    arguments = [
        Parameter("pattern", nargs="?")
    ]

    def main(self):
        if self.arguments.pattern:
            for issue in self.app.jira.search(self.arguments.pattern)["issues"]:
                self.app.workflow.add_item(
                    WorkflowItem(
                        title=issue["fields"]["summary"],
                        subtitle=issue["key"],
                        arg=issue["key"]
                    )
                )
        else:
            self.app.workflow.add_item(WorkflowItem(
                title="Open dashboard",
                subtitle="",
                arg=""
            ))
        self.logger.info(self.app.workflow.to_json())
