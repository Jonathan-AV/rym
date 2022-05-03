from conexion_bd import obtener_conexion

def insertar_cliente(nombre, apPaterno, apMaterno, tel, correo,contra,img_perfil):
    conexion = obtener_conexion()
    if img_perfil == "" or img_perfil == None:
        with conexion.cursor() as cursor:
            cursor.execute("INSERT INTO cliente(nombre,ape_paterno,ape_materno,telefono,correo,contraseña) VALUES (%s,%s,%s,%s,%s,%s)",
            (nombre,apPaterno,apMaterno,tel,correo,contra))
    else:    
        with conexion.cursor() as cursor:
            cursor.execute("INSERT INTO cliente(nombre,ape_paterno,ape_materno,telefono,correo,contraseña,img_perfil) VALUES (%s,%s,%s,%s,%s,%s,%s)",
            (nombre,apPaterno,apMaterno,tel,correo,contra,img_perfil))
    conexion.commit()
    conexion.close()

def obtener_cuentaC(correo):
    conexion = obtener_conexion()
    cliente = ()
    with conexion.cursor() as cursor:
        cursor.execute('SELECT id_cliente,contraseña FROM cliente WHERE correo = %s',
        (correo))
        cliente = cursor.fetchone()
    conexion.close()
    return cliente

def insertar_proveedor(nombre,apPaterno,apMaterno,ofigiro,dir,tel,correo,contra):
    conexion = obtener_conexion()
    if dir == "" or dir == None:
        with conexion.cursor() as cursor:
            cursor.execute('INSERT INTO proveedor(nombre,ape_paterno,ape_materno,telefono,correo,oficio_giro,contraseña) VALUES (%s,%s,%s,%s,%s,%s,%s)',
            (nombre,apPaterno,apMaterno,tel,correo,ofigiro,contra))
    else:    
        with conexion.cursor() as cursor:
            cursor.execute('INSERT INTO proveedor(nombre,ape_paterno,ape_materno,telefono,correo,oficio_giro,dir_negocio,contraseña) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)',
            (nombre,apPaterno,apMaterno,tel,correo,ofigiro,dir,contra))
    conexion.commit()
    conexion.close()

def obtener_cuentaP(correo):
    conexion = obtener_conexion()
    proveedor = ()
    with conexion.cursor() as cursor:
        cursor.execute('SELECT id_proveedor,contraseña nombre FROM proveedor WHERE correo = %s',(correo))
        proveedor = cursor.fetchone()
    conexion.close()
    return proveedor

def obtener_info_proveedor(id_proveedor):
    conexion = obtener_conexion()
    infoP = ()
    with conexion.cursor() as cursor:
        cursor.execute('SELECT nombre,ape_paterno,ape_materno,telefono,oficio_giro,' +
        'dir_negocio FROM proveedor WHERE id_proveedor = %s',(id_proveedor))
        infoP = cursor.fetchone()
    conexion.close()
    return infoP

def obtener_info_cliente(id_cliente):
    conexion = obtener_conexion()
    infoC = ()
    with conexion.cursor() as cursor:
        cursor.execute('SELECT nombre,ape_paterno,ape_materno,telefono,'+
        'img_perfil FROM cliente WHERE id_cliente = %s',(id_cliente))
        infoC = cursor.fetchone()
    conexion.close()
    return infoC

def registrar_servicio(id_proveedor, nomServicio, desc,tipoServicio):
    conexion = obtener_conexion()
    id_servicio =()
    with conexion.cursor() as cursor:
        cursor.execute('INSERT INTO servicio (id_proveedor,nom_titulo,descripcion,tipo_servicio) VALUES'+
        ' (%s,%s,%s,%s)', (id_proveedor,nomServicio,desc,tipoServicio))
    conexion.commit()
    conexion.close()

def registrar_img_servicio(id_proveedor,nomServicio,imgs):
    conexion = obtener_conexion()
    id_servicio = ()
    with conexion.cursor() as cursor:
        cursor.execute('SELECT id_servicio FROM servicio WHERE id_proveedor = %s AND nom_titulo'+
        ' = %s', (id_proveedor,nomServicio))
        id_servicio = cursor.fetchone()
    with conexion.cursor() as cursor:
        for img in imgs:
            cursor.execute('INSERT INTO img_servicio (id_servicio,img_servicio)'+
            ' VALUES (%s,%s)', (id_servicio, img))
    conexion.commit()
    conexion.close()

