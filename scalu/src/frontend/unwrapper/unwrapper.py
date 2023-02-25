
import scalu.src.model.structure as model
import copy

def unwrap(global_object):
    temporary_vars = list()
    for sandbox in global_object.sandbox:
        for service in sandbox.services:
            sequence_out = list()
            for statement in service.sequence:
                for var in temporary_vars:
                    var.used = False
                new_sequencing = None
                unwrapped = unwrapped_element(temporary_vars, sandbox.min_word_size)
                if model.is_assignment(statement):
                    new_sequencing = unwrapped.unwrap_assignment(statement)
                else:
                    new_sequencing = [statement]
                sequence_out = sequence_out + new_sequencing
            service.sequence = sequence_out
    return global_object

class unwrapped_element():

    def __init__(self, temporary_vars, word_size):
        self.instr_order = list()
        self.temps = temporary_vars
        self.word_size = word_size

    def unwrap_assignment(self, assignment):
        if model.is_variable(assignment.arg[0]):
            icopy = model.unary_operator()
            icopy.identity = 'copy'
            icopy.arg[0] = assignment.arg[0]
            icopy.output = assignment.identifier
            self.instr_order.append(icopy)
        else:
            self.unwrap(assignment.arg[0], assignment.identifier)
        return self.instr_order

    def unwrap(self, item, output_variable):
        item.output = output_variable
        item.arg = [self.unwrap_transform(arg, output_variable) for arg in item.arg]
        self.instr_order.append(item)

    def unwrap_transform(self, item, output_variable):
        if not model.is_variable(item):
            new_output_variable = self.generate_temporary_variable()
            self.unwrap(item, new_output_variable)
            return new_output_variable
        else:
            return item

    def generate_temporary_variable(self):
        for temp in self.temps:
            if (temp.word_size == self.word_size) and not temp.used:
                temp.used = True
                return temp
        temp = model.variable()
        temp.name = '_temp' + str(len(self.temps))
        temp.word_size = self.word_size
        temp.used = True
        self.temps.append(temp)
        return temp