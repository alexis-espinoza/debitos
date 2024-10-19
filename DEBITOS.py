
import os
from os import getcwd, system
import json
import time

dictDebitos = {"1":'Recarga',"2":'Claro TV',"3":'Compras',"4":"Efectivo","5":"Otros", "6":"Alquiler", "7": "Abono"} #opciones cargadas por defecto

def leer_registros():
    with open(str(getcwd())+'/debitos.json','r') as archivo:
        data_json = json.load(archivo)       
    return data_json

def guardar_cambios(dicc_datos):
    with open(str(getcwd())+'/debitos.json','w') as archivo:
        json.dump(dicc_datos, archivo, indent=1, ensure_ascii=True)

def listar_deudores(data):
    deudores = data.keys()
    return dict(zip(list(range(1,len(deudores)+1)), deudores))

def agregar_debito():

    try:
        sigt = '0'
        deudor = ''
        while(sigt=='0'): 
           data_actual = leer_registros()
           dict_deudores = listar_deudores(data_actual)
           if(deudor==''):
               print('\n'+str(dict_deudores).replace(', ','\n').strip("{").strip("}"))
               deudor = input('Seleccione o agregue un nuevo deudor: ')
           print(str(dictDebitos).replace(', ','\n').strip("{").strip("}"))
           _descripcion = str(input("Selecione o agregue una descripión: "))
           descripcion = dictDebitos[_descripcion] if _descripcion in list(dictDebitos.keys()) else _descripcion
           monto = float(input('Digite el monto: '))
           monto = monto if descripcion != 'Abono' else monto*-1 #se agrega el negativo para restar los abonos
           _fecha = str(input('Digite la fecha dd/mm/aa [en blanco para fecha actual]: '))
           fecha = _fecha if _fecha!='' else str(time.strftime("%d/%m/%y"))

           try:
              if(int(deudor) in list(dict_deudores.keys())):
                 data_actual[dict_deudores[int(deudor)]].append({"descripcion": descripcion, "monto": monto, "fecha": fecha})
               
           except:
                 data_actual[deudor]=[{"descripcion": descripcion, "monto": monto, "fecha": fecha}]

           guardar_cambios(data_actual)
           system('clear')
           print('\n¡Registro agregado exitosamente!')
           sigt = input('\nDesea agregar otro débito [0 = si]: ')
           system('clear')
    except Exception:
      system('clear')
      print('\n¡No se pudo agregar el registro!')


def eliminar_deudas():
    try:
        system('clear')
        data_actual = leer_registros()
        dict_deudores = listar_deudores(data_actual)
        
        print('\n'+str(dict_deudores).replace(', ','\n').strip("{").strip("}"))
        opc_deudor = int(input('Seleccione: '))
        deudor = dict_deudores[opc_deudor]
        datos_de_deudas = data_actual[deudor]
        datos_por_deudor = debitos_deudor(datos_de_deudas,deudor)
        
        if(datos_por_deudor['datos']):
              print(datos_por_deudor['texto'])
        else:
             system('clear')
             print('\n¡Sin pendientes!')
             return
        flag_cambio=False
        codigo_deuda = input('\nOpciones de eliminado:\n#ID = registro según ID\n# 0 = todos los registros\n#<0 = todos los registro + deudor\nn,m = registros por rango\nSeleccione:  ')
        if(codigo_deuda.find(',')==1):
            rg = codigo_deuda.split(',')
            i = int(rg[0])-1 #el primer registo
            j = int(rg[1])   #el último registro
            system('clear')
            del data_actual[deudor][i:j]
            flag_cambio=True
            print('\n¡Se eliminaron los gastos según el rango indicado!')
        else:
           codigo_deuda = int(codigo_deuda)
           if(codigo_deuda<0):
              system('clear')
              del data_actual[deudor]
              flag_cambio=True
              print('\n¡Se eliminó el deudor y sus registros asociados!')

           elif(codigo_deuda==0):
              system('clear')
              del data_actual[deudor][:]
              flag_cambio=True
              print('\n¡Se eliminaron todos los préstamos del deudor!')
              
           elif(codigo_deuda>0 and codigo_deuda <= len(datos_de_deudas)):
              system('clear')
              del data_actual[deudor][codigo_deuda-1]
              flag_cambio=True
              print('\n¡Se el eliminó el dato del préstamo seleccionado!')
              
        if(flag_cambio==True):
              guardar_cambios(data_actual)
        else:
              system('clear')
              print('\n¡No se produjeron cambios!')
           
        eliminar_deudas() if input('\nDesea eliminar otro débito [0 = si]: ') == '0' else system('clear')
           
    except Exception:
      system('clear')
      print('\n¡No se pudo procesar el borrado!')