def obtener_mis_servicios(id_proveedor):
    conexion = obtener_conexion()
    misServicios = ()
    with conexion.cursor() as cursor:
        cursor.execute('SELECT id_servicio, nom_titulo, descripcion FROM servicio WHERE id_proveedor = %s',(id_proveedor))
        misServicios = cursor.fetchall()
    conexion.close()
    return misServicios    

def obtener_mi_servicio(id_servicio):
    conexion = obtener_conexion()
    miServicio = ()
    with conexion.cursor() as cursor:
        cursor.execute('SELECT nom_titulo,descripcion FROM servicio WHERE id_servicio = %s',(id_servicio))
        miServicio = cursor.fetchone()
    conexion.close()
    return miServicio

def eliminar_servicio(id_servicio):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute('DELETE FROM servicio WHERE id_servicio = %s',(id_servicio))
    conexion.commit()
    conexion.close()

def eliminar_img_servicio(id_img):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute('DELETE FROM img_servicio WHERE id_img = %s',(id_img))
    conexion.commit()
    conexion.close()    

def agregar_imgs_servicio(id_servicio,imgs):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        for img in imgs:
            cursor.execute('INSERT INTO img_servicio (id_servicio,img_servicio)'+
            ' VALUES (%s,%s)', (id_servicio, img))
    conexion.commit()
    conexion.close()
    
def obtener_img_servicio(id_img):
    conexion = obtener_conexion()
    img = ()
    with conexion.cursor() as cursor:
        cursor.execute('SELECT img_servicio FROM img_servicio WHERE id_img = %s',(id_img))
        img = cursor.fetchone()
    conexion.close()
    return img

def obtener_imgs_servicio(id_servicio):
    conexion = obtener_conexion()
    imgs = ()
    with conexion.cursor() as cursor:
        cursor.execute('SELECT img_servicio FROM img_servicio WHERE id_servicio = %s',(id_servicio))
        imgs = cursor.fetchall()
    conexion.close()
    return imgs

def obtener_imgs_mi_servicio(id_servicio):
    conexion = obtener_conexion()
    imgs = ()
    with conexion.cursor() as cursor:
        cursor.execute('SELECT id_img,img_servicio FROM img_servicio WHERE id_servicio = %s',(id_servicio))
        imgs = cursor.fetchall()
    conexion.close()
    return imgs

def modificar_info_servicio(id_servicio,nomServicio,desc):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute('UPDATE servicio SET nom_titulo = %s,descripcion = %s WHERE id_servicio = %s',
        (nomServicio,desc,id_servicio))
    conexion.commit()
    conexion.close()

def obtener_servicios():
    conexion = obtener_conexion()
    servicios = ()
    with conexion.cursor() as cursor:
        cursor.execute('SELECT tipo_servicio FROM servicio GROUP BY (tipo_servicio)')
        servicios = cursor.fetchall()
    conexion.close()
    return servicios

def obtener_serv_por_tipoSer(tipoServicio):
    conexion = obtener_conexion()
    servicios = ()
    with conexion.cursor() as cursor:
        cursor.execute('SELECT proveedor.nombre,proveedor.ape_paterno,proveedor.ape_materno,'+
        'servicio.nom_titulo,servicio.descripcion,servicio.calificacion,servicio.id_servicio FROM servicio INNER JOIN proveedor ON '+
        'servicio.id_proveedor = proveedor.id_proveedor WHERE tipo_servicio = %s',
        (tipoServicio))
        servicios = cursor.fetchall()
    conexion.close()
    return servicios

def obtener_conversacionesP(id_proveedor):
    conexion = obtener_conexion()
    conversaciones = ()
    with conexion.cursor() as cursor:
        cursor.execute('SELECT conversacion.id_conversacion,conversacion.id_cliente,cliente.nombre' +
        ',cliente.ape_paterno,cliente.ape_materno,cliente.img_perfil'+
        ',(SELECT mensaje.mensaje FROM mensaje WHERE mensaje.id_conversacion=conversacion.id_conversacion ORDER BY fecha DESC LIMIT 1) AS "ultimo_mensaje",'+
        '(SELECT mensaje.fecha FROM mensaje WHERE mensaje.id_conversacion=conversacion.id_conversacion ORDER BY fecha DESC LIMIT 1) AS "fecha"'+
        ' FROM conversacion INNER JOIN cliente ON cliente.id_cliente = '+
        'conversacion.id_cliente WHERE conversacion.id_proveedor = %s', (id_proveedor))
        conversaciones = cursor.fetchall()
    conexion.close()
    return conversaciones

