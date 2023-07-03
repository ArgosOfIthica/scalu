This is old documentation and is no longer relevant.

Register Instructions:

	DUMP(variable):

		Prints out the contents of a variable in binary

	ADD(variable, variable):

		Adds two variables together with carry

	INC(variable):

		Increments a variable by one

	DEC(variable):

		Decrements a variable by one

	COPY(variable, variable):

		Copies the value of a variable to another

	BNEG(variable):

		Performs a bitwise negation

	BAND(variable, variable):

		Performs a bitwise and

	BOR(variable, variable):

		Performs a bitwise or

	ANEG(variable):

		Performs an arithmetic negation

	SUB(variable, variable):

		Performs subtraction on two variables

	ABS(variable):

		Computes the absolute value of a variable

	RAND(variable):

		Produces a random number between the minimum and maximum integer


Conditional Instructions:

	ZERO(variable):

		Executes true if the variable equals zero, otherwise false.

	EQUAL(variable, variable):

		Executes true if the variables have equivalent values, otherwise false.

	GTZ(variable, flag):

		Executes true if the variable is greater than zero, otherwise false  If the equality flag is true, this instruction will execute true if the variable is greater than or equal to zero, otherwise false.

	LTZ(variable, flag):

		Executes true if the variable is less than zero, otherwise false  If the equality flag is true, this instruction will execute true if the variable is less than or equal to zero, otherwise false.

	GT(variable, variable, flag):

		Executes true if the first variable is greater than the other, otherwise false. If the equality flag is true, this instruction will execute true if the variable is greater than or equal to zero, otherwise false.

	LT(variable, variable, flag):

		Executes true if the first variable is less than the other, otherwise false. If the equality flag is true, this instruction will execute true if the variable is less than or equal to zero, otherwise false.