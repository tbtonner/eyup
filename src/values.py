import math
import bodgers
import interpreter
import nodes
import errors 

#######################################
# VALUES
# value classes that have functions that can alter the result
#######################################


class Value:
    def __init__(self):
        self.set_pos()
        self.set_context()

    def set_pos(self, pos_start=None, pos_end=None):
        self.pos_start = pos_start
        self.pos_end = pos_end
        return self

    def set_context(self, context=None):
        self.context = context
        return self

    def added_to(self, other):
        return None, self.illegal_operation(other)

    def subtracted_by(self, other):
        return None, self.illegal_operation(other)

    def multiplied_by(self, other):
        return None, self.illegal_operation(other)

    def divided_by(self, other):
        return None, self.illegal_operation(other)

    def call_by(self, other):
        return None, self.illegal_operation(other)

    def concated_by(self, other):
        return None, self.illegal_operation(other)

    def powed_by(self, other):
        return None, self.illegal_operation(other)

    def get_comparison_equals(self, other):
        return None, self.illegal_operation(other)

    def get_comparison_not_equals(self, other):
        return None, self.illegal_operation(other)

    def get_comparison_less_than(self, other):
        return None, self.illegal_operation(other)

    def get_comparison_greater_than(self, other):
        return None, self.illegal_operation(other)

    def get_comparison_less_than_equals(self, other):
        return None, self.illegal_operation(other)

    def get_comparison_greater_than_equals(self, other):
        return None, self.illegal_operation(other)

    def anded_by(self, other):
        return None, self.illegal_operation(other)

    def ored_by(self, other):
        return None, self.illegal_operation(other)

    def notted(self):
        return None, self.illegal_operation(self)

    def execute(self, args):
        return interpreter.RTResult().failure(self.illegal_operation())

    def copy(self):
        raise Exception('No copy method defined')

    def is_true(self):
        return False

    def illegal_operation(self, other=None):
        if not other:
            other = self
        return errors.FlummoxedError(
            self.pos_start, other.pos_end,
            f"Can't do that meddlin'",
            self.context
        )

####################################### atom values #######################################

class Answer(Value):
    def __init__(self, value):
        super().__init__()
        self.value = value

    def copy(self):
        copy = Answer(self.value)
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy

    def __repr__(self):
        return str(self.value)

    def anded_by(self, other):
        if isinstance(other, Answer):
            a = True if self.value == "aye" else False
            b = True if other.value == "aye" else False
            if (a and b):
                return Answer("aye").set_context(self.context), None
            return Answer("nay").set_context(self.context), None

    def ored_by(self, other):
        if isinstance(other, Answer):
            a = True if self.value == "aye" else False
            b = True if other.value == "aye" else False
            if (a or b):
                return Answer("aye").set_context(self.context), None
            return Answer("nay").set_context(self.context), None

    def notted(self):
        if self.value == ("aye"): 
            return Answer("nay").set_context(self.context), None
        return Answer("aye").set_context(self.context), None

    def is_true(self):
        return 1 if self.value == 'aye' else 0


Answer.aye = Answer("aye")
Answer.nay = Answer("nay")


class Nowt(Value):
    def __init__(self, value):
        super().__init__()
        self.value = value

    def copy(self):
        copy = Nowt(self.value)
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy

    def __repr__(self):
        return "nowt"
        # return "Nowt, Type: " + str(self.value)


Nowt.nowt = Nowt("nowt")


class Script(Value):
    def __init__(self, value):
        super().__init__()
        self.value = value

    def concated_by(self, other):
        if isinstance(other, Script) or isinstance(other, Letter):
            return Script(self.value + other.value).set_context(self.context), None
        if isinstance(other, Number):
            return Script(self.value + str(other.value)).set_context(self.context), None
        if isinstance(other, Answer):
            return Script(self.value + str(other.value)).set_context(self.context), None
        if isinstance(other, Letter):
            return Script(self.value + str(other.value)).set_context(self.context), None
        if isinstance(other, List):
            return Script(self.value + str(other.elements)).set_context(self.context), None
        return None, Value.illegal_operation(self, other)

    def multiplied_by(self, other):
        if isinstance(other, Number):
            return Script(self.value * other.value).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def is_true(self):
        return len(self.value) > 0

    def copy(self):
        copy = Script(self.value)
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy

    def __repr__(self):
        return str(self.value)


