
from frontend.parser.expect import recursive_descent

class parser():

	def parse(self, tokens):
		descent = recursive_descent(tokens)
		ast = descent.parse()

