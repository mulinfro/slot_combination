import util
from post_register import post_modules

def extract_slots(slot_indexes, idx_slot_map):
    if not slot_indexes:  return {}
    ex_slots = {}
    for slot_name, slot_body in slot_indexes.items():
        val = slot_body["val"]
        if slot_body["tp"] == "VAR":
            ex_slots[slot_name] = idx_slot_map[val]
        elif slot_body["tp"] in ["STRING", "NUM"]:
            ex_slots[slot_name] = val
        elif slot_body["tp"] == "FUNC":
            paras = slot_body["paras"]
            ex_slots[slot_name] = post_modules[val](paras, ex_slots, idx_slot_map)
        else:
            Error("Unexpected slot type %s"%slot_body["tp"])

    return ex_slots

def get_idx_slot(slices, perm, matched_frags):
    pre = 0
    idx_slot_map = {}
    matched_part = ""
    for i in range(len(slices)):
        slot_val = util.join_tuple(matched_frags[pre: pre + slices[i]], 0)
        matched_part += slot_val
        pre += slices[i]
        ni = perm[i] if perm else i + 1
        idx_slot_map[ni] = slot_val
    idx_slot_map[0] = matched_part
    return idx_slot_map

def apply_post(slot_indexes, pfunc, idx_slot_map, context = {}):
    slots = extract_slots(slot_indexes, idx_slot_map)
    for fname, params in pfunc.items():
        post_modules[fname](params, slots, idx_slot_map, context = context)
    return slots
