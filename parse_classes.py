PRIVATE_PREFIX = '$_'
REFERENCE_PREFIX = 'ref_'
INHERIT_KEYWORD = 'Inherits'

def clean_prefix(root):
    for key, value in root.items():
        if(key.startswith(PRIVATE_PREFIX)):
            del root[key]
            key = key[len(PRIVATE_PREFIX):]
            root[key] = value
        if(type(value) is dict):
            clean_prefix(value)
        if(type(value) is list):
            for list_val in value:
                if(type(list_val) is dict):
                    clean_prefix(list_val)


def parse(tree_root):
    #Contains the result of parsing
    output = {}
    #Cache used for already solved classes
    cache = {}
    tree_root = tree_root["classes"]
    for class_key in tree_root:
        output[class_key] = dict(solve_class(cache, tree_root[class_key], class_key, tree_root))
    clean_prefix(output)
    return output


def solve_inheritance(cache, parents, root):
    output = {}
    for class_key in parents:
        solved_class = {}
        if(class_key in cache):
            solved_class = cache[class_key]
        else:
            solved_class = solve_class(cache, root[class_key], class_key, root)
        for prop_key, prop_value in solved_class.items():
            if(not prop_key.startswith(PRIVATE_PREFIX)):
                output[prop_key] = prop_value
    return output


def solve_list(cache, list_def, root):
    output = []
    for value in list_def:
        output.append(solve_value(cache, value, root))
    return output


def solve_dict(cache, dict_def, root):
    output = {}
    for key, value in dict_def.items():
        output[key] = solve_value(cache, value, root)
    return output


def solve_str(cache, str_def, root):
    if(str_def.startswith(REFERENCE_PREFIX)):
        class_name = str_def[len(REFERENCE_PREFIX):]
        if(class_name in cache):
            return cache[class_name]
        return solve_class(cache, root[class_name], class_name, root)
    else:
        return str_def


def solve_value(cache, value, root):
    if(type(value) is int or type(value) is float):
        return value
    if(type(value) is list):
        return solve_list(cache, value, root)
    if(type(value) is dict):
        return solve_dict(cache, value, root)
    if(type(value) is str):
        return solve_str(cache, value, root)
    # We shouldn't reach this point, unsopported stuff here
    raise Exception("Invalid type encountered while solving value " + str(value))


def solve_class(cache, class_def, class_key, root):
    output = {}
    if(class_key in cache):
        return cache[class_key]
    #Inheritance MUST be solved first (otherwise wonky shit happens)
    if(INHERIT_KEYWORD in class_def):
        new_props = solve_inheritance(cache, class_def[INHERIT_KEYWORD], root)
        output = {**output, **new_props}
    for prop_key, prop_value in class_def.items():
        if(prop_key == INHERIT_KEYWORD):
            continue
        output[prop_key] = solve_value(cache, prop_value, root)
    cache[class_key] = output
    return output

