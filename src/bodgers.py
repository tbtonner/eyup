from . import values
from . import interpreter
from . import nodes
from . import tokens
from . import parse

#######################################
# CONTEXT
# current display name, any parents, their entry pos and the symbol table of current context
#######################################


class Context:
    def __init__(self, display_name, parent=None, parent_entry_pos=None):
        self.display_name = display_name
        self.parent = parent
        self.parent_entry_pos = parent_entry_pos
        self.symbol_table = None

#######################################
# SYMBOL TABLE
# memory of summats, fettles and bodgers etc. -> saved as python dict
#######################################

class SymbolTable:
    def __init__(self, symbols={}, parent=None):
        self.symbols = symbols
        self.parent = parent

    def get(self, name):
        value = self.symbols.get(name, None)
        if value == None and self.parent:
            return self.parent.get(name)
        return value

    def set(self, name, value, allus=False):
        if allus:
            self.symbols[name] = nodes.AllusNode(value)
        else:
            self.symbols[name] = value

    def remove(self, name):
        del self.symbols[name]

    def copySymbols(self):
        new_dict = {}
        for symbol, value in self.symbols.items():
            if not isinstance(value, nodes.AllusNode):
                new_dict[symbol] = value.copy()
            else:
                new_dict[symbol] = value
        return new_dict


#######################################
# BODGER
# eyup bodger class 
#######################################

class Bodger():
    def __init__(self, name, context, parent=None):
        self.name = name
        self._interpreter = interpreter.Interpreter()
        self.context = context
        self.parent = parent

    def run(self, text):
        # tokenise input string
        tokeniser = tokens.Tokenise(text)
        tokens_, error = tokeniser.make_tokens()
        if error:
            return None, error

        # generate abstract syntax tree (AST) - parse tokens
        parser = parse.Parser(tokens_)
        ast = parser.parse()
        if ast.error:
            return None, ast.error

        # interpret ast
        result = self._interpreter.visit(ast.node, self.context)
        return result.value, result.error

    def partRun(self, node): # for when text string is already parsed by different bodger
        return self._interpreter.visit(node, self.context)


################################### The Global Symbol Table ###################################
global_symbol_table = SymbolTable()
global_symbol_table.set("nowt", values.Nowt.nowt, True)
global_symbol_table.set("aye", values.Answer.aye, True)
global_symbol_table.set("nay", values.Answer.nay, True)

global_symbol_table.set("write", values.BuiltInFunction.print, True)
global_symbol_table.set("prompt", values.BuiltInFunction.input, True)

global_symbol_table.set("isNumber", values.BuiltInFunction.isNumber, True)
global_symbol_table.set("isScript", values.BuiltInFunction.isScript, True)
global_symbol_table.set("isList", values.BuiltInFunction.isList, True)
global_symbol_table.set("isFettle", values.BuiltInFunction.isFettle, True)
global_symbol_table.set("isLetter", values.BuiltInFunction.isLetter, True)
global_symbol_table.set("isBodger", values.BuiltInFunction.isBodger, True)
global_symbol_table.set("isAnswer", values.BuiltInFunction.isAnswer, True)
global_symbol_table.set("isNowt", values.BuiltInFunction.isNowt, True)
global_symbol_table.set("toNumber", values.BuiltInFunction.toNumber, True)
global_symbol_table.set("toScript", values.BuiltInFunction.toScript, True)

global_symbol_table.set("add", values.BuiltInFunction.add, True)
global_symbol_table.set("take", values.BuiltInFunction.take, True)
global_symbol_table.set("has", values.BuiltInFunction.has, True)
global_symbol_table.set("hasOwt", values.BuiltInFunction.hasOwt, True)
global_symbol_table.set("hasNowt", values.BuiltInFunction.hasNowt, True)
global_symbol_table.set("addAll", values.BuiltInFunction.addAll, True)
global_symbol_table.set("takeAll", values.BuiltInFunction.takeAll, True)

################################### The Gaffer ###################################
gaffer_context = Context("Gaffer")
gaffer_context.symbol_table = SymbolTable(global_symbol_table.copySymbols())
Gaffer = Bodger("Gaffer", gaffer_context)

