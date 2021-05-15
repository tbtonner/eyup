import bodgers

#######################################
# SHELL
# where the user types their input
# determines multiline and when to send to tokeniser to start running of program
#######################################

####################################### multiline functions #######################################

def start_multiline(text): # should start multiline?
    word_list = text.split()

    if word_list == []:
        return False
    if word_list[-1] == "giz":
        return True
    if word_list[-1] == "gowon":
        return True
    if word_list[-1] == "while":
        return True
    if word_list[0] == "if" and (not word_list[-1] == "oer"):
        return True

    return False


def end_multiline(text): # should end multiline?
    word_list = text.split()
    if word_list == []:
        return False
    return True if word_list[-1] == "oer" else False


def new_statement(statement, depth): # new statement added to multiline
    tabs = '\t' * depth
    oer_count = 1
    while oer_count != 0:
        new_line = input(str(tabs + "> "))
        if start_multiline(new_line):
            nested_statement = new_statement(new_line, depth+1)
            statement += f'\n{nested_statement}'
            oer_count += 1
        else:
            if new_line != "":
                if new_line.split()[0] == 'if':
                    oer_count += 1
                statement += f'\n{new_line}'

        if end_multiline(statement):
            oer_count -= 1

    return statement

if __name__ == "__main__":
    ####################################### enter yorkshire first #######################################

    entered_yorkshire = False
    while entered_yorkshire == False:
        text = input("> ").strip(" ").lower()
        if text == "eyup":
            print("Enterin' Yorkshire v1.0 (areyt tyke!)")
            entered_yorkshire = True
        else:
            print("You need to enter Yorkshire first")

    ####################################### main read, eval, print loop #######################################

    inputs = []
    while True:
        try: # can't break system -> will just catch as an error
            inputs.append(input(f'{bodgers.CURRENT_BODGER.name}> '))
            if start_multiline(inputs[-1]):
                inputs[-1] = new_statement(inputs[-1], 1)
            if inputs[-1].strip() == "":
                continue

            # main run command
            result, error = bodgers.CURRENT_BODGER.run(inputs[-1])

            if error:
                print(error.as_string())
            elif result:
                if len(result.elements) == 1:
                    if result.elements[0] != None:
                        test = result.elements[0]
                        print(repr(result.elements[0]))
                else:
                    print(repr(result))

        except Exception as e:
            print("By heck! Y've crashed me!")
            print(f"Perplexed: {e}")
