import src.compiler as compiler
import testing.test_bootstrap as testing

def scalu(mode, program):
	if mode == 'compile':
		comp = compiler.compiler()
		output = comp.compile(program)
		if __name__ == __main__:
			print(output)
		return output
	elif mode == 'test':
		testing.test()

if __name__ == "__main__":
	scalu('test', '')
