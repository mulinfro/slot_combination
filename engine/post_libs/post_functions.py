
__all__ = ["join"]

def get_slot_val(para_item, slots, idx_slot_map):
    if para_item.tp == "VAR":
        return idx_slot_map[para_item.val]
    return para_item.val

"""
  join(seq, t1, t2, ...)
"""
def join(params, slots, idx_slot_map):
    if len(params) <= 1: return
    sep = get_slot_val(params[0], slots, idx_slot_map)
    vals = []
    for para_item in params[1:]:
        v = get_slot_val(para_item, slots, idx_slot_map)
        vals.append(v)
    return sep.join(vals)

