
import re
import math
import scalu.src.model.universe as universe

def minify(cfg_string, uni):
    blob = alias_blob(uni)
    blob.alias_tuples = to_tuple_list(cfg_string)
    root_computation = blob.alias_convert[blob.alias_tuples[0][0]]
    output_text = minify_names(blob) + root_computation
    output_text = clean_output(output_text)
    output_text = reallocate(output_text, blob)
    output_text = clean_output(output_text)
    output_text = deduplicate(output_text)
    output_text = write_once_reduction(output_text)
    output_text = clean_output(output_text)
    return output_text

def clean_output(output_text):
    output_text = re.sub(';(\s*)\"', '"', output_text)
    output_text = re.sub('\";', '"', output_text)
    output_text = re.sub('\n{2,}', '\n', output_text)
    output_text = re.sub(';{2,}', ';', output_text)
    output_text = re.sub('\";', '"', output_text)
    return output_text

def minify_names(blob):
    HEAD = 0
    TAIL = 1
    output_text = ''
    for alias in blob.alias_tuples:
        new_head = blob.alias_convert[alias[HEAD]]
        new_tail = minify_payload(alias[TAIL], blob)
        output_text += 'alias ' + new_head + ' "' + new_tail + '"\n'
    return output_text


def minify_payload(tail, blob):
    split_value = split_tail_word(tail)
    updated_value = [ minify_word(word, blob.alias_convert) for word in split_value]
    updated_value = ''.join(updated_value)
    return updated_value

def split_tail_word(tail):
    split_tail = re.split('(\W)', tail)
    for token in range(len(split_tail)):
        if split_tail[token] == '%':
            split_tail[token] = ''
            split_tail[token + 1] = '%' + split_tail[token + 1]
    return split_tail


def reallocate(output_text, blob):
    split_lines = re.split('\n', output_text)
    line = 0
    while True:
        if len(split_lines[line]) > blob.CONSOLE_MAX_BUFFER:
            replacement = compute_reallocation(split_lines[line], blob)
            split_lines = split_lines[:line] + replacement + split_lines[line + 1:]
        line += 1
        if line == len(split_lines):
            break
    new_output = '\n'.join(split_lines)
    return new_output



def compute_reallocation(text, blob):
    command_split = re.split(';', text)
    line_count = math.ceil(len(text) / blob.CONSOLE_MAX_BUFFER) + 1
    new_aliases = blob.pick.new_alias_list(line_count)
    lines = [''] * line_count
    command = 0
    for line in range(len(lines)):
        if line > 0 and command < len(command_split):
            lines[line] = 'alias ' + new_aliases[line - 1] + ' "'
        while(command < len(command_split)):
            test_line = lines[line] + command_split[command] + ';' + new_aliases[line]
            if len(test_line) < blob.CONSOLE_MAX_BUFFER:
                lines[line] = lines[line] + command_split[command] + ';'
                command += 1
            else:
                lines[line] = lines[line] + new_aliases[line] + '"'
                break
    return lines


def to_tuple_list(cfg_string):
    return list(re.findall('alias\s(\S+)\s\"(.*)\"', cfg_string))

def minify_word(word, alias_convert):
    if word in alias_convert:
        return alias_convert[word]
    else:
        return word

def replace_words(replacement_map, cfg):
    words = list()
    split_cfg = split_tail_word(cfg)
    for word in split_cfg:
        if word in replacement_map:
            words.append(replacement_map[word])
        else:
            words.append(word)
    words = ''.join(words)
    line_split = re.split('\n', words)
    purged_split = list()
    for split in line_split:
        element_list = to_tuple_list(split)
        if len(element_list) == 0 or (element_list[0][0] != element_list[0][1]):
            purged_split.append(split)
    line_split = list(dict.fromkeys(purged_split))
    return '\n'.join(line_split)


def deduplicate(cfg):
    count = 0
    running = True
    while count < 500:
        count += 1
        new_cfg = deduplicate_instance(cfg)
        if len(new_cfg) == len(cfg):
            return cfg
        cfg = new_cfg
    return cfg

def deduplicate_instance(cfg):
    HEAD = 0
    TAIL = 1
    tuple_list = to_tuple_list(cfg)
    unique_tails = dict()
    head_map = dict()
    for ele in tuple_list:
        if ele[TAIL] not in unique_tails:
            unique_tails[ele[TAIL]] = ele[HEAD]
        else:
            head_map[ele[HEAD]] = unique_tails[ele[TAIL]]
    new_cfg = replace_words(head_map, cfg)
    tuple_list = to_tuple_list(new_cfg)
    replacement_map = dict()
    for ele in tuple_list:
        if re.match('^%\w*$', ele[TAIL]) and re.match('^%\w*$', ele[HEAD]):
            replacement_map[ele[HEAD]] = ele[TAIL]
    new_cfg = replace_words(replacement_map, new_cfg)
    return new_cfg


def write_once_reduction(cfg):
    all_vars = re.findall('(%[a-z0-9]*)', cfg)
    unique_vars = list(set(all_vars))
    for var in unique_vars:
        outer_assignments = re.findall('(alias ' + var + ' \")', cfg)
        if len(outer_assignments) > 0:
            continue
        assignments = re.findall('alias '+ var + ' (%[a-z0-9]*)', cfg)
        if len(assignments) == 1:
            cfg = re.sub('alias ' + var + ' ' + assignments[0], '', cfg)
            cfg = re.sub(';' + var + '\"', ';'+assignments[0]+'"', cfg)
            cfg = re.sub(';' + var + ';', ';'+assignments[0]+';', cfg)
    return cfg

class alias_blob():

    def __init__(self, uni):
        self.CONSOLE_MAX_BUFFER = 510 #determined by engine
        self.alias_tuples = tuple()
        self.alias_convert = dict()
        self.pick = uni.picker.reset()
        if uni is not None:
            for alias in uni.known_aliases:
                if alias.type == 'event':
                    self.alias_convert[alias.identity] = alias.string
                else:
                    self.alias_convert[alias.identity] = self.pick.new_alias()
