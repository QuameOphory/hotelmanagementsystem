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
    datepart = ''.join(str(today).split('-'))
    if qs.count()==0:
        numberstring = prefix + datepart + postfix.zfill(6)
        return numberstring
    else:
        firstrecord = qs.first()
        roomnumber, new_roomnumber = firstrecord.bookingnumber[7:], str(int(firstrecord.bookingnumber[7:]) + 1)
        postfix = new_roomnumber.zfill(len(new_roomnumber) + (len(roomnumber) - len(new_roomnumber)))
        numberstring = prefix + datepart + postfix
        return numberstring




        
        return prefix + yy[2:] + mm + dd + postfix.zfill(3)
    
        