class Letter(Value):
    def __init__(self, value):
        super().__init__()
        self.value = value

    def concated_by(self, other):
        if isinstance(other, Script) or isinstance(other, Letter):
            return Script(self.value + other.value).set_context(self.context), None
        if isinstance(other, Number):
            return Script(self.value + str(other.value)).set_context(self.context), None
        if isinstance(other, Answer):
            return Script(self.value + str(other.value)).set_context(self.context), None
        if isinstance(other, Letter):
            return Script(self.value + str(other.value)).set_context(self.context), None
        if isinstance(other, List):
            return Script(self.value + str(other.elements)).set_context(self.context), None
        return None, Value.illegal_operation(self, other)

    def multiplied_by(self, other):
        if isinstance(other, Number):
            return Script(self.value * other.value).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def copy(self):
        copy = Script(self.value)
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy

    def __repr__(self):
        return str(self.value)

class Number(Value):
    def __init__(self, value):
        super().__init__()
        self.value = value

    def added_to(self, other):
        if isinstance(other, Number):
            return Number(self.value + other.value).set_context(self.context), None

    def subtracted_by(self, other):
        if isinstance(other, Number):
            return Number(self.value - other.value).set_context(self.context), None

    def multiplied_by(self, other):
        if isinstance(other, Number):
            return Number(self.value * other.value).set_context(self.context), None

    def modded_by(self, other):
        if isinstance(other, Number):
            return Number(self.value % other.value).set_context(self.context), None

    def divided_by(self, other):
        if isinstance(other, Number):
            if other.value == 0:
                return None, errors.FlummoxedError(
                    other.pos_start, other.pos_end,
                    'Division by zero',
                    self.context
                )

            return Number(self.value / other.value).set_context(self.context), None

    ######################################################

    def get_comparison_equals(self, other):
        if isinstance(other, Number):
            if (self.value == other.value):
                return Answer("aye").set_context(self.context), None
            return Answer("nay").set_context(self.context), None

    def get_comparison_not_equals(self, other):
        if isinstance(other, Number):
            if (self.value != other.value):
                return Answer("aye").set_context(self.context), None
            return Answer("nay").set_context(self.context), None

    def get_comparison_less_than(self, other):
        if isinstance(other, Number):
            if (self.value < other.value):
                return Answer("aye").set_context(self.context), None
            return Answer("nay").set_context(self.context), None

    def get_comparison_greater_than(self, other):
        if isinstance(other, Number):
            if (self.value > other.value):
                return Answer("aye").set_context(self.context), None
            return Answer("nay").set_context(self.context), None

    def get_comparison_less_than_equals(self, other):
        if isinstance(other, Number):
            if (self.value <= other.value):
                return Answer("aye").set_context(self.context), None
            return Answer("nay").set_context(self.context), None

    def get_comparison_greater_than_equals(self, other):
        if isinstance(other, Number):
            if (self.value >= other.value):
                return Answer("aye").set_context(self.context), None
            return Answer("nay").set_context(self.context), None

    ######################################################

    def copy(self):
        copy = Number(self.value)
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return str(self.value)


class List(Value):
    def __init__(self, elements):
        super().__init__()
        self.elements = elements

    def set_elements(self, new_elements):
        self.elements = new_elements

    def added_to(self, other):
        new_list = self.copy()
        new_list.elements.append(other)

        return new_list, None

    def copy(self):
        copy = List(self.elements.copy())
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy

    def subtracted_by(self, other):
        if isinstance(other, Number):
            new_list = self.copy()
            try:
                new_list.elements.pop(other.value)
                return new_list, None
            except:
                return None, errors.FlummoxedError(
                    other.pos_start, other.pos_end,
                    f"'{other.value}' tis out'v range of {self.elements}",
                    self.context
                )
        else:
            return None, Value.illegal_operation(self, other)

    def multiplied_by(self, other):
        if isinstance(other, List):
            new_list = self.copy()
            new_list.elements.extend(other.elements)
            return new_list, None
        else:
            return None, Value.illegal_operation(self, other)

    def __str__(self):
        return f'[{", ".join([repr(x) for x in self.elements])}]'

    def __repr__(self):
        return f'[{", ".join([repr(x) for x in self.elements])}]'

####################################### fettle values #######################################