def modificar_infoP_p(id_proveedor,nombre,apPaterno,apMaterno,ofigiro,dir,tel):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        if dir:
            cursor.execute('UPDATE proveedor SET nombre = %s,ape_paterno = %s,ape_materno = %s,telefono = %s'+
            ',oficio_giro = %s,dir_negocio = %s WHERE id_proveedor = %s', (nombre,apPaterno,apMaterno,tel,
            ofigiro,dir,id_proveedor))
        else:
            cursor.execute('UPDATE proveedor SET nombre = %s,ape_paterno = %s,ape_materno = %s,telefono = %s'+
            ',oficio_giro = %s WHERE id_proveedor = %s',(nombre,apPaterno,apMaterno,tel,ofigiro,id_proveedor))    
    conexion.commit()
    conexion.close()

def modificar_contra_p(id_proveedor,contra):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute('UPDATE proveedor SET contraseña = %s WHERE id_proveedor = %s',(contra,id_proveedor))
    conexion.commit()
    conexion.close()

def modificar_infoP_c(id_cliente,nombre,apPaterno,apMaterno,telefono):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute('UPDATE cliente SET nombre = %s,ape_paterno = %s,ape_materno = %s,'+
        'telefono = %s WHERE id_cliente = %s',(nombre,apPaterno,apMaterno,telefono,id_cliente))
    conexion.commit()
    conexion.close()

def modificar_contra_c(id_cliente,contra):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute('UPDATE cliente SET contraseña = %s WHERE id_cliente = %s', (contra,id_cliente))
    conexion.commit()
    conexion.close()

def obtener_img_perfil(id_cliente):
    conexion = obtener_conexion()
    img_perfil = ()
    with conexion.cursor() as cursor:
        cursor.execute('SELECT img_perfil FROM cliente WHERE id_cliente = %s',(id_cliente))
        img_perfil = cursor.fetchone()
    conexion.close()
    return img_perfil

def modificar_img_perfil(id_cliente,img):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute('UPDATE cliente SET img_perfil = %s WHERE id_cliente = %s',(img,id_cliente))
    conexion.commit()
    conexion.close()

def registrar_cali(id_servicio,id_cliente,califi):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.callproc('calificar',(id_servicio,id_cliente,califi))
    conexion.commit()
    conexion.close()    

def obtener_nomProveedor_por_id_servicio(id_servicio):
    conexion = obtener_conexion()
    proveedor = ()
    with conexion.cursor() as cursor:
        cursor.execute('SELECT nombre,ape_paterno,ape_materno FROM proveedor INNER JOIN servicio ON '+
        'servicio.id_proveedor=proveedor.id_proveedor WHERE id_servicio = %s',(id_servicio))
        proveedor = cursor.fetchone()
    conexion.close()
    return proveedor

def obtener_infoProveedor_por_id_servicio(id_servicio):
    conexion = obtener_conexion()
    info = ()
    with conexion.cursor() as cursor:
        cursor.execute('SELECT proveedor.nombre,proveedor.ape_paterno,proveedor.ape_materno,'+
        'proveedor.telefono,proveedor.correo,proveedor.dir_negocio,servicio.nom_titulo FROM proveedor INNER JOIN servicio ON'+
        ' proveedor.id_proveedor = servicio.id_proveedor WHERE id_servicio = %s',(id_servicio))
        info = cursor.fetchone()
    conexion.close()
    return info

def obtener_correoC(id_cliente):
    conexion = obtener_conexion()
    correo = ()
    with conexion.cursor() as cursor:
        cursor.execute('SELECT correo FROM cliente WHERE id_cliente = %s',(id_cliente))
        correo = cursor.fetchone()
    conexion.close()
    return correo

def obtener_infoCliente_solicitud(id_cliente):
    conexion = obtener_conexion()
    info = ()
    with conexion.cursor() as cursor:
        cursor.execute('SELECT nombre,ape_paterno,ape_materno,correo,telefono FROM'+
        ' cliente WHERE id_cliente = %s',(id_cliente))
        info = cursor.fetchone()
    conexion.close()
    return info

def obtener_infoProveedor_solicitud(id_servicio):
    conexion = obtener_conexion()
    info = ()
    with conexion.cursor() as cursor:
        cursor.execute('SELECT proveedor.correo,servicio.nom_titulo FROM proveedor'+
        ' INNER JOIN servicio ON proveedor.id_proveedor=servicio.id_proveedor WHERE servicio.id_servicio = %s',
        (id_servicio))
        info = cursor.fetchone()
    conexion.close()
    return info

