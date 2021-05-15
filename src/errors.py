import bodgers

#######################################
# ERRORS
# display and return errors from this class
#######################################


class Error:
    def __init__(self, pos_start, pos_end, error_name, details):
        self.pos_start = pos_start
        self.pos_end = pos_end
        self.error_name = error_name
        self.details = details

    def as_string(self):
        result = f'\n{self.error_name}: {self.details}\n'
        result += f'problem in {bodgers.CURRENT_BODGER.name}, line {self.pos_start.line_number + 1}:'
        result += '\n\n' + \
            self.string_with_arrows(self.pos_start.ftxt,
                                    self.pos_start, self.pos_end)
        return result

    def string_with_arrows(self, text, pos_start, pos_end):
        result = ''
        # calculate indices
        index_start = max(text.rfind('\n', 0, pos_start.index), 0)
        index_end = text.find('\n', index_start + 1)
        if index_end < 0:
            index_end = len(text)

        # generate each line
        line_count = pos_end.line_number - pos_start.line_number + 1
        for i in range(line_count):
            # calculate line columnumns
            line = text[index_start:index_end]
            column_start = pos_start.column_number if i == 0 else 0
            column_end = pos_end.column_number if i == line_count - \
                1 else len(line) - 1

            # append to result
            result += line + '\n'
            result += ' ' * column_start + '^' * (column_end - column_start)

            # re-calculate indices
            index_start = index_end
            index_end = text.find('\n', index_start + 1)
            if index_end < 0:
                index_end = len(text)

        return result.replace('\t', '')

# typically parsing error 
class VexedError(Error):
    def __init__(self, pos_start, pos_end, details=''):
        super().__init__(pos_start, pos_end, 'Vexed', details)


# typically interpreting error 
class FlummoxedError(Error):
    def __init__(self, pos_start, pos_end, details, context):
        super().__init__(pos_start, pos_end, 'Flummoxed', details)
        self.context = context

    def as_string(self):
        result = f'\n{self.error_name}: {self.details}\n'
        result += '-----------------------------------------\n'
        result += self.generate_traceback()
        result += '\n' + \
            self.string_with_arrows(self.pos_start.ftxt,
                                    self.pos_start, self.pos_end)
        return result

    def generate_traceback(self):
        result = ''
        pos = self.pos_start
        context = self.context

        while context:
            result = f'problem in {bodgers.CURRENT_BODGER.name}, line {str(pos.line_number + 1)}:' + result
            pos = context.parent_entry_pos
            context = context.parent

        return "Lookin' back at wh't 'appened; " + result
