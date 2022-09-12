
import scalu.src.model.structure as model
import copy

def unwrap(global_object):
    temporary_vars = list()
    for sandbox in global_object.sandbox:
        for service in sandbox.services:
            sequence_out = list()
            for statement in service.sequence:
                new_sequencing = None
                unwrapped = unwrapped_element(temporary_vars)
                if model.is_assignment(statement):
                    new_sequencing = unwrapped.unwrap_assignment(statement)
                else:
                    new_sequencing = [statement]
                sequence_out = sequence_out + new_sequencing
            service.sequence = sequence_out
    return global_object

class unwrapped_element():

    def __init__(self, temporary_vars):
        self.instr_order = list()
        self.temps = temporary_vars
        self.var_counter = 0


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
        if self.var_counter < len(self.temps) :
            temp = self.temps[self.var_counter]
            self.var_counter += 1
            return temp
        else:
            temp = model.variable()
            temp.name = '_temp' + str(self.var_counter)
            self.temps.append(temp)
            self.var_counter += 1
            return temp

