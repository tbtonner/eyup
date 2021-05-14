import current_bodger
from tokens import *
from nodes import *
from values import List
from errors import VexedError

#######################################
# PARSE RESULT
# result class that has a AST (as a node) or error -> wrap all things in result.register()
#######################################


class ParseResult:
    def __init__(self):
        self.error = None
        self.node = None
        self.last_registered_advance_count = 0
        self.advance_count = 0
        self.to_reverse_count = 0

    def register_advancement(self):
        self.advance_count += 1

    def register_reverse(self):
        self.advance_count -= 1

    def register(self, result):
        self.advance_count += result.advance_count
        if result.error:
            self.error = result.error
        return result.node

    def try_register(self, result):
        if result.error:
            self.to_reverse_count = result.advance_count
            return None
        return self.register(result)

    def success(self, node):
        self.node = node
        return self

    def failure(self, error):
        if not self.error or self.advance_count == 0:
            self.error = error
        return self

#######################################
# PARSER
# parses the token stream from the tokeniser into a AST
#######################################


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.token_index = -1
        self.advance()

    def advance(self, ):
        self.token_index += 1
        self.update_current_token()
        return self.current_token

    def reverse(self, amount=1):
        self.token_index -= amount
        self.update_current_token()
        return self.current_token

    def update_current_token(self):
        if self.token_index >= 0 and self.token_index < len(self.tokens):
            self.current_token = self.tokens[self.token_index]

    def parse(self):
        result = self.statements()
        if not result.error and self.current_token.type != TT_EOF:
            return result.failure(VexedError(
                self.current_token.pos_start, self.current_token.pos_end,
                "Wuz expectin' a valid statement"
            ))
        return result

    def optinal_newline(self, result):
        while self.current_token.type == TT_NEWLINE:
            result.register_advancement()
            self.advance()

    ###################################

    def statements(self, is_fettle=False):
        result = ParseResult()
        statements = []
        pos_start = self.current_token.pos_start.copy()

        # optional newlines
        self.optinal_newline(result)

        statement = result.register(self.statement(is_fettle))
        if result.error:
            return result
        statements.append(statement)

        more_statements = True
        while True:
            newline_count = 0
            while self.current_token.type == TT_NEWLINE:
                result.register_advancement()
                self.advance()
                newline_count += 1
            if newline_count == 0:
                more_statements = False

            if not more_statements:
                break
            statement = result.try_register(self.statement(is_fettle))
            if not statement:
                self.reverse(result.to_reverse_count)
                more_statements = False
                continue
            statements.append(statement)

        return result.success(ListNode(
            statements,
            pos_start,
            self.current_token.pos_end.copy()
        ))

    def statement(self, is_fettle):
        result = ParseResult()

        expression = result.register(self.expression(is_fettle, False))
        if result.error:
            return result.failure(VexedError(
                self.current_token.pos_start, self.current_token.pos_end,
                "Wuz expectin' a valid statement"
            ))
        return result.success(expression)

    def if_expression(self):
        result = ParseResult()
        cases = []
        else_case = None

        if not self.current_token.matches(TT_KEYWORD, 'if'):
            return result.failure(VexedError(
                self.current_token.pos_start, self.current_token.pos_end,
                f"Weerz 'if'?"
            ))

        result.register_advancement()
        self.advance()

        condition = result.register(self.expression())
        if result.error:
            return result

        # optional newlines
        self.optinal_newline(result)

        if not self.current_token.matches(TT_KEYWORD, 'then'):
            return result.failure(VexedError(
                self.current_token.pos_start, self.current_token.pos_end,
                f"Weerz 'then'?"
            ))

        result.register_advancement()
        self.advance()

        ################### MULTILINE #######################

        # optional newlines
        self.optinal_newline(result)

        exprs = result.register(self.statements())
        if result.error:
            return result
        cases.append((condition, exprs))

        # optional newlines
        self.optinal_newline(result)

        #####################################################

        while self.current_token.matches(TT_KEYWORD, 'when'):
            result.register_advancement()
            self.advance()

            # optional newlines
            self.optinal_newline(result)

            condition = result.register(self.expression())
            if result.error:
                return result

            # optional newlines
            self.optinal_newline(result)

            if not self.current_token.matches(TT_KEYWORD, 'then'):
                return result.failure(VexedError(
                    self.current_token.pos_start, self.current_token.pos_end,
                    f"Weerz 'then'?"
                ))

            result.register_advancement()
            self.advance()

            ################### MULTILINE #######################

            # optional newlines
            self.optinal_newline(result)

            exprs = result.register(self.statements())
            if result.error:
                return result
            cases.append((condition, exprs))

            #####################################################

        # optional newlines
        self.optinal_newline(result)

        if self.current_token.matches(TT_KEYWORD, 'else'):
            result.register_advancement()
            self.advance()

            ################### MULTILINE #######################

            # optional newlines
            self.optinal_newline(result)

            else_case = result.register(self.statements())
            if result.error:
                return result

            # optional newlines
            self.optinal_newline(result)

            #####################################################

        if not self.current_token.matches(TT_KEYWORD, 'oer'):
            return result.failure(VexedError(
                self.current_token.pos_start, self.current_token.pos_end,
                f"Weerz 'oer'?"
            ))

        result.register_advancement()
        self.advance()

        return result.success(IfNode(cases, else_case))

    def call(self):
        result = ParseResult()
        atom = result.register(self.atom())
        if result.error:
            return result

        if self.current_token.type == TT_LBRACK:
            result.register_advancement()
            self.advance()
            arg_nodes = []

            if self.current_token.type == TT_RBRACK:
                result.register_advancement()
                self.advance()
            else:
                arg_nodes.append(result.register(
                    self.expression(is_call=True)))
                if result.error:
                    return result.failure(VexedError(
                        self.current_token.pos_start, self.current_token.pos_end,
                        "Wuz expectin' a valid statement"
                    ))

                while self.current_token.type == TT_COMMA:
                    result.register_advancement()
                    self.advance()

                    arg_nodes.append(result.register(self.expression()))
                    if result.error:
                        return result

                if self.current_token.type != TT_RBRACK:
                    return result.failure(VexedError(
                        self.current_token.pos_start, self.current_token.pos_end,
                        f"Weerz ',' or ')'?"
                    ))

                result.register_advancement()
                self.advance()
            return result.success(CallNode(atom, arg_nodes))
        return result.success(atom)

    def atom(self):
        result = ParseResult()
        token = self.current_token

        if token.type in (TT_INT, TT_FLOAT):
            result.register_advancement()
            self.advance()
            return result.success(NumberNode(token))

        elif token.type in TT_SCRIPT:
            result.register_advancement()
            self.advance()
            return result.success(ScriptNode(token))

        elif token.type in TT_LETTER:
            result.register_advancement()
            self.advance()
            return result.success(LetterNode(token))

        elif token.type == TT_KEYWORD and (token.value == 'Number' or token.value == 'Script' or token.value == 'Letter' or token.value == 'Answer' or token.value == 'List' or token.value == 'Bodger'):
            result.register_advancement()
            self.advance()
            return result.success(NowtNode(token))

        elif token.type == TT_ANSWER:
            result.register_advancement()
            self.advance()
            return result.success(AnswerNode(token))

        elif token.type == TT_IDENTIFIER:
            result.register_advancement()
            self.advance()

            if self.current_token.type == TT_CALL:
                return self.bodger_call(result, token)

            if self.current_token.type == TT_LEFT_SQUARE_BRACK:
                return self.id_rbrack(result, token)

            return result.success(VarAccessNode(token))

        elif token.type == TT_LBRACK:
            result.register_advancement()
            self.advance()
            expression = result.register(self.expression())
            if result.error:
                return result
            if self.current_token.type == TT_RBRACK:
                result.register_advancement()
                self.advance()
                return result.success(expression)
            else:
                return result.failure(VexedError(
                    self.current_token.pos_start, self.current_token.pos_end,
                    "Weerz ')'?"
                ))
        elif token.type == TT_LEFT_SQUARE_BRACK:
            list_expression = result.register(self.list_expression())
            if result.error:
                return result
            return result.success(list_expression)

        elif token.matches(TT_KEYWORD, 'if'):
            if_expression = result.register(self.if_expression())
            if result.error:
                return result
            return result.success(if_expression)

        elif token.matches(TT_KEYWORD, 'while'):
            while_expression = result.register(self.while_expression())
            if result.error:
                return result
            return result.success(while_expression)

        elif token.matches(TT_KEYWORD, 'gowon'):
            gowon_expression = result.register(self.gowon_expression())
            if result.error:
                return result
            return result.success(gowon_expression)

        elif token.matches(TT_KEYWORD, 'fettle'):
            func_def = result.register(self.function_def())
            if result.error:
                return result
            return result.success(func_def)

        elif token.matches(TT_KEYWORD, 'gander'):
            gander_res = result.register(self.gander_res())
            if result.error:
                return result
            return result.success(gander_res)

        elif token.matches(TT_KEYWORD, 'wang'):
            wang_res = result.register(self.wang_res())
            if result.error:
                return result
            return result.success(wang_res)

        elif self.current_token.matches(TT_KEYWORD, 'sithee'):
            result.register_advancement()
            self.advance()
            return result.success(SitheeNode(self.current_token))

        elif self.current_token.matches(TT_KEYWORD, 'sithi'):
            result.register_advancement()
            self.advance()
            return result.success(SitheeNode(self.current_token))

        elif token.matches(TT_KEYWORD, 'allus'):
            allus_res = result.register(self.allus_res())
            if result.error:
                return result
            return result.success(allus_res)

        elif self.current_token.matches(TT_KEYWORD, 'missen'):
            token = self.current_token
            result.register_advancement()
            self.advance()

            return result.success(MissenNode(token))

        return result.failure(VexedError(
            token.pos_start, token.pos_end,
            "Wuz expectin' a valid statement"
        ))

    def list_expression(self):
        result = ParseResult()
        element_nodes = []
        pos_start = self.current_token.pos_start.copy()

        if self.current_token.type != TT_LEFT_SQUARE_BRACK:
            return result.failure(VexedError(
                self.current_token.pos_start, self.current_token.pos_end,
                f"Weerz '['?"
            ))

        result.register_advancement()
        self.advance()

        if self.current_token.type == TT_RIGHT_SQUARE_BRACK:
            result.register_advancement()
            self.advance()
        else:
            element_nodes.append(result.register(self.expression()))
            if result.error:
                return result.failure(VexedError(
                    self.current_token.pos_start, self.current_token.pos_end,
                    "Wuz expectin' a valid statement"
                ))

            while self.current_token.type == TT_COMMA:
                result.register_advancement()
                self.advance()

                element_nodes.append(result.register(self.expression()))
                if result.error:
                    return result

            if self.current_token.type != TT_RIGHT_SQUARE_BRACK:
                return result.failure(VexedError(
                    self.current_token.pos_start, self.current_token.pos_end,
                    f"Weerz ',' or ']'?"
                ))

            result.register_advancement()
            self.advance()

        return result.success(ListNode(
            element_nodes,
            pos_start,
            self.current_token.pos_end.copy()
        ))

    def factor(self):
        result = ParseResult()
        token = self.current_token

        if token.type in (TT_PLUS, TT_MINUS):
            result.register_advancement()
            self.advance()
            factor = result.register(self.factor())
            if result.error:
                return result
            return result.success(UnaryOpNode(token, factor))

        # return self.atom()
        return self.call()

    def term(self):  # two factors or expressios between *, / or %
        return self.binary_op(self.factor, (TT_MUL, TT_DIV, TT_MOD))

    def arithmetic_expression(self):
        return self.binary_op(self.term, (TT_PLUS, TT_MINUS, TT_CONCAT_APPEND, TT_CALL))

    def comparison_expression(self):
        result = ParseResult()

        if self.current_token.matches(TT_KEYWORD, 'not'):
            op_token = self.current_token
            result.register_advancement()
            self.advance()

            node = result.register(self.comparison_expression())
            if result.error:
                return result
            return result.success(UnaryOpNode(op_token, node))

        node = result.register(
            self.binary_op(
                self.arithmetic_expression, (
                    TT_EQUALS,
                    TT_NOT_EQUALS,
                    TT_LESS_THAN,
                    TT_GREATER_THAN,
                    TT_LESS_THAN_EQUALS,
                    TT_GREATER_THAN_EQUALS
                )
            )
        )

        if result.error:
            return result.failure(VexedError(
                self.current_token.pos_start, self.current_token.pos_end,
                "Wuz expectin' a valid statement"
            ))

        return result.success(node)

    def var_assign(self, result, init_var_name, is_summat, is_fettle=False):
        var_names = [init_var_name]  # start it as a list

        while self.current_token.type == TT_COMMA:
            result.register_advancement()
            self.advance()

            if self.current_token.type != TT_IDENTIFIER:
                return result.failure(VexedError(
                    self.current_token.pos_start, self.current_token.pos_end,
                    "Weerz t' identifier?"
                ))

            var_names.append(self.current_token)

            result.register_advancement()
            self.advance()

        if self.current_token.type != TT_VAR_COMPLETE and self.current_token.type != TT_VAR_DECLARE:
            return result.failure(VexedError(
                self.current_token.pos_start, self.current_token.pos_end,
                "Weerz ':=', or ':'?"
            ))

        assign_type = self.current_token.type

        result.register_advancement()
        self.advance()

        expression = result.register(self.expression())
        if result.error:
            return result

        if assign_type == TT_VAR_DECLARE:  # if declare type then has to be a Nowt: List, Number, Script, Letter or Answer
            if isinstance(expression, VarAccessNode):
                result.register_reverse()
                self.reverse()

                return result.failure(VexedError(
                    self.current_token.pos_start, self.current_token.pos_end,
                    f"Weerz a Number, List, Answer, Script or Letter?"
                ))
            if not expression.token.matches(TT_KEYWORD, 'Number') and expression.token.matches(TT_KEYWORD, 'List' and expression.token.matches(TT_KEYWORD, 'Script') and expression.token.matches(TT_KEYWORD, 'Letter') and expression.token.matches(TT_KEYWORD, 'Answer')):
                result.register_reverse()
                self.reverse()

                return result.failure(VexedError(
                    self.current_token.pos_start, self.current_token.pos_end,
                    f"Weerz a Number, List, Answer, Script or Letter?"
                ))

        var_names = List(var_names)

        if is_summat:
            return result.success(VarAssignNode(var_names, expression))
        return result.success(VarAssignOldNode(var_names, expression))

    def id_rbrack(self, result, var_name):
        result.register_advancement()
        self.advance()

        if not (self.current_token.type == TT_INT or self.current_token.type == TT_IDENTIFIER):
            return result.failure(VexedError(
                self.current_token.pos_start, self.current_token.pos_end,
                "Weerz proper Number?"
            ))

        index = result.register(self.expression())

        if not self.current_token.type == TT_RIGHT_SQUARE_BRACK:
            return result.failure(VexedError(
                self.current_token.pos_start, self.current_token.pos_end,
                "Weerz proper Number?"
            ))

        result.register_advancement()
        self.advance()

        if self.current_token.type == TT_VAR_COMPLETE:
            result.register_advancement()
            self.advance()

            expression = result.register(self.expression())
            if result.error:
                return result

            return result.success(PartScriptAssignNode(var_name, index, expression))

        return result.success(PartScriptNode(var_name, index))

    # entire expression of terms and factors (seperate expressions between brackets) + KEYWORDS

    def expression(self, is_fettle=False, is_call=False):
        result = ParseResult()

        if self.current_token.matches(TT_KEYWORD, 'eyup'):
            result.register_advancement()
            self.advance()

            if self.current_token.type != TT_IDENTIFIER:
                return result.failure(VexedError(
                    self.current_token.pos_start, self.current_token.pos_end,
                    "Weerz identifier?"
                ))

            bodger_to_change = self.current_token

            result.register_advancement()
            self.advance()

            return result.success(BodgerChangeNode(bodger_to_change))

        if self.current_token.matches(TT_KEYWORD, 'bodger'):
            result.register_advancement()
            self.advance()

            if self.current_token.type != TT_IDENTIFIER:
                return result.failure(VexedError(
                    self.current_token.pos_start, self.current_token.pos_end,
                    "Weerz identifier?"
                ))

            bodger_to_add = self.current_token

            result.register_advancement()
            self.advance()

            return result.success(AddBodgerNode(bodger_to_add))

        ######################

        if self.current_token.type == TT_IDENTIFIER:  # already assigned var check
            var_name = self.current_token
            result.register_advancement()
            self.advance()

            if self.current_token.type == TT_VAR_COMPLETE:
                return self.var_assign(result, var_name, False, is_fettle)

            if self.current_token.type == TT_COMMA and not is_call:
                return self.var_assign(result, var_name, False)

            result.register_reverse()
            self.reverse()

        if self.current_token.matches(TT_KEYWORD, 'forget'):
            result.register_advancement()
            self.advance()

            if self.current_token.type != TT_IDENTIFIER:
                return result.failure(VexedError(
                    self.current_token.pos_start, self.current_token.pos_end,
                    "Weerz identifier?"
                ))

            var_name = self.current_token
            result.register_advancement()
            self.advance()

            return result.success(VarForgetNode(var_name))

        if self.current_token.matches(TT_KEYWORD, 'summat'):
            result.register_advancement()
            self.advance()

            if self.current_token.type != TT_IDENTIFIER:
                return result.failure(VexedError(
                    self.current_token.pos_start, self.current_token.pos_end,
                    "Weerz identifier?"
                ))

            var_name = self.current_token
            result.register_advancement()
            self.advance()

            return self.var_assign(result, var_name, True)  # not overwrite

        # node = result.register(self.binary_op(self.term, (TT_PLUS, TT_MINUS)))
        node = result.register(self.binary_op(
            self.comparison_expression, ((TT_KEYWORD, 'and'), (TT_KEYWORD, 'or'))))

        if result.error:
            return result.failure(VexedError(
                self.current_token.pos_start, self.current_token.pos_end,
                "Wuz expectin' a valid statement"
            ))

        return result.success(node)

    def bodger_call(self, result, bodger_name):
        result.register_advancement()
        self.advance()

        atom = result.register(self.atom())
        if result.error:
            return result

        if self.current_token.type == TT_VAR_COMPLETE or self.current_token.type == TT_VAR_DECLARE:
            print("DFFDFD")
            return result.failure(VexedError(
                self.current_token.pos_start, self.current_token.pos_end,
                f"faffin' wi' {bodger_name}.{atom}"
            ))

        return result.success(BodgerCallNode(bodger_name, atom))

    def while_expression(self):
        result = ParseResult()

        if not self.current_token.matches(TT_KEYWORD, 'while'):
            return result.failure(VexedError(
                self.current_token.pos_start, self.current_token.pos_end,
                f"Weerz 'while'?"
            ))

        result.register_advancement()
        self.advance()

        condition = result.register(self.expression())
        if result.error:
            return result

        # optional newlines
        self.optinal_newline(result)

        if not self.current_token.matches(TT_KEYWORD, 'gowon'):
            return result.failure(VexedError(
                self.current_token.pos_start, self.current_token.pos_end,
                f"Weerz 'gowon'?"
            ))

        result.register_advancement()
        self.advance()

        ################### MULTILINE #######################

        # optional newlines
        self.optinal_newline(result)

        body = result.register(self.statements())
        if result.error:
            return result

        # optional newlines
        self.optinal_newline(result)

        #####################################################

        if not self.current_token.matches(TT_KEYWORD, 'oer'):
            return result.failure(VexedError(
                self.current_token.pos_start, self.current_token.pos_end,
                f"Weerz 'oer'?"
            ))

        result.register_advancement()
        self.advance()

        return result.success(WhileNode(condition, body))

    def gowon_expression(self):
        result = ParseResult()

        if not self.current_token.matches(TT_KEYWORD, 'gowon'):
            return result.failure(VexedError(
                self.current_token.pos_start, self.current_token.pos_end,
                f"Weerz 'gowon'?"
            ))

        result.register_advancement()
        self.advance()

        ################### MULTILINE #######################

        # optional newlines
        self.optinal_newline(result)

        body = result.register(self.statements())
        if result.error:
            return result

        # optional newlines
        self.optinal_newline(result)

        #####################################################

        if not self.current_token.matches(TT_KEYWORD, 'while'):
            return result.failure(VexedError(
                self.current_token.pos_start, self.current_token.pos_end,
                f"Weerz 'while'?"
            ))

        result.register_advancement()
        self.advance()

        # optional newlines
        self.optinal_newline(result)

        condition = result.register(self.expression())
        if result.error:
            return result

        # optional newlines
        self.optinal_newline(result)

        if not self.current_token.matches(TT_KEYWORD, 'oer'):
            return result.failure(VexedError(
                self.current_token.pos_start, self.current_token.pos_end,
                f"Weerz 'oer'?"
            ))

        result.register_advancement()
        self.advance()

        return result.success(GowonNode(body, condition))

    def gander_res(self):
        result = ParseResult()

        result.register_advancement()
        self.advance()

        if self.current_token.type == TT_EOF:
            token = Token(TT_IDENTIFIER, current_bodger.CURRENT_BODGER.name,
                          self.current_token.pos_start, self.current_token.pos_end)
            return result.success(GanderNode(token))

        if self.current_token.matches(TT_KEYWORD, "missen"):
            result.register_advancement()
            self.advance()
            token = Token(TT_IDENTIFIER, current_bodger.CURRENT_BODGER.name,
                          self.current_token.pos_start, self.current_token.pos_end)
            return result.success(GanderNode(token))

        if self.current_token.type != TT_IDENTIFIER:
            return result.failure(VexedError(
                self.current_token.pos_start, self.current_token.pos_end,
                f"Weerz idenfifier?"
            ))

        bodger_to_gander = self.current_token

        result.register_advancement()
        self.advance()

        return result.success(GanderNode(bodger_to_gander))

    def wang_res(self):
        result = ParseResult()

        result.register_advancement()
        self.advance()

        condition = result.register(self.expression())
        if result.error:
            return result

        return result.success(WangNode(condition))

    def allus_res(self):
        result = ParseResult()

        result.register_advancement()
        self.advance()

        value = result.register(self.expression())
        if result.error:
            return result

        return result.success(AllusNode(value))

    def function_def(self):
        result = ParseResult()

        if not self.current_token.matches(TT_KEYWORD, 'fettle'):
            return result.failure(VexedError(
                self.current_token.pos_start, self.current_token.pos_end,
                f"Weerz 'fettle'?"
            ))

        result.register_advancement()
        self.advance()

        if self.current_token.type != TT_IDENTIFIER:
            return result.failure(VexedError(
                self.current_token.pos_start, self.current_token.pos_end,
                f"Weerz idenfifier?"
            ))

        var_name_token = self.current_token
        result.register_advancement()
        self.advance()

        arg_dict = {}
        if self.current_token.type == TT_LBRACK:
            result.register_advancement()
            self.advance()

            if self.current_token.type == TT_IDENTIFIER:
                while True:  # while true break used so code is run at least once
                    init_token = self.current_token
                    result.register_advancement()
                    self.advance()

                    result.register(self.var_assign(result, init_token, True))
                    if result.error:
                        return result

                    for token in result.node.var_name_tokens.elements:
                        arg_dict[token] = result.node.value_node.token.value
                    if self.current_token.type == TT_COMMA:
                        result.register_advancement()
                        self.advance()
                    else:
                        break

            if self.current_token.type != TT_RBRACK:
                return result.failure(VexedError(
                    self.current_token.pos_start, self.current_token.pos_end,
                    f"Weerz identifier or ')'?"
                ))

            result.register_advancement()
            self.advance()

        static_type_return = None
        if self.current_token.type == TT_VAR_DECLARE:
            result.register_advancement()
            self.advance()
            
            if not (self.current_token.matches(TT_KEYWORD, 'Number') or self.current_token.matches(TT_KEYWORD, 'List') or self.current_token.matches(TT_KEYWORD, 'Answer') or self.current_token.matches(TT_KEYWORD, 'Script') or self.current_token.matches(TT_KEYWORD, 'Bodger') or self.current_token.matches(TT_KEYWORD, 'Letter')):
                result.register_reverse()
                self.reverse()

                return result.failure(VexedError(
                    self.current_token.pos_start, self.current_token.pos_end,
                    f"Weerz a Number, List, Answer, Script, Bodger or Letter?"
                ))

            static_type_return = self.current_token.value
            result.register_advancement()
            self.advance()

        if self.current_token.matches(TT_KEYWORD, 'gioer'):
            result.register_advancement()
            self.advance()
            return result.success(FuncDefNode(
                var_name_token,
                arg_dict,
                ListNode(NowtNode(Token("nowt", pos_start=self.current_token.pos_start)),
                         self.current_token.pos_start, self.current_token.pos_end),
                static_type_return
            ))

        if not self.current_token.matches(TT_KEYWORD, 'giz'):
            return result.failure(VexedError(
                self.current_token.pos_start, self.current_token.pos_end,
                f"Weerz giz?"
            ))

        result.register_advancement()
        self.advance()

        ################## MULTILINE #######################
        # optional newlines
        self.optinal_newline(result)

        nodes_to_execute = result.register(self.statements(True))

        if result.error:
            return result

        # optional newlines
        self.optinal_newline(result)
        #####################################################

        if not self.current_token.matches(TT_KEYWORD, 'oer'):
            return result.failure(VexedError(
                self.current_token.pos_start, self.current_token.pos_end,
                f"Weerz 'oer'?"
            ))
        result.register_advancement()
        self.advance()

        final_node = FuncDefNode(
            var_name_token,
            arg_dict,
            nodes_to_execute,
            static_type_return
        )

        return result.success(final_node)

    #####################################################

    def binary_op(self, function_a, ops, function_b=None):
        if function_b == None:
            function_b = function_a

        result = ParseResult()
        left = result.register(function_a())
        if result.error:
            return result

        while self.current_token.type in ops or (self.current_token.type, self.current_token.value) in ops:
            op_token = self.current_token
            result.register_advancement()
            self.advance()
            right = result.register(function_b())
            if result.error:
                return result
            left = BinaryOpNode(left, op_token, right)

        return result.success(left)
