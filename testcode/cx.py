import cx_Oracle

conn = cx_Oracle.connect('photo_gxv/HjviU5ntxh192.168.40.30:1521/syntong')
curs = conn.cursor()
sqlstr = 'select pic ,SNO,NO from id_pic_all  where sno = \'1730792\''
curs.execute(sqlstr)

for result in curs:
    print(result)

curs.close()
conn.close()