def obtener_idProveedor_por_idServicio(id_servicio):
    conexion = obtener_conexion()
    info = ()
    with conexion.cursor() as cursor:
        cursor.execute('SELECT proveedor.id_proveedor FROM proveedor INNER JOIN servicio'+
        ' ON proveedor.id_proveedor=servicio.id_proveedor WHERE id_servicio = %s',
        (id_servicio))
        info = cursor.fetchone()
    conexion.close()
    return info    

def registrar_comentario(id_cliente,id_servicio,comentario):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute('INSERT INTO comentario (id_servicio,id_cliente,comentario) VALUES (%s,%s,%s)',
        (id_servicio,id_cliente,comentario))
    conexion.commit()
    conexion.close()

def obtener_comentarios(id_servicio):
    conexion = obtener_conexion()
    comentarios = ()
    with conexion.cursor() as cursor:
        cursor.execute('SELECT comentario.comentario,comentario.fecha,'+
        'cliente.nombre,cliente.ape_paterno,cliente.ape_materno,'+
        'cliente.img_perfil FROM comentario INNER JOIN cliente ON '+
        'comentario.id_cliente = cliente.id_cliente WHERE id_servicio = %s',
        (id_servicio))
        comentarios = cursor.fetchall()
    conexion.close()
    return comentarios

def crear_conversacion(id_cliente,id_proveedor):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute('INSERT INTO conversacion (id_cliente,id_proveedor)'+
        ' VALUES (%s,%s)',(id_cliente,id_proveedor))
    conexion.commit()
    conexion.close()

def obtener_conversacion(id_cliente,id_proveedor):
    conexion = obtener_conexion()
    info = ()
    with conexion.cursor() as cursor:
        cursor.execute('SELECT id_conversacion FROM conversacion'+
        ' WHERE id_cliente = %s AND id_proveedor = %s',(id_cliente,id_proveedor))
        info = cursor.fetchone()
    conexion.close()
    return info

def obtener_conversacionesC(id_cliente):
    conexion = obtener_conexion()
    conversaciones = ()
    with conexion.cursor() as cursor:
        cursor.execute('SELECT conversacion.id_conversacion,conversacion.id_proveedor,proveedor.nombre,proveedor.ape_paterno,proveedor.ape_materno,'+
        '(SELECT mensaje.mensaje FROM mensaje WHERE mensaje.id_conversacion=conversacion.id_conversacion ORDER BY mensaje.fecha DESC LIMIT 1) AS "ultimo_mensaje",'+
        '(SELECT mensaje.fecha FROM mensaje WHERE mensaje.id_conversacion=conversacion.id_conversacion ORDER by mensaje.fecha DESC LIMIT 1) AS "fecha"'+
        ' FROM conversacion INNER JOIN proveedor ON proveedor.id_proveedor = conversacion.id_proveedor WHERE conversacion.id_cliente = %s',(id_cliente))
        conversaciones = cursor.fetchall()
    conexion.close()
    return conversaciones

def registrar_mensaje(id_conversacion,mensaje,id_emisor):
    conexio = obtener_conexion()
    with conexio.cursor() as cursor:
        cursor.execute('INSERT INTO mensaje (id_conversacion,mensaje,id_emisor)'+
        ' VALUES (%s,%s,%s)',(id_conversacion,mensaje,id_emisor))
    conexio.commit()
    conexio.close()

def obtener_mensajes(id_conversacion):
    conexio = obtener_conexion()
    mensajes = ()
    with conexio.cursor() as cursor:
        cursor.execute('SELECT mensaje,fecha,id_emisor FROM mensaje WHERE id_conversacion = '+
        '%s ORDER BY fecha',(id_conversacion))
        mensajes = cursor.fetchall()
    conexio.close()
    return mensajes

def obtener_ultimo_mensaje(id_conver):
    conexion = obtener_conexion()
    mensaje = ()
    with conexion.cursor() as cursor:
        cursor.execute('SELECT mensaje,fecha FROM mensaje WHERE id_conversacion = '+
        '%s ORDER BY fecha DESC LIMIT 1', (id_conver))
        mensaje = cursor.fetchone()
    conexion.close()
    return mensaje

def recuperar_contraC(correo,contra):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute('UPDATE cliente SET contraseña = %s WHERE correo = %s',
        (contra,correo))
    conexion.commit()
    conexion.close()

def recuperar_contraP(correo,contra):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute('UPDATE proveedor SET contraseña = %s WHERE correo = %s',
        (contra,correo))
    conexion.commit()
    conexion.close()
