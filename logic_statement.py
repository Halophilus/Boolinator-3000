import random, re

def random_logical_expression():
    '''
        Function: generates a mathematical statement of a max parenthetical depth of three with a string length < 16
            Helper function: generate_expression(d), takes a value for depth and recursively generates a string representing a logical statement at each level of depth
        Args:
            None
        Returns:
            Mathematical statement string to be printed / evaluated
    '''
    variables = ['X', 'Y', 'Z']
    binary_operators = ['&', '|', '^']
    unary_operators = ['!', '']
    try:
        def generate_expression(d):
            if d == 0:
                return random.choice(unary_operators) + random.choice(variables)
            else:
                expr_type = random.choice(['binary', 'unary'])
                if expr_type == 'binary':
                    return '(' + generate_expression(d-1) + random.choice(binary_operators) + generate_expression(d-1) + ')'
                else:
                    return random.choice(unary_operators) + generate_expression(d-1)

        expr = generate_expression(3)
        while len(expr) > 16: # Imposes char limit
            expr = generate_expression(3)
        return expr
    except Exception as ex:
        print(f"Error in random_logical_expression: {ex}")

def evaluate_logical_expression(expr, X, Y, Z):
    '''
        Function: evaluate_logical_expression, determines the overall truth value of a string representing a logical statement
        Args:
            expr (str), a mathematical statement 
            X, Y, Z (bool), truth values for Boolean variables in statement
        Returns:
            Tries to evaluate logical expression, returns overall truth value if successful, otherwise returns None
    '''
    # Convert human readable logical operators into ones that can be parsed by Python
    expr = expr.replace('&', ' and ').replace('|', ' or ').replace('!', ' not ').replace('^', ' ^ ')
    # print(expr)
    # Enclose 'not' operations in parentheses, handling repeated 'not's
    # Match 'not' followed by either a variable, another 'not', or a '('
    expr = re.sub(r'(\bnot\b\s+)(?=\b[XZY]\b|\bnot\b|\()', r'(not ', expr)
    # print(expr)
    # Add closing parentheses for all opened 'not' parentheses
    open_parens = expr.count('(not')
    expr += ')' * open_parens
    print(f"EVALUATED STATEMENT: {expr}")
    
    try:
        return eval(expr, {"__builtins__": None}, {"X": X, "Y": Y, "Z": Z})
    except Exception as ex:
        print(f"Error evaluating expression: {ex}")
        return None

def random_bools():
    '''
    Generates three random booleans
    '''
    X, Y, Z = (random.choice([True, False]) for bools in range(3))
    return X, Y, Z

if __name__ == '__main__':
    expr = random_logical_expression()
    print("Generated Expression:", expr)
    X, Y, Z = random_bools()
    print(X, Y, Z)
    truth_value = evaluate_logical_expression(expr, X, Y, Z)
    print("Evaluated to:", truth_value)