def filtrar_lista_de_deudas(filtro,arr_deudas):
    if(filtro!=''):
        if(filtro.find(',')!= -1): #flujo cuando se filtra por rango
            new_arr_deudas = []
            rg = filtro.split(',')
            i = int(rg[0])-1 #el primer registo
            j = int(rg[1])   #el último registro
            for reg in range(i,j):
                new_arr_deudas.append(arr_deudas[reg])
            return new_arr_deudas
        else:					#flujo cuando se filtra por palabra clave
            new_arr_deudas = []
            for registro in arr_deudas:
                if(registro['descripcion'].lower() == filtro.lower()):
                    new_arr_deudas.append(registro)
            return new_arr_deudas if len(new_arr_deudas)!=0 else arr_deudas
    else:
        return arr_deudas

def debitos_deudor(arr_deudas, deudor):
        system('clear')
        encabezado = '\nDetalle de:' if deudor[0] == '-' else 'Prestado a: '                  
        linea = encabezado + deudor.upper()
        linea += "\n\n\tID\tDESCT\t\tMONTO\t\tFECHA\n\n"
        id = 0
        total=0
        for registro in arr_deudas:
              id =id+1
              linea+=f'\t{id}'
              total+=registro["monto"]
              for campo in list(registro.keys()):
                 linea+= '\t'+str(registro[campo]).ljust(15)                         
              linea += '\n'
        linea+=f"\n\t{'-'*50}\n\tTOTAL: {total}"
        linea = linea + '\t\t¡CANCELADO!' if (total <=0 and id>0) else linea 
        return {'datos':True, 'texto':linea} if id>0 else {'datos': False}
    
def consultar_debito_por_deudor():

   try:
      data_actual = leer_registros()
      dict_deudores = listar_deudores(data_actual)
      print('\n'+str(dict_deudores).replace(', ','\n').strip("{").strip("}"))
      opc_deudor = int(input('Seleccione: '))
      filtro = input('Filtro o rango (n,m) para la búqueda[opcional]: ')#se usa para cuando hay que filtrar
      deudor = dict_deudores[opc_deudor]
      system('clear')
      datos_de_deudas = filtrar_lista_de_deudas(filtro,data_actual[deudor])
      datos_por_deudor = debitos_deudor(datos_de_deudas,deudor)
      
      if(datos_por_deudor['datos']):
          print(datos_por_deudor['texto'])

      else:
            print('\n¡Sin pendientes!')

   except Exception:
      system('clear')
      print('\n¡No se pudo consultar el registro!')

def consultar_total():

   try:
      data_actual = leer_registros()
      total_general=0
      system('clear')
      if(len(data_actual)>0):
            for key in data_actual.keys():
               print('\n')
               encabezado = 'Detalle de:' if key[0] == '-' else 'Prestado a: '                  
               print(encabezado, key.upper(),'\n')
               print("\tDESCT\t\tMONTO\t\tFECHA\n\n")
               total=0
               for registro in data_actual[key]:
                     linea=''
                     total+=registro["monto"]
                     for campo in list(registro.keys()):
                        linea+= '\t'+str(registro[campo]).ljust(15)
                     print(linea)
               total_general+=total
               print(f"\n\t{'-'*40}\n\tTOTAL: {total}")
            print(f"\n\t{'-'*40}\n\tTOTAL GENERAL: {total_general}\n\t{'-'*40}")
      else:
            system('clear')
            print('\n¡Sin pendientes!')

   except Exception:
      system('clear')
      print('\n¡No se pudo consultar el registro!')
      

def menu():
    try:
        while(True):
         
         #system('clear')
         opcion = int(input('\n1)-Agregar débito\n2)-Consultar débitos\n3)-Consultar total\n4)-Eliminar débitos\n5)-Salir\nSeleccione: '))
         if(opcion==1):
            system('clear')
            agregar_debito()

         elif(opcion==2):
            system('clear')            
            consultar_debito_por_deudor()

         elif(opcion==3):
            system('clear')
            consultar_total()

         elif(opcion==4):
            system('clear')
            eliminar_deudas()

         elif(opcion==5):
            system('clear')
            exit()
            
         else:
            system('clear')
            menu()
      
    except Exception:
      system('clear')
      print('\n¡Retornando al menú principal!')
      menu()
      
menu()
   

   


