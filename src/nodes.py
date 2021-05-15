import values

#######################################
# NODES
# all the various node classes
#######################################

################################### basic atom nodes ###################################

class NowtNode:
    def __init__(self, token):
        self.token = token

        self.pos_start = self.token.pos_start
        self.pos_end = self.token.pos_end

    def __repr__(self):
        return f'{self.token.value}'


class AllusNode:
    def __init__(self, token):
        self.token = token

        self.pos_start = self.token.pos_start
        self.pos_end = self.token.pos_end

    def __repr__(self):
        return f'{self.token.value}'


class ListNode:
    def __init__(self, element_nodes, pos_start, pos_end):
        self.element_nodes = element_nodes

        self.pos_start = pos_start
        self.pos_end = pos_end

    def repr_list(self, _list):
        if isinstance(_list, values.List): _list = _list.elements
        string = ""
        for element in _list:
            string += str(element) + ", "
        mod_string = string[:-2]
        return mod_string

    def __repr__(self):
        return f'{self.repr_list(self.element_nodes)}'


class ScriptNode:
    def __init__(self, token):
        self.token = token

        self.pos_start = self.token.pos_start
        self.pos_end = self.token.pos_end

    def __repr__(self):
        return f'{self.token.value}'


class LetterNode:
    def __init__(self, token):
        self.token = token

        self.pos_start = self.token.pos_start
        self.pos_end = self.token.pos_end

    def __repr__(self):
        return f'{self.token.value}'


class NumberNode:
    def __init__(self, token):
        self.token = token

        self.pos_start = self.token.pos_start
        self.pos_end = self.token.pos_end

    def __repr__(self):
        return f'{self.token.value}'


class AnswerNode:
    def __init__(self, token):
        self.token = token

        self.pos_start = self.token.pos_start
        self.pos_end = self.token.pos_end

    def __repr__(self):
        return f'{self.token.value}'


################################### single nodes ###################################

class GanderNode:
    def __init__(self, bodger_identifer):
        self.bodger_identifer = bodger_identifer

        self.pos_start = self.bodger_identifer.pos_start
        self.pos_end = self.bodger_identifer.pos_end

    def __repr__(self):
        return f'{self.bodger_identifer}'


class WangNode:
    def __init__(self, condition):
        self.condition = condition

        self.pos_start = self.condition.pos_start
        self.pos_end = self.condition.pos_end

    def __repr__(self):
        return f'{self.condition}'


class SitheeNode:
    def __init__(self, sithee_token):
        self.sithee_token = sithee_token
        self.pos_start = sithee_token.pos_start
        self.pos_end = sithee_token.pos_end

    def __repr__(self):
        return f'{self.sithee_token}'


class MissenNode:
    def __init__(self, missen_token):
        self.missen_token = missen_token
        self.pos_start = missen_token.pos_start
        self.pos_end = missen_token.pos_end

    def __repr__(self):
        return f'{self.missen_token}'

################################### operation nodes ###################################

class BinaryOpNode:
    def __init__(self, left_node, op_token, right_node):
        self.left_node = left_node
        self.op_token = op_token
        self.right_node = right_node

        self.pos_start = self.left_node.pos_start
        self.pos_end = self.right_node.pos_end

    def __repr__(self):
        return f'{self.left_node} {self.op_token} {self.right_node}'


class UnaryOpNode:
    def __init__(self, op_token, node):
        self.op_token = op_token
        self.node = node

        self.pos_start = self.op_token.pos_start
        self.pos_end = node.pos_end

    def __repr__(self):
        return f'{self.op_token}, {self.node}'

################################### assign/access nodes ###################################

class VarAccessNode:
    def __init__(self, var_name_token):
        self.var_name_token = var_name_token

        self.pos_start = self.var_name_token.pos_start
        self.pos_end = self.var_name_token.pos_end

    def __repr__(self):
        return f'{self.var_name_token}'


class VarForgetNode:
    def __init__(self, var_name_token):
        self.var_name_token = var_name_token

        self.pos_start = self.var_name_token.pos_start
        self.pos_end = self.var_name_token.pos_end

    def __repr__(self):
        return f'{self.var_name_token}'


class VarAssignNode:
    def __init__(self, var_name_tokens, value_node):
        self.var_name_tokens = var_name_tokens
        self.value_node = value_node

        self.pos_start = self.var_name_tokens.elements[0].pos_start
        self.pos_end = self.value_node.pos_end

    def repr_list(self, _list):
        if isinstance(_list, values.List): _list = _list.elements
        string = ""
        for element in _list:
            string += str(element) + ", "
        mod_string = string[:-2]
        return mod_string

    def __repr__(self):
        return f'{self.repr_list(self.var_name_tokens)}'



