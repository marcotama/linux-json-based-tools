import re

print(re.match(r'([a-zA-Z0-9-_]+)', 'is-directory'))
print(re.match(r'(==|>=|>|<=|<|!=|=~)', '=='))
print(re.match(r'\d+(?:(?:K|M|G|T|P|E)?i?)|\d+\.\d+(?:(?:K|M|G|T|P|E)?i?)|\d+\.\d+e\d+|"[^"]+"|True|False', '1'))
