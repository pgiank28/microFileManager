import datetime
months = {
    '01': "Jan",
    '02': "Feb",
    '03': "Mar",
    '04': "Apr",
    '05': "May",
    '06': "Jun",
    '07': "Jul",
    '08': "Aug",
    '09': "Sep",
    '10': "Oct",
    '11': "Nov",
    '12': "Dec"
}
revMonths = {
    "Jan": '01',
    "Feb": '02',
    "Mar": '03',
    "Apr": '04',
    "May": '05',
    "Jun": '06',
    "Jul": '07',
    "Aug": '08',
    "Sep": '09',
    "Oct": '10',
    "Nov": '11',
    "Dec": '12'
}
def getPrivileges(num):
    priv = bin(num)
    humanPriv = [int(priv[-9:-6],2),int(priv[-6:-3],2),int(priv[-3:],2)]
    return humanPriv

def convertDate(date):
    tm = datetime.datetime.fromtimestamp(date)
    mon = tm.strftime("%m")
    year = tm.strftime("%Y")
    return months[mon]+" "+tm.strftime('%d')+"  "+year

def dateToLongFormat(date):
    x = date[-4:]+revMonths[date[0:3]]+date[4:6]
    return int(x)
