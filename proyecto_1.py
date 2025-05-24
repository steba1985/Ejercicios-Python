"""aplicacion de gection de contactos.
crear una aplicacion de consola que permitira al usuario agregar, buscar, ver y eliminar contactos. 
cada contacto tendra: 
nombre
telefono
correo.
funcionalidad:
agregar un nuevo contacto
ver todos los contactos
buscar contacto por nombre
eliminar un contacto
salir de la aplicacion.

estructura:
funcion principal: iniciar la aplicacion y muestre el menu principal
funciones para cada operacion: agregar, ver, buscar y eliminar"""

# trabajar con diccionario


def menu_opciones():
    contacto={}
    indice=1
    valor=0
    while int(valor)<5:
        print("Sistema para Gestión de Contactos:")
        print("1-. Agregar un Contacto")
        print("2-. Ver Contactos existentes")
        print("3-. Buscar un Contacto")
        print("4-. Eliminar un Contacto")
        print("5-. Salir")
        valor = input("Ingrese una Opción: ")
        if int(valor) == 1:
            nombre=(input("Ingresa el Nombre del Contacto: "))
            telefono=(input("Ingresa Teléfono de Contacto: "))
            correo=(input("Ingrese Correo del Contacto: "))
            add_contacto(nombre,telefono,correo,contacto,indice)
            indice=indice+1
        elif int(valor) == 2:
            ver_contacto(contacto)
        elif int(valor) == 3:
            busca=input("Ingresa el Nombre del Contacto a Buscar:")
            buscar_contacto(busca, contacto)
        elif int(valor) == 4:
            busca=input("Ingresa el Nombre del Contacto a Eliminar:")
            del_contacto(busca,contacto)
        elif int(valor) > 4:
            print("Gracias por usar el Sistema.")
    
def add_contacto(nombre,telefono,correo,contacto,indice):
    print(indice)
    contacto[indice]=[nombre,telefono,correo]
    print("Contacto Agregado.... Regresando al Menu Principal.")


def ver_contacto(contacto):
    y=0
    for x in contacto:
        y=y+1
        print("Contacto {}-. Nombre: {}, Telefono: {}, Correo: {}".format(y,(contacto[x][0]),(contacto[x][1]),(contacto[x][2])))
    print("Contactos Mostrados.... Regresando al Menu Principal.")

def buscar_contacto(busca, contacto):
    
    cantidad=0
    for x in contacto:
        if contacto[x][0]==busca:
            cantidad=cantidad + 1
            print("-. Nombre: {}, Telefono: {}, Correo: {}".format((contacto[x][0]),(contacto[x][1]),(contacto[x][2])))
    if cantidad>0:
        print("Se mostraron {} Contactos con el Nombre {}".format(cantidad, busca))
    else:
        print("No Existen Contactos Guardados con el Nombre {}".format(busca))
    print("Contacto Buscado.... Regresando al Menu Principal.")

def del_contacto(busca, contacto):
    cantidad=0
    borrar=[]
    valor=0
    for x in contacto:
        valor=valor+1
        if contacto[x][0]==busca:
            borrar.append(valor)
            cantidad=cantidad+1
            print("-. Nombre: {}, Telefono: {}, Correo: {}".format((contacto[x][0]),(contacto[x][1]),(contacto[x][2])))
    if cantidad>0:
        borrar.sort(reverse=True)
        for borrado in borrar:
            contacto.pop(borrado)
        print("Se Eliminaron {} Contactos con el Nombre {}".format(cantidad, busca))
    else:
        print("No Existen Contactos Guardados con el Nombre {}".format(busca))
    print("Contacto(s) Eliminado(s).... Regresando al Menu Principal.")

menu_opciones()