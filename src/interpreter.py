import bodgers
import values
import errors
import tokens
import nodes
import time
import sys
from func_timeout import func_timeout, FunctionTimedOut

#######################################
# RUNTIME RESULT
# result class that has a value or error -> wrap all things in result.register()
#######################################


class RTResult:
    def __init__(self):
        self.value = None
        self.error = None

    def register(self, res):
        if res.error:
            self.error = res.error
        return res.value

    def success(self, value):
        self.value = value
        return self

    def failure(self, error):
        self.error = error
        return self

#######################################
# INTERPRETER
# interprets the node AST from the parser and returns the values of the tree or the error message
# visit methods which visit various nodes from the AST
#######################################


class Interpreter:

    ################################### non-visit ###################################

    def replace_str_index(self, text, index=0, replacement=''):
        return '%s%s%s' % (text[:index], replacement, text[index+1:])

    def eyupise_value(self, value):  # normalise types from python types into EYUP types
        _type = type(value).__name__
        if _type == 'int':
            return 'Number'
        if _type == 'float':
            return 'Number'
        if _type == 'complex':
            return 'Number'
        if _type == 'bool':
            return 'Answer'
        if _type == 'str':
            return 'Script'
        if _type == 'BodgerVal':
            return 'Bodger'
        return _type

    ################################### main visit ###################################

    def visit(self, node, context):
        method_name = f'visit_{type(node).__name__}'
        method = getattr(self, method_name, self.no_visit_method)
        return method(node, context)

    def no_visit_method(self, node, context):
        raise Exception(f'No visit_{type(node).__name__} method defined')

    ################################### basic atom visits ###################################

    def visit_NowtNode(self, node, context):
        return RTResult().success(
            values.Nowt(node.token.value).set_context(
                context).set_pos(node.pos_start, node.pos_end)
        )

    def visit_NumberNode(self, node, context):
        return RTResult().success(
            values.Number(node.token.value).set_context(
                context).set_pos(node.pos_start, node.pos_end)
        )

    def visit_AnswerNode(self, node, context):
        return RTResult().success(
            values.Answer(node.token.value).set_context(
                context).set_pos(node.pos_start, node.pos_end)
        )

    def visit_ScriptNode(self, node, context):
        return RTResult().success(
            values.Script(node.token.value).set_context(
                context).set_pos(node.pos_start, node.pos_end)
        )

    def visit_LetterNode(self, node, context):
        return RTResult().success(
            values.Letter(node.token.value).set_context(
                context).set_pos(node.pos_start, node.pos_end)
        )

    def visit_ListNode(self, node, context):
        result = RTResult()
        elements = []

        for element_node in node.element_nodes:
            elements.append(result.register(self.visit(element_node, context)))
            if result.error:
                return result

        return result.success(
            values.List(elements).set_context(
                context).set_pos(node.pos_start, node.pos_end)
        )

    def visit_AllusNode(self, node, context):
        result = RTResult()
        value = result.register(self.visit(node.token, context))
        return result.success(nodes.AllusNode(value))

    ################################### single visits ###################################

    def visit_SitheeNode(self, node, context):
        parent_bodger = bodgers.CURRENT_BODGER.parent
        if parent_bodger is None:
            print("Leavin' Yorkshire v1.0 (flippin 'eck!)")
            time.sleep(1)
            sys.exit(0)

        bodgers.CURRENT_BODGER = parent_bodger
        return RTResult().success(None)

    def visit_MissenNode(self, node, context):
        return RTResult().success(values.BodgerVal(bodgers.CURRENT_BODGER))

    def visit_GanderNode(self, node, context):
        result = RTResult()
        name = node.bodger_identifer

        exisiting_bodger = self.visit_VarAccessNode(
            nodes.VarAccessNode(name), context).value
        if exisiting_bodger is None:
            return result.failure(errors.FlummoxedError(
                node.pos_start, node.pos_end,
                f"{name} ain't no bodger I've 'erd of",
                context
            ))
        exisiting_bodger = exisiting_bodger.bodger

        allus = False
        for symbol in exisiting_bodger.context.symbol_table.symbols:
            if symbol not in bodgers.global_symbol_table.symbols:
                value = exisiting_bodger.context.symbol_table.get(symbol)
                if isinstance(value, nodes.AllusNode):
                    value = value.token
                    allus = True
                else:
                    allus = False

                if isinstance(value, values.Function) or isinstance(value, values.BaseFunction):
                    if allus : print(str(name.value) + "." + symbol + "() *")
                    else: print(str(name.value) + "." + symbol + "()")
                else:
                    if allus : print(str(name.value) + "." + symbol + " *")
                    else: print(str(name.value) + "." + symbol)

        return result.success(None)

    def visit_WangNode(self, node, context):
        result = RTResult()

        value = result.register(self.visit(node.condition, context))
        if not isinstance(value, values.Answer):
            return result.failure(errors.FlummoxedError(
                node.pos_start, node.pos_end,
                f"Need somthing to wang",
                context
            ))

        if value.value == "aye":
            return result.failure(errors.FlummoxedError(
                node.pos_start, node.pos_end,
                f"Wangged is aye",
                context
            ))

        return result.success(None)

    ################################### operation visits ###################################

    def visit_UnaryOpNode(self, node, context):
        result = RTResult()
        number = result.register(self.visit(node.node, context))
        if result.error:
            return result

        if node.op_token.type == tokens.TT_MINUS:
            if not isinstance(number, values.Number):
                return result.failure(errors.FlummoxedError(
                    node.pos_start, node.pos_end,
                    f"{number} ain't a number",
                    context
                ))
            number, error = number.multiplied_by(values.Number(-1))

            if error: return result.failure(error)
            return result.success(number.set_pos(node.pos_start, node.pos_end))

        answer = number
        if not isinstance(answer, values.Answer):
            return result.failure(errors.FlummoxedError(
                node.pos_start, node.pos_end,
                f"{answer} ain't a answer",
                context
            ))

        answer, error = answer.notted()

        if error: return result.failure(error)
        return result.success(answer.set_pos(node.pos_start, node.pos_end))

    def visit_BinaryOpNode(self, node, context):
        res = RTResult()
        left = res.register(self.visit(node.left_node, context))
        if res.error:
            return res

        if node.op_token.type == tokens.TT_CALL:
            if not isinstance(left, values.BodgerVal):
                return res.failure(errors.FlummoxedError(
                    node.pos_start, node.pos_end,
                    f"{node.left_node.var_name_token.value} ain't a bodger",
                    context
                ))
            right = res.register(self.visit(
                node.right_node, left.bodger.context))
            result, error = left.call_by(right)
        else:
            right = res.register(self.visit(node.right_node, context))

        if res.error:
            return res

        if type(left) == values.Nowt or type(right) == values.Nowt:
            return res.failure(errors.FlummoxedError(
                node.pos_start, node.pos_end,
                f"Can't do stuff wi {left} or {right} being nowt",
                context
            ))

        # assign positions to node positions if not already set correctly
        left.pos_start = node.left_node.pos_start
        left.pos_end = node.left_node.pos_end
        right.pos_start = node.right_node.pos_start
        right.pos_end = node.right_node.pos_end

        if node.op_token.type == tokens.TT_PLUS:
            result, error = left.added_to(right)
        elif node.op_token.type == tokens.TT_MINUS:
            result, error = left.subtracted_by(right)
        elif node.op_token.type == tokens.TT_MUL:
            result, error = left.multiplied_by(right)
        elif node.op_token.type == tokens.TT_DIV:
            result, error = left.divided_by(right)
        elif node.op_token.type == tokens.TT_MOD:
            result, error = left.modded_by(right)
        elif node.op_token.type == tokens.TT_CONCAT_APPEND:
            result, error = left.concated_by(right)
        elif node.op_token.type == tokens.TT_EQUALS:
            result, error = left.get_comparison_equals(right)
        elif node.op_token.type == tokens.TT_NOT_EQUALS:
            result, error = left.get_comparison_not_equals(right)
        elif node.op_token.type == tokens.TT_LESS_THAN:
            result, error = left.get_comparison_less_than(right)
        elif node.op_token.type == tokens.TT_GREATER_THAN:
            result, error = left.get_comparison_greater_than(right)
        elif node.op_token.type == tokens.TT_LESS_THAN_EQUALS:
            result, error = left.get_comparison_less_than_equals(right)
        elif node.op_token.type == tokens.TT_GREATER_THAN_EQUALS:
            result, error = left.get_comparison_greater_than_equals(right)
        elif node.op_token.matches(tokens.TT_KEYWORD, 'and'):
            result, error = left.anded_by(right)
        elif node.op_token.matches(tokens.TT_KEYWORD, 'or'):
            result, error = left.ored_by(right)

        if error:
            return res.failure(error)
        else:
            return res.success(result.set_pos(node.pos_start, node.pos_end))

    ################################### assign/access visits ###################################

    def visit_VarAccessNode(self, node, context):
        result = RTResult()
        var_name = node.var_name_token.value
        value = context.symbol_table.get(var_name)

        if isinstance(value, nodes.AllusNode):
            value = value.token

         # if it's a function with no args
        if isinstance(value, values.Function):
            if len(value.arg_dict) == 0:
                return_value = result.register(value.execute({}))
                if result.error:
                    return result

                return_value = return_value.copy().set_pos(
                    node.pos_start, node.pos_end).set_context(context)
                return result.success(return_value)

        if not value:
            return result.failure(errors.FlummoxedError(
                node.pos_start, node.pos_end,
                f"weerz {var_name}?",
                context
            ))

        value = value.copy().set_pos(node.pos_start, node.pos_end).set_context(context)
        return result.success(value)

    def visit_VarAssignNode(self, node, context):
        result = RTResult()
        var_name_tokens = node.var_name_tokens.elements

        value = values.Nowt
        # if bodger chnge node
        if isinstance(node.value_node, nodes.BodgerChangeNode):
            exisiting_bodger_name = node.value_node.bodger_name

            exisiting_bodger = self.visit_VarAccessNode(
                nodes.VarAccessNode(exisiting_bodger_name), context).value
            if exisiting_bodger is None:
                return result.failure(errors.FlummoxedError(
                    node.pos_start, node.pos_end,
                    f"{node.value_node.bodger_name} ain't a bodger",
                    context
                ))

            exisiting_bodger = exisiting_bodger.bodger
            new_symbol_table = exisiting_bodger.context.symbol_table.copySymbols()

            for var_name_token in var_name_tokens:
                print(f'{bodgers.CURRENT_BODGER.name}.{var_name_token.value}')

                new_context = bodgers.Context(var_name_token.value)
                for name, value in new_symbol_table.items():
                    if not isinstance(value, nodes.AllusNode):
                        value.set_context(new_context)
                new_context.symbol_table = bodgers.SymbolTable(
                    new_symbol_table)
                new_bodger = bodgers.Bodger(
                    var_name_token.value, new_context, bodgers.CURRENT_BODGER)

                context.symbol_table.set(
                    var_name_token.value, values.BodgerVal(new_bodger))

            return result.success(None)

        # else
        value = result.register(self.visit(node.value_node, context))
        if result.error:
                return result

        for var_name_token in var_name_tokens:
            if context.symbol_table.get(var_name_token.value) is not None:
                result.register(self.visit_VarForgetNode(
                    nodes.VarForgetNode(var_name_token), context))
                if result.error:
                    return result

            print(f'{bodgers.CURRENT_BODGER.name}.{var_name_token.value}')

            context.symbol_table.set(var_name_token.value, value)

        return result.success(value)

    def visit_VarAssignOldNode(self, node, context):
        result = RTResult()
        var_name_tokens = node.var_name_tokens.elements

        # if bodger change node
        if isinstance(node.value_node, nodes.BodgerChangeNode):
            exisiting_bodger_name = node.value_node.bodger_name

            exisiting_bodger = self.visit_VarAccessNode(
                nodes.VarAccessNode(exisiting_bodger_name), context).value
            if exisiting_bodger is None:
                return result.failure(errors.FlummoxedError(
                    node.pos_start, node.pos_end,
                    f"{node.value_node.bodger_name} ain't a bodger",
                    context
                ))

            exisiting_bodger = exisiting_bodger.bodger
            existing_symbol_table = exisiting_bodger.context.symbol_table.copySymbols()

            for var_name_token in var_name_tokens:
                new_context = bodgers.Context(var_name_token.value)
                new_context.symbol_table = bodgers.SymbolTable(
                    existing_symbol_table)
                new_bodger = bodgers.Bodger(
                    var_name_token.value, new_context, bodgers.CURRENT_BODGER)

                context.symbol_table.set(
                    var_name_token.value, values.BodgerVal(new_bodger))

            return result.success(values.BodgerVal(new_bodger))

        # else
        value = result.register(self.visit(node.value_node, context))
        new_type = self.eyupise_value(value)

        for var_name_token in var_name_tokens:
            if isinstance(var_name_token, int):
                return

            if context.symbol_table.get(var_name_token.value) is None:
                return result.failure(errors.FlummoxedError(
                    var_name_token.pos_start, var_name_token.pos_end,
                    f"'{var_name_token.value}' ain't bin made y't",
                    context
                ))

            old_value = context.symbol_table.get(var_name_token.value)
            if isinstance(old_value, values.Nowt):
                old_type = old_value.value
                if old_type == "Nowt":
                    old_type = new_type
            else:
                if isinstance(old_value, nodes.AllusNode):
                    return result.failure(errors.FlummoxedError(
                        var_name_token.pos_start, var_name_token.pos_end,
                        f"{var_name_token.value} must allus be same",
                        context
                    ))
                old_type = self.eyupise_value(old_value)

            if isinstance(old_value, values.Function):  # if declaring in the function
                if old_value.static_type_return is not None:
                    if new_type != old_value.static_type_return:
                        return result.failure(errors.VexedError(
                            var_name_token.pos_start, var_name_token.pos_end,
                            f"{var_name_token} wi' bad'un '{node.value_node}:{new_type}'"
                        ))

                old_value.setValue(value)
                return result.success(None)

            if new_type != old_type:
                return result.failure(errors.VexedError(
                    var_name_token.pos_start, var_name_token.pos_end,
                    f"{var_name_token} wi' bad'un '{node.value_node}':{new_type}"
                ))
            else:
                context.symbol_table.set(var_name_token.value, value)
        return result.success(value)

    def visit_PartScriptAssignNode(self, node, context):
        # get initial parts of the node
        script_token = node.script_token
        index_node = node.index_node
        letter_value_node = node.letter_value_node

        # script validation
        if not isinstance(script_token, tokens.Token):
            return RTResult().failure(errors.FlummoxedError(
                node.pos_start, node.pos_end,
                f"{script_token}'s type is a bad'un",
                context
            ))
        str_script = context.symbol_table.get(script_token.value)
        if str_script == "None":
            return RTResult().failure(errors.FlummoxedError(
                node.pos_start, node.pos_end,
                f"'{script_token.value}' is a bad'un",
                context
            ))

        # index validation
        if isinstance(index_node, nodes.BinaryOpNode):
            index = self.visit_BinaryOpNode(index_node, context).value.value
        elif isinstance(index_node, nodes.VarAccessNode):
            index = self.visit_VarAccessNode(index_node, context).value.value

        if isinstance(index_node, nodes.NumberNode):
            index = index_node.token.value
        elif not isinstance(index, int):
            return RTResult().failure(errors.FlummoxedError(
                node.pos_start, node.pos_end,
                f"{index_node}'s type is a bad'un",
                context
            ))

        if isinstance(str_script, values.Script):
            str_script = str(str_script)
            if index < 0 or index >= len(str_script):
                return RTResult().failure(errors.FlummoxedError(
                    node.pos_start, node.pos_end,
                    f"'{index}' tis out'v range of {str_script}",
                    context
                ))

            # letter validation
            letter = None
            if isinstance(letter_value_node, nodes.VarAccessNode):
                letter = self.visit_VarAccessNode(
                    letter_value_node, context).value.value

            if isinstance(letter_value_node, nodes.LetterNode):
                letter = str(letter_value_node.token.value)

            if isinstance(letter, str):
                if len(letter) != 1:
                    return RTResult().failure(errors.FlummoxedError(
                        node.pos_start, node.pos_end,
                        f"'{letter}' ain't no letter",
                        context
                    ))
            else:
                return RTResult().failure(errors.FlummoxedError(
                    node.pos_start, node.pos_end,
                    f"{letter_value_node}'s type is a bad'un",
                    context
                ))

            # set new script
            str_script = self.replace_str_index(str_script, index, letter)
            script = values.Script(str_script)

            context.symbol_table.set(script_token.value, script)
            return RTResult().success(script)
        elif isinstance(str_script, values.List):
            list_to_change = str_script.elements
            if index < 0 or index >= len(list_to_change):
                return RTResult().failure(errors.FlummoxedError(
                    node.pos_start, node.pos_end,
                    f"'{index}' tis out'v range of {list_to_change}",
                    context
                ))

            change_node = letter_value_node

            change = None
            if isinstance(change_node, nodes.VarAccessNode):
                change = self.visit_VarAccessNode(
                    change_node, context).value.value
            else:
                change = change_node.token.value

            list_to_change[index] = change
            return RTResult().success(list_to_change)

        return RTResult().failure(errors.FlummoxedError(
            node.pos_start, node.pos_end,
            f"By heck, right unknown error this",
            context
        ))

    def visit_PartScriptNode(self, node, context):
        var_name = node.var_name.value
        index = node.index_token.token.value
        value = context.symbol_table.get(var_name)

        if not isinstance(index, int):
            if isinstance(index, str):
                index = context.symbol_table.get(index)
                if not isinstance(index, values.Number):
                    return RTResult().failure(errors.FlummoxedError(
                        node.pos_start, node.pos_end,
                        f"{node.index_token.token.value} ain't a number",
                        context
                    ))
                index = index.value
            else:
                return RTResult().failure(errors.FlummoxedError(
                    node.pos_start, node.pos_end,
                    f"{node.index_token.token.value} ain't a proper number",
                    context
                ))

        if not isinstance(value, values.Script) and isinstance(value, values.Letter):
            return RTResult().failure(errors.FlummoxedError(
                node.pos_start, node.pos_end,
                f"'{var_name}' is a bad'un",
                context
            ))

        # LIST
        if isinstance(value, values.List):
            list_value = value.elements

            if index >= len(list_value) or index < 0:
                return RTResult().failure(errors.FlummoxedError(
                    node.pos_start, node.pos_end,
                    f"'{index}' tis out'v range of {list_value}",
                    context
                ))

            list_value = list_value[index]
            return RTResult().success(list_value)

        # SCRIPT
        if not isinstance(value, values.Script):
            return RTResult().failure(errors.FlummoxedError(
                node.pos_start, node.pos_end,
                f"'{value}' is a bad'un, should be script",
                context
            ))

        value = value.value

        if index >= len(value) or index < 0:
            return RTResult().failure(errors.FlummoxedError(
                node.pos_start, node.pos_end,
                f"'{index}' tis out'v range of {value}",
                context
            ))

        value = value[index]

        return RTResult().success(
            values.Letter(value).set_context(
                context).set_pos(node.pos_start, node.pos_end)
        )

    def visit_VarForgetNode(self, node, context):
        result = RTResult()

        if isinstance(node.var_name_token, nodes.AllusNode):
            return result.failure(errors.FlummoxedError(
                node.pos_start, node.pos_end,
                f"{node.var_name_token.value} must allus be same",
                context
            ))

        var_name = node.var_name_token.value

        value = context.symbol_table.get(var_name)
        if value is None:
            return result.failure(errors.FlummoxedError(
                node.pos_start, node.pos_end,
                f"Can't forget summat already forgotten",
                context
            ))

        if isinstance(value, nodes.AllusNode):
            return result.failure(errors.FlummoxedError(
                node.pos_start, node.pos_end,
                f"{node.var_name_token.value} must allus be same",
                context
            ))

        context.symbol_table.remove(var_name)
        return result.success(None)

    ################################### bodger visits ###################################

    def visit_BodgerCallNode(self, node, context):
        result = RTResult()

        bodger_name = node.bodger_name
        expression = node.expression

        if isinstance(expression, nodes.VarAssignOldNode):
            string = ""
            for elem in expression.var_name_tokens.elements:
                string += f'{bodger_name.value}.{elem.value} '
            return result.failure(errors.FlummoxedError(
                node.pos_start, node.pos_end,
                f"faffin' wi {string}",
                context
            ))

        bodger = self.visit_VarAccessNode(
            nodes.VarAccessNode(bodger_name), context).value
        if bodger is None:
            return result.failure(errors.FlummoxedError(
                node.pos_start, node.pos_end,
                f"'{bodger_name.value}' ain't no bodger I've 'erd of",
                context
            ))

        res = bodger.bodger.partRun(expression)
        if res.error:
            return res

        return result.success(res.value)

    def visit_BodgerChangeNode(self, node, context):
        result = RTResult()

        bodger_name = node.bodger_name
        bodger = self.visit_VarAccessNode(
            nodes.VarAccessNode(bodger_name), context).value
        if bodger is None:
            return result.failure(errors.FlummoxedError(
                node.pos_start, node.pos_end,
                f"{bodger_name.value}' is a bad'un",
                context
            ))

        bodgers.CURRENT_BODGER = bodger.bodger

        return result.success(None)

    def visit_AddBodgerNode(self, node, context):
        result = RTResult()
        bodger_name = node.bodger_name
        exisiting_var = self.visit_VarAccessNode(
            nodes.VarAccessNode(bodger_name), context).value
        if exisiting_var is not None:
            return result.failure(errors.FlummoxedError(
                node.pos_start, node.pos_end,
                f"{bodger_name} is a bad'un",
                context
            ))
        bodger_name = str(bodger_name.value)

        _current_bodger = bodgers.CURRENT_BODGER
        current_symbol_table = _current_bodger.context.symbol_table.copySymbols()

        new_context = bodgers.Context(bodger_name)
        new_context.symbol_table = bodgers.SymbolTable(current_symbol_table)
        new_bodger = bodgers.Bodger(bodger_name, new_context, _current_bodger)

        new_bodger.context.symbol_table.set(bodger_name, values.BodgerVal(new_bodger)) # so it knows itself

        print(f'{bodgers.CURRENT_BODGER.name}.{new_bodger.name}')
        context.symbol_table.set(bodger_name, values.BodgerVal(new_bodger))

        return result.success(None)

    ################################### if visits ###################################

    def visit_IfNode(self, node, context):
        result = RTResult()

        for condition, expression in node.cases:
            condition_value = result.register(self.visit(condition, context))
            if result.error:
                return result

            if condition_value.is_true():
                result.register(self.visit(expression, context))
                if result.error:
                    return result
                return result.success(None)

        if node.else_case:
            result.register(self.visit(node.else_case, context))
            if result.error:
                return result
            return result.success(None)

        return result.success(None)

    ################################### loop visits ###################################

    def while_loop(self, res, node, context):
        while True:
            condition = res.register(self.visit(node.condition_node, context))
            if res.error:
                return res
            if condition.is_true():
                break

            res.register(self.visit(node.body_node, context))
            if res.error:
                return res
        return res

    def gowon_loop(self, res, node, context):
        while True:
            res.register(self.visit(node.body_node, context))
            if res.error:
                return res

            condition = res.register(self.visit(node.condition_node, context))
            if res.error:
                return res
            if condition.is_true():
                break
        return res

    def visit_WhileNode(self, node, context):
        res = RTResult()

        try:
            res = func_timeout(5, self.while_loop, args=(res, node, context))
        except FunctionTimedOut:
            print(f"Flippin 'eck weerz tha bin?")
            return res.failure(errors.FlummoxedError(
                node.pos_start, node.pos_end,
                f"I'm flaggin' me! Took too long t' compute that did",
                context
            ))

        return res.success(None)

    def visit_GowonNode(self, node, context):
        res = RTResult()

        try:
            res = func_timeout(5, self.gowon_loop, args=(res, node, context))
        except FunctionTimedOut:
            print(f"Flippin 'eck weerz tha bin?")
            return res.failure(errors.FlummoxedError(
                node.pos_start, node.pos_end,
                f"I'm flaggin' me! Took too long t' compute that did",
                context
            ))

        return res.success(None)

    ################################### fettle visits ###################################

    def visit_FuncDefNode(self, node, context):
        result = RTResult()

        func_name = node.var_name_token.value if node.var_name_token else None
        func_value = values.Function(
            func_name,
            node.body_nodes,
            node.arg_dict,
            node.static_type_return
        ).set_context(context).set_pos(node.pos_start, node.pos_end)

        if context.symbol_table.get(node.var_name_token.value) is not None:
            result.register(self.visit_VarForgetNode(
                nodes.VarForgetNode(node.var_name_token), context))
            if result.error:
                return result

        if node.var_name_token:
            context.symbol_table.set(func_name, func_value)

        return result.success(func_value)

    def visit_CallNode(self, node, context):
        result = RTResult()
        args = []

        func_to_call = result.register(self.visit(node.node_to_call, context))
        if result.error:
            return result
        func_to_call = func_to_call.copy().set_pos(node.pos_start, node.pos_end)

        for arg_node in node.arg_nodes:
            args.append(result.register(self.visit(arg_node, context)))
            if result.error:
                return result

        return_value = result.register(func_to_call.execute(args))
        if result.error:
            return result
        return_value = return_value.copy().set_pos(
            node.pos_start, node.pos_end).set_context(context)
        return result.success(return_value)