class VarAssignOldNode:
    def __init__(self, var_name_tokens, value_node):
        self.var_name_tokens = var_name_tokens
        self.value_node = value_node

        self.pos_start = self.var_name_tokens.pos_start
        self.pos_end = self.value_node.pos_end

    def repr_list(self, _list):
        if isinstance(_list, values.List): _list = _list.elements
        string = ""
        for element in _list:
            string += str(element) + ", "
        mod_string = string[:-2]
        return mod_string

    def __repr__(self):
        return f'{self.repr_list(self.var_name_tokens)}'


class PartScriptAssignNode:
    def __init__(self, script_token, index_node, letter_value_node):
        self.script_token = script_token
        self.index_node = index_node
        self.letter_value_node = letter_value_node

        self.pos_start = self.script_token.pos_start
        self.pos_end = self.letter_value_node.pos_end

    def __repr__(self):
        return f'{self.script_token}[{self.index_node}]'


class PartScriptNode:
    def __init__(self, var_name, index_token):
        self.var_name = var_name
        self.index_token = index_token

        self.pos_start = self.var_name.pos_start
        self.pos_end = self.var_name.pos_end

    def __repr__(self):
        return f'{self.var_name}[{self.index_token}]'


################################### if/loop nodes ###################################

class IfNode:
    def __init__(self, cases, else_case):
        self.cases = cases
        self.else_case = else_case

        self.pos_start = self.cases[0][0].pos_start
        if self.else_case is not None:
            self.pos_end = self.else_case.pos_end
        else:
            self.pos_end = self.cases[len(self.cases) - 1][0].pos_end

    def __repr__(self):
        return f'if {self.cases}, else {self.else_case}'


class WhileNode:
    def __init__(self, condition_node, body_node):
        self.condition_node = condition_node
        self.body_node = body_node

        self.pos_start = self.condition_node.pos_start
        self.pos_end = self.body_node.pos_end

    def __repr__(self):
        return f'while {self.condition_node} gowon {self.body_node}'


class GowonNode:
    def __init__(self, body_node, condition_node):
        self.body_node = body_node
        self.condition_node = condition_node

        self.pos_start = self.condition_node.pos_start
        self.pos_end = self.body_node.pos_end

    def __repr__(self):
        return f'gowon {self.body_node}), while {self.condition_node}'

################################### bodger nodes ###################################

class BodgerCallNode:
    def __init__(self, bodger_name, expression):
        self.bodger_name = bodger_name
        self.expression = expression

        self.pos_start = bodger_name.pos_start
        self.pos_end = expression.pos_end

    def __repr__(self):
        return f'{self.bodger_name}'


class BodgerChangeNode:
    def __init__(self, bodger_name):
        self.bodger_name = bodger_name

        self.pos_start = bodger_name.pos_start
        self.pos_end = bodger_name.pos_end

    def __repr__(self):
        return f'{self.bodger_name}'


class AddBodgerNode:
    def __init__(self, bodger_name):
        self.bodger_name = bodger_name

        self.pos_start = bodger_name.pos_start
        self.pos_end = bodger_name.pos_end

    def __repr__(self):
        return f'{self.bodger_name}'


################################### fettle nodes ###################################

class FuncDefNode:
    def __init__(self, var_name_token, arg_dict, body_nodes, static_type_return):
        self.var_name_token = var_name_token
        self.arg_dict = arg_dict
        self.body_nodes = body_nodes
        self.static_type_return = static_type_return

        if self.var_name_token:
            self.pos_start = self.var_name_token.pos_start
        elif len(self.arg_dict) > 0:
            self.pos_start = self.next(iter(arg_dict)).pos_start
        else:
            self.pos_start = self.body_nodes.pos_start

        self.pos_end = self.body_nodes.pos_end

    def __repr__(self):
        return f'{self.var_name_token}({self.arg_dict})'


class CallNode:
    def __init__(self, node_to_call, arg_nodes):
        self.node_to_call = node_to_call
        self.arg_nodes = arg_nodes

        self.pos_start = self.node_to_call.pos_start

        if len(self.arg_nodes) > 0:
            self.pos_end = self.arg_nodes[len(self.arg_nodes) - 1].pos_end
        else:
            self.pos_end = self.node_to_call.pos_end

    def __repr__(self):
        return f'{self.node_to_call}({self.arg_nodes})'
