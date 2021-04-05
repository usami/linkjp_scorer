import json


def load_json(filename):
    with open(filename) as f:
        return [json.loads(line) for line in f.readlines()]


def generate_key(data, offset_type=None):
    if offset_type == 'text' or (offset_type is None and
                                 'text_offset' in data):
        return '{}:{}:text:{}'.format(data['attribute'],
                                      data['page_id'],
                                      offset_tuple(data['text_offset']))
    elif offset_type == 'html':
        return '{}:{}:html:{}'.format(data['attribute'],
                                      data['page_id'],
                                      offset_tuple(data['html_offset']))
    else:
        return None


def offset_tuple(offset):
    return (offset['start']['line_id'],
            offset['start']['offset'],
            offset['end']['offset'])


def link_annotation(data):
    if 'link_type' in data:
        return (data['link_page_id'],
                data['link_type']['later_name'],
                data['link_type']['part_of'],
                data['link_type']['derivation_of'])
    else:
        return (data['link_page_id'], False, False, False)