class BaseFunction(Value):
    def __init__(self, name):
        super().__init__()
        self.name = name or "<anonymous>"

    def generate_new_context(self):
        new_context = bodgers.Context(self.name, self.context, self.pos_start)
        new_context.symbol_table = bodgers.SymbolTable(
            new_context.parent.symbol_table.copySymbols())
        return new_context

    def too_few_too_many(self, args, arg_list_dict):
        result = interpreter.RTResult()

        if len(args) > len(arg_list_dict):
            string = ""
            for i in range(len(args) - len(arg_list_dict)):
                string += str(args[-(i+1)]) + ":" + \
                    type(args[-(i+1)]).__name__ + ", "
            string = string[:len(string) - 2]

            return result.failure(errors.FlummoxedError(
                self.pos_start, self.pos_end,
                f"{self.name} wi' traipsin' {string}",
                self.context
            ))

        if len(args) < len(arg_list_dict):
            string = ""
            if len(args) != 0:
                diff = len(arg_list_dict) - len(args)
                for i in range(diff):
                    current = list(arg_list_dict)[-(i+1)]
                    if isinstance(current, str):
                        string += current + ", "
                    else:
                        string += str(current.value) + ":" + str(arg_list_dict[current]) + ", "
                string = string[:len(string) - 2]

            return result.failure(errors.FlummoxedError(
                self.pos_start, self.pos_end,
                f"{self.name} bah't {string}",
                self.context
            ))

        return result.success(True)

    def check_args(self, arg_dict, args):
        result = interpreter.RTResult()

        correct_no_args = self.too_few_too_many(args, arg_dict)
        if correct_no_args.error:
            return correct_no_args

        iterator = 0
        for identifer_token, old_type in arg_dict.items():
            new_type = interpreter.Interpreter.eyupise_value(
                result, args[iterator])
            if old_type != new_type:
                return result.failure(errors.FlummoxedError(
                    self.pos_start, self.pos_end,
                    f"Check yer types pal! {new_type} ain't the same as {old_type}",
                    self.context
                ))
            iterator = iterator + 1

        return result.success(None)

    def populate_args(self, arg_names, args, execution_context):
        for i in range(len(args)):
            arg_name = arg_names[i]
            arg_value = args[i]
            arg_value.set_context(execution_context)
            execution_context.symbol_table.set(arg_name, arg_value)

    def check_and_populate_args(self, arg_dict, args, built_in, execution_context):
        result = interpreter.RTResult()

        if built_in:
            arg_names = arg_dict
        else:
            result.register(self.check_args(arg_dict, args))
            if result.error:
                return result

            arg_names = []
            for arg_name in arg_dict.keys():
                arg_names.append(arg_name.value)

        self.populate_args(arg_names, args, execution_context)
        return result.success(None)


class Function(BaseFunction):
    def __init__(self, name, body_nodes, arg_dict, static_type_return):
        super().__init__(name)
        self.name = name
        self.body_nodes = body_nodes
        self.arg_dict = arg_dict
        self.static_type_return = static_type_return
        self.value = Nowt.nowt

    @classmethod
    def setValue(self, value):
        self.value = value

    @classmethod
    def getValue(self):
        return self.value

    def execute(self, args):
        result = interpreter.RTResult()
        _interpreter = interpreter.Interpreter()
        execution_context = self.context
        self.setValue(Nowt.nowt)

        result.register(self.check_and_populate_args(
            self.arg_dict, args, False, execution_context))
        if result.error:
            return result

        if not isinstance(self.body_nodes.element_nodes, nodes.NowtNode):
            for _node in self.body_nodes.element_nodes:
                if isinstance(_node, nodes.NowtNodeWangNode):
                    temp = _interpreter.visit(_node, execution_context)
                    if temp.error:
                        return result.failure(errors.FlummoxedError(
                            self.pos_start, _node.pos_end,
                            f"Wangged condition: {_node.condition} is aye",
                            self.context
                        ))
                else:
                    temp = result.register(
                        _interpreter.visit(_node, execution_context))

        if result.error:
            return result

        self.value = self.getValue()

        value_type = interpreter.Interpreter.eyupise_value(result, self.value)
        if self.static_type_return is not None:
            if self.static_type_return != value_type:
                return result.failure(errors.FlummoxedError(
                    self.pos_start, self.pos_end,
                    f"Check yer types pal! {self.static_type_return} ain't the same as {value_type}",
                    self.context
                ))

        return result.success(self.value)

    def copy(self):
        copy = Function(self.name, self.body_nodes,
                        self.arg_dict, self.static_type_return)
        copy.set_context(self.context)
        copy.set_pos(self.pos_start, self.pos_end)
        return copy

    def __repr__(self):
        return f"{bodgers.CURRENT_BODGER.name}.{self.name}"


