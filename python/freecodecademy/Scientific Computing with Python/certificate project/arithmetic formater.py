def arithmetic_arranger(problems, show_answers=False):
    if len(problems) > 5:
        return 'Error: Too many problems.'
    
    row1 = []
    row2 = []
    row3 = []
    row4 = []
    space = ' '*4

    for problem in problems:
        # Split the problem into operands using operators
        operands = problem.split('+') if '+' in problem else problem.split('-') if '-' in problem else None

        # Check if the operator is valid
        if operands is None:
            return "Error: Operator must be '+' or '-'."
        
        # Strip whitespace from operands
        operand1 = operands[0].strip()
        operand2 = operands[1].strip()

        # Check if operands are only made of digits
        if not operand1.isdigit() or not operand2.isdigit():
            return "Error: Numbers must only contain digits."
        
        if len(operand1) > 4 or len(operand2) > 4:
            return "Error: Numbers cannot be more than four digits."
        
        # Prepare the arranged strings
        addition = True if '+' in problem else False
        max_length = max(len(operand1), len(operand2))        

        # Arrange the first operand
        row1.append(' '*(max_length+2 - len(operand1)) + operand1)
        row2.append(('+' if addition else '-') + ' '*(max_length+1 - len(operand2)) + operand2)
        row3.append('-'*(max_length+2))
        
        result = str(int(operand1) + int(operand2) if addition else int(operand1) - int(operand2))
        row4.append((' '*(max_length+2 - len(result)) + result))

    arranged = space.join(row1) + '\n' + \
               space.join(row2) + '\n' + \
               space.join(row3)
    
    if show_answers:
        arranged += '\n' + space.join(row4)

    return arranged

print(f'\n{arithmetic_arranger(["3801 - 2", "123 + 49"])}')