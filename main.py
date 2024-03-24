import sys
import copy

def lex(input):
	input = input.replace("(", " ( ")
	input = input.replace(")", " ) ")
	return input.split()


def categorize(token):
	try: result = float(token)
	except ValueError: result = token
	return result


def parse(tokens, ast = []):
	if not tokens:
		return ast.pop()
	token = tokens.pop(0)
	if token == "(":
		ast.append(parse(tokens, []))
		return parse(tokens, ast)
	elif token == ")":
		return ast
	else:
		ast.append(categorize(token))
		return parse(tokens, ast)

def evaluate_oper(op, rest):
	result = evaluate(rest.pop(0))
	while rest:
		match op:
			case "+": result += evaluate(rest.pop(0)) 
			case "-": result -= evaluate(rest.pop(0)) 
			case "*": result *= evaluate(rest.pop(0)) 
	return result


def evaluate_infix(op, rest):
	left = rest.pop(0)
	right = rest.pop(0)
	if rest: sys.exit("Too many operands for " + op + " " + str(rest))
	match op:
		case "/": return evaluate(left) / evaluate(right)
		case "%": return evaluate(left) % evaluate(right)
		case "<": return int(evaluate(left) < evaluate(right))
		case ">": return int(evaluate(left) > evaluate(right))
		case "<=": return int(evaluate(left) <= evaluate(right))
		case ">=": return int(evaluate(left) >= evaluate(right))
		case "==": return int(evaluate(left) == evaluate(right))
		case "!=": return int(evaluate(left) != evaluate(right))

context = {}


def evaluate(item):
	global context
	if type(item) is str:
		if item[0] == '"' and item[-1] == '"':
			return item[1 : -1]
		elif item in ["+", "-", "*", "/", "%", ">", "<", "<=", ">=", "==", "!=", "list", "eval", "if", "defvar", "print", "for"]:
			sys.exit("Invalid variable name " + str(item))
		elif item in context.keys():
			return context[item]
		else: sys.exit("Malformed item: " + item)
	elif type(item) is float: return item
	elif type(item) is list: 
		if item: op = item.pop(0)
		else: sys.exit("Can't evaluate empty list")
		if op in ["+", "-", "*"]:
			return evaluate_oper(op, item)
		elif op in ["/", "%", ">", "<", "<=", ">=", "==", "!="]:
			return evaluate_infix(op, item)
		elif op == "list":
			result = []
			while item:
				result.append(evaluate(item.pop(0)))
			return result
		elif op == "eval":
			result = []
			while item:
				result = evaluate(evaluate(item.pop(0)))
			return result
		elif op == "if":
			condition = evaluate(item.pop(0))
			consequence = evaluate(item.pop(0))
			alternative = evaluate(item.pop(0))
			if item: sys.exit("Too many operands for if " + str(item))
			if condition: return consequence
			else: return alternative
		elif op == "defvar":
			ident = item.pop(0)
			result = evaluate(item.pop(0))
			if item: sys.exit("Too many operands for defvar " + str(item))
			context[ident] = result
			return ident
		elif op == "print":
			result = evaluate(item.pop(0))
			if item: sys.exit("Too many operands for print " + str(item))
			print(result)
			return result
		elif op == "for":
			initial = item.pop(0)
			condition = item.pop(0)
			final = item.pop(0)
			body = item.pop(0)
			if item: sys.exit("Too many operands for for " + str(item))
			evaluate(initial)
			while evaluate(copy.deepcopy(condition)):
				result = evaluate(copy.deepcopy(body))
				evaluate(copy.deepcopy(final))
			return result
		elif op == "quote":
			result = item.pop(0)
			if item: sys.exit("Too many operands for quote " + str(item))
			return result
		else:
			sys.exit("Invalid operation: " + str(op))


while True:
	tokens = lex(input(">>> "))
	ast = parse(tokens)
	print(evaluate(ast))