class BuiltInFunction(BaseFunction):
    def __init__(self, name):
        super().__init__(name)

    def execute(self, args):
        result = interpreter.RTResult()
        execution_context = self.generate_new_context()

        method_name = f'execute_{self.name}'
        method = getattr(self, method_name, self.no_visit_method)

        if not self.name == 'input':
            correct_no_args = self.too_few_too_many(args, method.arg_list)
            if correct_no_args.error:
                return correct_no_args
        else:
            if not len(args) == 0:
                correct_no_args = self.too_few_too_many(args, method.arg_list)
                if correct_no_args.error:
                    return correct_no_args

        result.register(self.check_and_populate_args(
            method.arg_list, args, True, execution_context))
        if result.error:
            return result

        return_value = result.register(method(execution_context))
        if result.error:
            return result
        return result.success(return_value)

    def no_visit_method(self, node, context):
        raise Exception(f'No execute_{self.name} method defined')

    def copy(self):
        copy = BuiltInFunction(self.name)
        copy.set_context(self.context)
        copy.set_pos(self.pos_start, self.pos_end)
        return copy

    def __repr__(self):
        return f"<built-in function {self.name}>"

    ################################### Global Built-in-Functions ###################################

    def execute_print(self, execution_context):
        print(str(execution_context.symbol_table.get('value')))
        return interpreter.RTResult().success(Nowt.nowt)
    execute_print.arg_list = ["value"]

    def execute_input(self, execution_context):
        prompt = str(execution_context.symbol_table.get('value'))
        if prompt == 'None':
            text = input()
        else:
            text = input(prompt)

        if text.isnumeric():
            return interpreter.RTResult().success(Number(float(text)))
        return interpreter.RTResult().success(Script(text))
    execute_input.arg_list = ["value"]

    def execute_isNumber(self, execution_context):
        isNumber = isinstance(
            execution_context.symbol_table.get("value"), Number)
        return interpreter.RTResult().success(Answer.aye if isNumber else Answer.nay)
    execute_isNumber.arg_list = ["value"]

    def execute_isScript(self, execution_context):
        isScript = isinstance(
            execution_context.symbol_table.get("value"), Script)
        return interpreter.RTResult().success(Answer.aye if isScript else Answer.nay)
    execute_isScript.arg_list = ["value"]

    def execute_isList(self, execution_context):
        isList = isinstance(
            execution_context.symbol_table.get("value"), List)
        return interpreter.RTResult().success(Answer.aye if isList else Answer.nay)
    execute_isList.arg_list = ["value"]

    def execute_isFettle(self, execution_context):
        isFettle = isinstance(
            execution_context.symbol_table.get("value"), BaseFunction)
        return interpreter.RTResult().success(Answer.aye if isFettle else Answer.nay)
    execute_isFettle.arg_list = ["value"]

    def execute_isLetter(self, execution_context):
        isLetter = isinstance(
            execution_context.symbol_table.get("value"), Letter)
        return interpreter.RTResult().success(Answer.aye if isLetter else Answer.nay)
    execute_isLetter.arg_list = ["value"]

    def execute_isBodger(self, execution_context):
        isBodger = isinstance(
            execution_context.symbol_table.get("value"), BodgerVal)
        return interpreter.RTResult().success(Answer.aye if isBodger else Answer.nay)
    execute_isBodger.arg_list = ["value"]

    def execute_isAnswer(self, execution_context):
        isAnswer = isinstance(
            execution_context.symbol_table.get("value"), Answer)
        return interpreter.RTResult().success(Answer.aye if isAnswer else Answer.nay)
    execute_isAnswer.arg_list = ["value"]

    def execute_isNowt(self, execution_context):
        isNowt = isinstance(
            execution_context.symbol_table.get("value"), Nowt)
        return interpreter.RTResult().success(Answer.aye if isNowt else Answer.nay)
    execute_isNowt.arg_list = ["value"]

    def execute_toNumber(self, execution_context):
        result = interpreter.RTResult()

        # getting the value -> validating input is str or num
        value_to_convert = execution_context.symbol_table.get("value")
        if not isinstance(value_to_convert, Script) and not isinstance(value_to_convert, Number) and not isinstance(value_to_convert, Letter):
            return result.failure(errors.FlummoxedError(
                self.pos_start, self.pos_end,
                "{value_to_convert} ain't a script, number or letter",
                execution_context
            ))
        value_to_convert = value_to_convert.value

        # attempt convert to float
        try:
            number = float(value_to_convert)
        except ValueError:
            return result.failure(errors.FlummoxedError(
                self.pos_start, self.pos_end,
                "{value_to_convert} ain't a number",
                execution_context
            ))
        if number.is_integer():
            number = int(number)
        return result.success(Number(number))
    execute_toNumber.arg_list = ["value"]

    def execute_toScript(self, execution_context):
        result = interpreter.RTResult()

        # getting the value -> validating input is str or num
        value_to_convert = execution_context.symbol_table.get("value")
        if not isinstance(value_to_convert, Script) and not isinstance(value_to_convert, Number) and not isinstance(value_to_convert, Letter) and not isinstance(value_to_convert, List):
            return result.failure(errors.FlummoxedError(
                self.pos_start, self.pos_end,
                "{value_to_convert} ain't a script, number, list or letter",
                execution_context
            ))
        if isinstance(value_to_convert, List):
            value_to_convert = str(value_to_convert.elements)
        else:
            value_to_convert = str(value_to_convert.value)

        return result.success(Script(value_to_convert))
    execute_toScript.arg_list = ["value"]

    def execute_add(self, execution_context):
        list_ = execution_context.symbol_table.get("list")
        value = execution_context.symbol_table.get("value")

        if not isinstance(list_, List):
            return interpreter.RTResult().failure(errors.FlummoxedError(
                self.pos_start, self.pos_end,
                f"{list_} ain't no list",
                execution_context
            ))

        list_.elements.append(value)
        return interpreter.RTResult().success(list_)
    execute_add.arg_list = ["list", "value"]

    def execute_take(self, execution_context):
        list_ = execution_context.symbol_table.get("list")
        index = execution_context.symbol_table.get("index")

        if not isinstance(list_, List):
            return interpreter.RTResult().failure(errors.FlummoxedError(
                self.pos_start, self.pos_end,
                f"{list_} ain't no list",
                execution_context
            ))

        if not isinstance(index, Number):
            return interpreter.RTResult().failure(errors.FlummoxedError(
                self.pos_start, self.pos_end,
                f"{index} ain't no Number",
                execution_context
            ))

        try:
            element = list_.elements.pop(index.value)
        except:
            return interpreter.RTResult().failure(errors.FlummoxedError(
                self.pos_start, self.pos_end,
                f"'{index}' tis out'v range of {list_}",
                execution_context
            ))
        return interpreter.RTResult().success(element)
    execute_take.arg_list = ["list", "index"]

    def execute_has(self, execution_context):
        list_ = execution_context.symbol_table.get("list")
        value = execution_context.symbol_table.get("value")

        if not isinstance(list_, List):
            return interpreter.RTResult().failure(errors.FlummoxedError(
                self.pos_start, self.pos_end,
                f"{list_} ain't no list",
                execution_context
            ))

        if not (isinstance(value, Number) or isinstance(value, Script) or isinstance(value, Letter) or isinstance(value, Answer)):
            return interpreter.RTResult().failure(errors.FlummoxedError(
                self.pos_start, self.pos_end,
                f"{value} ain't no number, script, letter or answer",
                execution_context
            ))

        has = False
        for l_value in list_.elements:
            if l_value.value == value.value:
                has = True

        return interpreter.RTResult().success(Answer.aye if has else Answer.nay)
    execute_has.arg_list = ["list", "value"]

    def execute_hasOwt(self, execution_context):
        list_ = execution_context.symbol_table.get("list")

        if not isinstance(list_, List):
            return interpreter.RTResult().failure(errors.FlummoxedError(
                self.pos_start, self.pos_end,
                f"{list_} ain't no list",
                execution_context
            ))

        hasOwt = False if len(list_.elements) == 0 else True

        return interpreter.RTResult().success(Answer.aye if hasOwt else Answer.nay)
    execute_hasOwt.arg_list = ["list"]

    def execute_hasNowt(self, execution_context):
        list_ = execution_context.symbol_table.get("list")

        if not isinstance(list_, List):
            return interpreter.RTResult().failure(errors.FlummoxedError(
                self.pos_start, self.pos_end,
                f"{list_} ain't no list",
                execution_context
            ))

        hasNowt = True if len(list_.elements) == 0 else False
        return interpreter.RTResult().success(Answer.aye if hasNowt else Answer.nay)
    execute_hasNowt.arg_list = ["list"]

    def execute_addAll(self, execution_context):
        list_ = execution_context.symbol_table.get("list")
        other_list = execution_context.symbol_table.get("other_list")

        if not isinstance(list_, List):
            return interpreter.RTResult().failure(errors.FlummoxedError(
                self.pos_start, self.pos_end,
                f"{list_} ain't no list",
                execution_context
            ))

        if not isinstance(other_list, List):
            return interpreter.RTResult().failure(errors.FlummoxedError(
                self.pos_start, self.pos_end,
                f"{other_list} ain't no list",
                execution_context
            ))

        for value in other_list.elements:
            list_.elements.append(value)
        return interpreter.RTResult().success(list_)
    execute_addAll.arg_list = ["list", "other_list"]

    def execute_takeAll(self, execution_context):
        list_ = execution_context.symbol_table.get("list")
        values = execution_context.symbol_table.get("values")

        if not isinstance(list_, List):
            return interpreter.RTResult().failure(errors.FlummoxedError(
                self.pos_start, self.pos_end,
                f"{list_} ain't no list",
                execution_context
            ))

        if not isinstance(values, List):
            return interpreter.RTResult().failure(errors.FlummoxedError(
                self.pos_start, self.pos_end,
                f"{values} ain't no list",
                execution_context
            ))

        elements = []

        for value in values.elements:
            try:
                if not isinstance(value, Number):
                    return interpreter.RTResult().failure(errors.FlummoxedError(
                        self.pos_start, self.pos_end,
                        f"{value} ain't no Number",
                        execution_context
                    ))
                value = value.value
                elements.append(list_.elements[value])
            except:
                return interpreter.RTResult().failure(errors.FlummoxedError(
                    self.pos_start, self.pos_end,
                    f"'{value}' tis out'v range of {list_}",
                    execution_context
                ))
        return interpreter.RTResult().success(List(elements))
    execute_takeAll.arg_list = ["list", "values"]

    ################################### TrigMath Built-in-Functions ###################################

    def execute_sin(self, execution_context):
        number = execution_context.symbol_table.get("value")
        if not isinstance(number, Number):
            return interpreter.RTResult().failure(errors.FlummoxedError(
                self.pos_start, self.pos_end,
                "{number} ain't a number",
                execution_context
            ))

        result = Number(math.sin(number.value))
        return interpreter.RTResult().success(result)
    execute_sin.arg_list = ["value"]

    def execute_cos(self, execution_context):
        number = execution_context.symbol_table.get("value")
        if not isinstance(number, Number):
            return interpreter.RTResult().failure(errors.FlummoxedError(
                self.pos_start, self.pos_end,
                "{number} ain't a number",
                execution_context
            ))

        result = Number(math.cos(number.value))
        return interpreter.RTResult().success(result)
    execute_cos.arg_list = ["value"]

    def execute_tan(self, execution_context):
        number = execution_context.symbol_table.get("value")
        if not isinstance(number, Number):
            return interpreter.RTResult().failure(errors.FlummoxedError(
                self.pos_start, self.pos_end,
                "{number} ain't a number",
                execution_context
            ))

        result = Number(math.tan(number.value))
        return interpreter.RTResult().success(result)
    execute_tan.arg_list = ["value"]

    def execute_hypot(self, execution_context):
        a = execution_context.symbol_table.get("a")
        b = execution_context.symbol_table.get("b")

        if not (isinstance(a, Number) and isinstance(b, Number)):
            return interpreter.RTResult().failure(errors.FlummoxedError(
                self.pos_start, self.pos_end,
                "{a} and/or {b} ain't a number",
                execution_context
            ))

        result = Number(math.hypot(a.value, b.value))
        return interpreter.RTResult().success(result)
    execute_hypot.arg_list = ["a", "b"]

    def execute_degrees(self, execution_context):
        number = execution_context.symbol_table.get("value")
        if not isinstance(number, Number):
            return interpreter.RTResult().failure(errors.FlummoxedError(
                self.pos_start, self.pos_end,
                "{number} ain't a number",
                execution_context
            ))

        result = Number(math.degrees(number.value))
        return interpreter.RTResult().success(result)
    execute_degrees.arg_list = ["value"]

    def execute_radians(self, execution_context):
        number = execution_context.symbol_table.get("value")
        if not isinstance(number, Number):
            return interpreter.RTResult().failure(errors.FlummoxedError(
                self.pos_start, self.pos_end,
                "{number} ain't a number",
                execution_context
            ))

        result = Number(math.radians(number.value))
        return interpreter.RTResult().success(result)
    execute_radians.arg_list = ["value"]

    def execute_asin(self, execution_context):
        number = execution_context.symbol_table.get("value")
        if not isinstance(number, Number):
            return interpreter.RTResult().failure(errors.FlummoxedError(
                self.pos_start, self.pos_end,
                "{number} ain't a number",
                execution_context
            ))

        result = Number(math.asin(number.value))
        return interpreter.RTResult().success(result)
    execute_asin.arg_list = ["value"]

    def execute_acos(self, execution_context):
        number = execution_context.symbol_table.get("value")
        if not isinstance(number, Number):
            return interpreter.RTResult().failure(errors.FlummoxedError(
                self.pos_start, self.pos_end,
                "{number} ain't a number",
                execution_context
            ))

        result = Number(math.acos(number.value))
        return interpreter.RTResult().success(result)
    execute_acos.arg_list = ["value"]

    def execute_atan(self, execution_context):
        number = execution_context.symbol_table.get("value")
        if not isinstance(number, Number):
            return interpreter.RTResult().failure(errors.FlummoxedError(
                self.pos_start, self.pos_end,
                "{number} ain't a number",
                execution_context
            ))

        result = Number(math.atan(number.value))
        return interpreter.RTResult().success(result)
    execute_atan.arg_list = ["value"]

    ################################### LogMath Built-in-Functions ###################################
    def execute_log(self, execution_context):
        number = execution_context.symbol_table.get("value")
        if not isinstance(number, Number):
            return interpreter.RTResult().failure(errors.FlummoxedError(
                self.pos_start, self.pos_end,
                "{number} ain't a number",
                execution_context
            ))

        result = Number(math.log(number.value))
        return interpreter.RTResult().success(result)
    execute_log.arg_list = ["value"]

    def execute_log2(self, execution_context):
        number = execution_context.symbol_table.get("value")
        if not isinstance(number, Number):
            return interpreter.RTResult().failure(errors.FlummoxedError(
                self.pos_start, self.pos_end,
                "{number} ain't a number",
                execution_context
            ))

        result = Number(math.log2(number.value))
        return interpreter.RTResult().success(result)
    execute_log2.arg_list = ["value"]

    def execute_log10(self, execution_context):
        number = execution_context.symbol_table.get("value")
        if not isinstance(number, Number):
            return interpreter.RTResult().failure(errors.FlummoxedError(
                self.pos_start, self.pos_end,
                "{number} ain't a number",
                execution_context
            ))

        result = Number(math.log10(number.value))
        return interpreter.RTResult().success(result)
    execute_log10.arg_list = ["value"]

    def execute_logBase(self, execution_context):
        number = execution_context.symbol_table.get("value")
        base = execution_context.symbol_table.get("base")
        if not (isinstance(number, Number) and isinstance(base, Number)):
            return interpreter.RTResult().failure(errors.FlummoxedError(
                self.pos_start, self.pos_end,
                "{number} and/or {base} ain't a number",
                execution_context
            ))

        result = Number(math.log(number.value, base.value))
        return interpreter.RTResult().success(result)
    execute_logBase.arg_list = ["value", "base"]

    ################################### PolyMath Built-in-Functions ###################################
    def execute_pow(self, execution_context):
        number = execution_context.symbol_table.get("value")
        pow_of = execution_context.symbol_table.get("pow_of")
        if not (isinstance(number, Number) and isinstance(pow_of, Number)):
            return interpreter.RTResult().failure(errors.FlummoxedError(
                self.pos_start, self.pos_end,
                "{number} ain't a number",
                execution_context
            ))

        result = Number(math.pow(number.value, pow_of.value))
        return interpreter.RTResult().success(result)
    execute_pow.arg_list = ["value", "pow_of"]

    def execute_sqrt(self, execution_context):
        number = execution_context.symbol_table.get("value")
        if not isinstance(number, Number):
            return interpreter.RTResult().failure(errors.FlummoxedError(
                self.pos_start, self.pos_end,
                "{number} ain't a number",
                execution_context
            ))

        result = Number(math.sqrt(number.value))
        return interpreter.RTResult().success(result)
    execute_sqrt.arg_list = ["value"]

    def execute_maximum(self, execution_context):
        n1 = execution_context.symbol_table.get("num1")
        n2 = execution_context.symbol_table.get("num2")

        if not isinstance(n1, Number):
            return interpreter.RTResult().failure(errors.FlummoxedError(
                self.pos_start, self.pos_end,
                "{n1} ain't a number",
                execution_context
            ))
        n1 = n1.value

        if not isinstance(n2, Number):
            return interpreter.RTResult().failure(errors.FlummoxedError(
                self.pos_start, self.pos_end,
                "{n2} ain't a number",
                execution_context
            ))
        n2 = n2.value

        result = Number(n1 if n1 > n2 else n2)
        return interpreter.RTResult().success(result)
    execute_maximum.arg_list = ["num1", "num2"]

    def execute_minimum(self, execution_context):
        n1 = execution_context.symbol_table.get("num1")
        n2 = execution_context.symbol_table.get("num2")

        if not isinstance(n1, Number):
            return interpreter.RTResult().failure(errors.FlummoxedError(
                self.pos_start, self.pos_end,
                "{n1} ain't a number",
                execution_context
            ))
        n1 = n1.value

        if not isinstance(n2, Number):
            return interpreter.RTResult().failure(errors.FlummoxedError(
                self.pos_start, self.pos_end,
                "{n2} ain't a number",
                execution_context
            ))
        n2 = n2.value

        result = Number(n1 if n1 < n2 else n2)
        return interpreter.RTResult().success(result)
    execute_minimum.arg_list = ["num1", "num2"]

    ################################################################


