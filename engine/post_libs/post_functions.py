
__all__ = ["join", "delete", "to_hans"]

def get_slot_val(para_item, slots, idx_slot_map):
    if para_item.tp == "VAR":
        return idx_slot_map[para_item.val]
    return para_item.val

"""
  join(seq, t1, t2, ...)
"""
def join(params, slots, idx_slot_map, context={}):
    if len(params) <= 1: return
    sep = get_slot_val(params[0], slots, idx_slot_map)
    vals = []
    for para_item in params[1:]:
        v = get_slot_val(para_item, slots, idx_slot_map)
        vals.append(v)
    return sep.join(vals)


def delete(params, slots, idx_slot_map, context={}):
    for para_item in params:
        if para_item.val in slots:
            slots.pop(para_item.val)


def to_hans(params, slots, idx_slot_map, context={}):
    trans_map = {"0":"零", "1":"一", "2":"二", "3":"三", "4":"四", "5":"五", "6":"六", "7":"七", "8":"八", "9":"九"}
    res = ""
    for para_item in params:
        v = get_slot_val(para_item, slots, idx_slot_map)
        nv = [trans_map.get(x, x) for x in v]
        res =  "".join(nv)
    return res
            

