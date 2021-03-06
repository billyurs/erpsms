import json
import simplejson
import ujson

JSONEncoder = json.JSONEncoder

def loads(json_str):
    try:
        return ujson.loads(json_str)
    except:
        return simplejson.loads(json_str)

def load(fp):
    try:
        return ujson.load(fp)
    except:
        return simplejson.load(fp)


def dumps(obj, cls=None):
    try:
        return json.dumps(obj, cls=cls)
    except:
        return simplejson.dumps(obj, cls=cls)

def dump(obj, fp):
    try:
        return ujson.dump(obj, fp)
    except:
        try:
            return json.dump(obj, fp)
        except:
            return simplejson.dump(obj, fp)

