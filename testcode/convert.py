#coding:utf-8
import xlwt

book = xlwt.Workbook(encoding='utf-8',style_compression=0)
sheet = book.add_sheet('mysheet',cell_overwrite_ok=True)

heads = ['账号','姓名','学工号','卡号','部门号','身份类型','性别']
for col,head in enumerate(heads):
     sheet.write(0,col,head)

with open('out.txt', encoding='utf-8') as file:
    lines = file.read().split('\n')
    for row, line in enumerate(lines):
        if len(line)==0 or  line[0]=='#':
            continue
        cols = line.split(',')
        for j,col in enumerate(cols):
            sheet.write(row,j,col)
        
#             f.write(cols[1]+','+cols[2]+','+cols[3]+','+cols[4]+','+cols[5]+','+cols[6]+','+cols[8]+'\n')

book.save('outcome.xlsx')     

# with open('out.csv','w', encoding='utf-8') as f:
#     f.write('账号,姓名,学工号,卡号，部门号，身份类型，性别\n')
#     with open('students.txt', encoding='utf-8') as file:
#         lines = file.read().split('\n')
#         for line in lines:
#             if len(line)==0 or  line[0]=='#':
#                 continue
#             cols = line.split(',')
#             for i in range(0,len(cols)):
#                 cols[i] = cols[i].strip()
            
#             f.write(cols[1]+','+cols[2]+','+cols[3]+','+cols[4]+','+cols[5]+','+cols[6]+','+cols[8]+'\n')
