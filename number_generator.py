def generate_number(prefix, qs, postfix='1', length=4):
    if qs.count() == 0:
        return prefix + postfix.zfill(length - 1)
    else:
        firstrecord = qs.first()
        postfix = str(int(firstrecord.roomnumber[1:]) + 1)
        return prefix + postfix.zfill(length - len(postfix))
        