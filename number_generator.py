from datetime import date


def generate_number(prefix, qs, postfix='1', length=4):
    if qs.count() == 0:
        return prefix + postfix.zfill(length - 1)
    else:
        firstrecord = qs.first()
        postfix = str(int(firstrecord.roomnumber[1:]) + 1)
        return prefix + postfix.zfill(length - len(postfix))


def generate_number_with_date(prefix, qs, postfix='1'):
    today = date.today()
    yy, mm, dd = str(today).split('-')
    if len(mm) == 1:
        mm = mm.zfill(2)
    if len(dd) == 1:
        dd = dd.zfill(2)
    if qs.count()==0:
        return prefix + yy + mm + dd + postfix.zfill(4)
    else:
        # TODO: work on it well
        firstrecord = qs.first()
        postfix = str(int(firstrecord.bookingnumber[7:]) + 1)
        return prefix + yy[2:] + mm + dd + postfix.zfill(3)
    
        