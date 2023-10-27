week=['dom','lun','mar','mer','gio','ven','sab']
ottobre=(week*4)+week[0:3]
print(ottobre)

dict_ottobre={i+1: ottobre[i] for i in range(len(ottobre))}
# crea insieme di coppie (numero+1 : giorno) per tutti i numeri in [0,31)
print(dict_ottobre)
print(dict_ottobre[15])