# General global functions
BuiltInFunction.print = BuiltInFunction("print")
BuiltInFunction.input = BuiltInFunction("input")
BuiltInFunction.isNumber = BuiltInFunction("isNumber")
BuiltInFunction.isScript = BuiltInFunction("isScript")
BuiltInFunction.isList = BuiltInFunction("isList")
BuiltInFunction.isFettle = BuiltInFunction("isFettle")
BuiltInFunction.isLetter = BuiltInFunction("isLetter")
BuiltInFunction.isBodger = BuiltInFunction("isBodger")
BuiltInFunction.isAnswer = BuiltInFunction("isAnswer")
BuiltInFunction.isNowt = BuiltInFunction("isNowt")
BuiltInFunction.toNumber = BuiltInFunction("toNumber")
BuiltInFunction.toScript = BuiltInFunction("toScript")
BuiltInFunction.add = BuiltInFunction("add")
BuiltInFunction.take = BuiltInFunction("take")
BuiltInFunction.has = BuiltInFunction("has")
BuiltInFunction.hasOwt = BuiltInFunction("hasOwt")
BuiltInFunction.hasNowt = BuiltInFunction("hasNowt")
BuiltInFunction.addAll = BuiltInFunction("addAll")
BuiltInFunction.takeAll = BuiltInFunction("takeAll")

