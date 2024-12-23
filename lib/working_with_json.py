import json
import os


def create_json_if_not_exists(path):
    # print('checking for ' + path)
    if not os.path.exists(path):
        with open(path, 'w') as f:
            json.dump({}, f)
            f.close()


def load_json(path):
    # print('loading ' + path)
    with open(path, 'r') as f:
        var_name = json.load(f)
        f.close()
        return var_name


def save_json(data, path):
    # print('saving ' + path)
    if '../' in path or '..\\' in path:
        raise Exception('Invalid file path')
    with open(path, 'w') as f:
        json.dump(data, f)
        f.close()
