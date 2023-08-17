from norminette.rules import Rule

allowed_on_comment = ["COMMENT", "MULT_COMMENT", "SPACE", "TAB"]


class CheckComment(Rule):
    def __init__(self):
        super().__init__()
        self.depends_on = []

    def run(self, context):
        """
        Comments are only allowed in GlobalScope.
        """
        is_start_of_line = context.peek_token(0).pos[1] == 0
        i = context.skip_ws(0)

        has_code = is_start_of_line
        has_comment = False
        while (
            context.peek_token(i) is not None
            and context.check_token(i, "NEWLINE") is False
        ):
            if not context.check_token(i, ["COMMENT", "MULT_COMMENT"]):
                has_code = True

            if context.check_token(i, allowed_on_comment) is False:
                if has_comment is True:
                    context.new_error("COMMENT_ON_INSTR", context.peek_token(i))
                    return True, i
            elif context.check_token(i, ["COMMENT", "MULT_COMMENT"]) is True:
                # if (
                #     context.scope.name != "GlobalScope"
                #     or context.history[-1] == "IsFuncDeclaration"
                # ):
                #     context.new_error("WRONG_SCOPE_COMMENT", context.peek_token(i))
                if has_code:
                    context.new_error("COMMENT_ON_INSTR", context.peek_token(i))
                has_comment = True
            i += 1
        i = context.skip_ws(0)
        return False, 0