# TrigMath
BuiltInFunction.sin = BuiltInFunction("sin")
BuiltInFunction.cos = BuiltInFunction("cos")
BuiltInFunction.tan = BuiltInFunction("tan")
BuiltInFunction.hypot = BuiltInFunction("hypot")
BuiltInFunction.degrees = BuiltInFunction("degrees")
BuiltInFunction.radians = BuiltInFunction("radians")
BuiltInFunction.asin = BuiltInFunction("asin")
BuiltInFunction.acos = BuiltInFunction("acos")
BuiltInFunction.atan = BuiltInFunction("atan")

# LogMath
BuiltInFunction.log = BuiltInFunction("log")
BuiltInFunction.log2 = BuiltInFunction("log2")
BuiltInFunction.log10 = BuiltInFunction("log10")
BuiltInFunction.logBase = BuiltInFunction("logBase")

# PolyMath
BuiltInFunction.pow = BuiltInFunction("pow")
BuiltInFunction.sqrt = BuiltInFunction("sqrt")
BuiltInFunction.maximum = BuiltInFunction("maximum")
BuiltInFunction.minimum = BuiltInFunction("minimum")

####################################### bodger value #######################################

class BodgerVal(Value):
    def __init__(self, bodger):
        super().__init__()
        self.bodger = bodger

    def copy(self):
        copy = BodgerVal(self.bodger)
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy

    def __str__(self):
        return f'{self.bodger.name}'

    def __repr__(self):
        return f'{self.bodger.name}'

    def call_by(self, other):
        if isinstance(other, Number):
            return Number(other.value), None
        if isinstance(other, List):
            return List(other.elements), None
        if isinstance(other, Answer):
            return Answer(other.value), None
        if isinstance(other, Letter):
            return Letter(other.value), None
        if isinstance(other, Script):
            return Script(other.value), None
        if isinstance(other, Nowt):
            return Nowt(other.value), None
        if isinstance(other, BuiltInFunction):
            return BuiltInFunction(other), None
        if isinstance(other, Function):
            return Function(other), None
        if isinstance(other, BodgerVal):
            return BodgerVal(other.bodger), None

        return BodgerVal(self.bodger), None
