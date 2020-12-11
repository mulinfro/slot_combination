
def interval_cover(it, intervals):
    for itv in intervals:
        if it[1] <= itv[1] and it[1] >= itv[0]:
            return True
        if itv[1] <= it[1] and itv[1] >= it[0]:
            return True

    return False

def join_tuple(lst, idx):
    t = [e[idx] for e in lst]
    return "".join(t)