################################### TrigMath Bodger ###################################
# defines the constant pi and standard trigonometric functions
trig_context = Context("TrigMath")
trig_context.symbol_table = SymbolTable(global_symbol_table.copySymbols())
TrigMath = Bodger("TrigMath", trig_context, Gaffer)

TrigMath.context.symbol_table.set("pi", values.Number(3.1415926535), True)
TrigMath.context.symbol_table.set("sin", values.BuiltInFunction.sin, True)
TrigMath.context.symbol_table.set("cos", values.BuiltInFunction.cos, True)
TrigMath.context.symbol_table.set("tan", values.BuiltInFunction.tan, True)
TrigMath.context.symbol_table.set("hypot", values.BuiltInFunction.hypot, True)
TrigMath.context.symbol_table.set(
    "degrees", values.BuiltInFunction.degrees, True)
TrigMath.context.symbol_table.set(
    "radians", values.BuiltInFunction.radians, True)
TrigMath.context.symbol_table.set("asin", values.BuiltInFunction.asin, True)
TrigMath.context.symbol_table.set("acos", values.BuiltInFunction.acos, True)
TrigMath.context.symbol_table.set("atan", values.BuiltInFunction.atan, True)


################################### LogMath Bodger ###################################
# defines Euler's constant e, logarithm and exponential functions
log_context = Context("LogMath")
log_context.symbol_table = SymbolTable(global_symbol_table.copySymbols())
LogMath = Bodger("LogMath", log_context, Gaffer)

LogMath.context.symbol_table.set("e", values.Number(2.7182818284), True)
LogMath.context.symbol_table.set("log", values.BuiltInFunction.log, True)
LogMath.context.symbol_table.set("log2", values.BuiltInFunction.log2, True)
LogMath.context.symbol_table.set("log10", values.BuiltInFunction.log10, True)
LogMath.context.symbol_table.set(
    "logBase", values.BuiltInFunction.logBase, True)

################################### PolyMath Bodger ###################################
# defines polynomial powers and roots of different degrees
poly_context = Context("PolyMath")
poly_context.symbol_table = SymbolTable(global_symbol_table.copySymbols())
PolyMath = Bodger("PolyMath", poly_context, Gaffer)

PolyMath.context.symbol_table.set("sqrt", values.BuiltInFunction.sqrt, True)
PolyMath.context.symbol_table.set("pow", values.BuiltInFunction.pow, True)
PolyMath.context.symbol_table.set("maximum", values.BuiltInFunction.maximum, True)
PolyMath.context.symbol_table.set("minimum", values.BuiltInFunction.minimum, True)

############################## Bodger Knowledge of each other ##############################
Gaffer.context.symbol_table.set("Gaffer", values.BodgerVal(Gaffer), True)
Gaffer.context.symbol_table.set("TrigMath", values.BodgerVal(TrigMath), True)
Gaffer.context.symbol_table.set("LogMath", values.BodgerVal(LogMath), True)
Gaffer.context.symbol_table.set("PolyMath", values.BodgerVal(PolyMath), True)

TrigMath.context.symbol_table.set("Gaffer", values.BodgerVal(Gaffer), True)
TrigMath.context.symbol_table.set("TrigMath", values.BodgerVal(TrigMath), True)
TrigMath.context.symbol_table.set("LogMath", values.BodgerVal(LogMath), True)
TrigMath.context.symbol_table.set("PolyMath", values.BodgerVal(PolyMath), True)

LogMath.context.symbol_table.set("Gaffer", values.BodgerVal(Gaffer), True)
LogMath.context.symbol_table.set("TrigMath", values.BodgerVal(TrigMath), True)
LogMath.context.symbol_table.set("LogMath", values.BodgerVal(LogMath), True)
LogMath.context.symbol_table.set("PolyMath", values.BodgerVal(PolyMath), True)

PolyMath.context.symbol_table.set("Gaffer", values.BodgerVal(Gaffer), True)
PolyMath.context.symbol_table.set("TrigMath", values.BodgerVal(TrigMath), True)
PolyMath.context.symbol_table.set("LogMath", values.BodgerVal(LogMath), True)
PolyMath.context.symbol_table.set("PolyMath", values.BodgerVal(PolyMath), True)

CURRENT_BODGER = Gaffer