import datetime

# strBirth=input('data di nascita gg-mm-yyyy: ')
# birth = datetime.datetime.strptime(strBirth, "%d-%m-%Y")
# adesso=datetime.datetime.now()
# age=adesso-birth
# 
# print('nascita:',birth)
# print('età:',round(age.days/365),'anni,',age.days%365,'giorni',age.seconds/(60*60),'ore')
# print('età in secondi:', age.total_seconds())



strBirth=input('data di nascita gg-mm-yyyy hh.mm: ')
birth = datetime.datetime.strptime(strBirth, "%d-%m-%Y %H.%M")
adesso=datetime.datetime.now()
age=adesso-birth

print('nascita:',birth)
print('età:',round(age.days/365),'anni,',age.days%365,'giorni',age.seconds/(60*60),'ore')
print('età in secondi:', age.total_seconds())
