from norminette.rules import Rule


class CheckFunctionsCount(Rule):
    def __init__(self):
        super().__init__()
        self.depends_on = ["IsFuncDeclaration"]

    def run(self, context):
        """
        Each file cannot contain more than 15 functions
        """
        if context.scope is not None and context.scope.name == "GlobalScope":
            if context.scope.functions > 15:
                context.new_error("TOO_MANY_FUNCS", context.peek_token(0))
        return False, 0
