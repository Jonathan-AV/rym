from datetime import datetime
from functools import wraps
import os,controlador,utilidadesRyM
import pymysql
from flask import Flask,render_template, request,redirect,url_for, flash, session
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mail import Mail,Message
from config import Config
from flask_socketio import SocketIO,join_room

app = Flask(__name__)
app.secret_key = "PR0Y3CT0#RyM#24_#19_#01"
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config.from_object(Config)
mail = Mail(app)
socketio = SocketIO(app)

def login_required(f):
    @wraps(f)
    def wrap(*args,**kwargs):
        if 'id_usuarioC' or 'id_usuarioP' in session:
            return f(*args,**kwargs)
        else:
            return redirect(url_for('index'))
    return wrap

@app.route("/")
def index():
    if "id_usuarioP" in session:
        return redirect(url_for("inicio_proveedor"))
    elif "id_usuarioC" in session:
        return redirect(url_for("inicio_cliente"))
    else:    
        return render_template('index.html')

@app.route("/sesion_cliente", methods=["GET","POST"])
def sesion_cliente():
    if request.method == "POST":
        correo = request.form['input_correo']
        contra = request.form['input_contra']
        U_cliente = controlador.obtener_cuentaC(correo)

        if U_cliente == None or not check_password_hash(U_cliente[1],contra):
            # Para enviar un mensaje despues de fallar al identificar el usuario:
            msj_uIncorrecto = 'El correo y/o la contraseña no conciden. Si no tiene una cuenta se le aconseja registrarse.'
            flash(msj_uIncorrecto, 'usuario-incorrecto')

            return redirect(url_for('sesion_cliente'))
        else:
            session["id_usuarioC"] = U_cliente[0]
            return redirect(url_for('inicio_cliente')) 
    else:    
        return render_template('sesion_cliente.html')

@app.route("/sesion_proveedor", methods=['GET','POST'])
def sesion_proveedor():
    if request.method == 'POST':
        correo = request.form['input_correo']
        contra = request.form['input_contra']

        U_proveedor = controlador.obtener_cuentaP(correo)
        if U_proveedor == None or not check_password_hash(U_proveedor[1],contra):
            # Para enviar un mensaje despues de fallar al identificar el usuario:
            msj_uIncorrecto = 'El correo y/o la contraseña no conciden. Si no tiene una cuenta se le aconseja registrarse.'
            flash(msj_uIncorrecto, 'usuario-incorrecto')

            return redirect(url_for('sesion_proveedor'))
        else:
            session["id_usuarioP"] = U_proveedor[0]
            return redirect(url_for('inicio_proveedor')) 

    else:    
        return render_template('sesion_proveedor.html')

@app.route("/registro_cilente", methods=['GET','POST'])
def registro_cliente():
    if request.method == 'POST':
        nombC = request.form['input_nombre']
        apPaternoC = request.form['input_ap_pat']
        apMaternoC = request.form['input_ap_mat']
        telC = request.form['input_tel']
        correoC = request.form['input_correo']
        contraC = generate_password_hash(request.form['input_contra'], method="sha256",salt_length=5)

        img_perfil = request.files['img_perfil']
        f_img = ""
        imgPath = ""
        if img_perfil.filename == None or img_perfil.filename == "":
            imgPath = None
        else:    
            f_img = secure_filename(utilidadesRyM.nombrarNArchivo(img_perfil.filename))
            imgPath = os.path.join('static\img_perfiles',f_img)
            img_perfil.save(imgPath)
        
        try:
            controlador.insertar_cliente(nombC,apPaternoC,apMaternoC,telC,
            correoC,contraC,imgPath)
        except pymysql.err.IntegrityError as except_detail:
            if except_detail.args[0] == 1062:
                flash('El correo ya está registrado en la aplicación. Por cuestiones del buen funcionamiento '+
                'de la aplicación, le pedimos que ingrese otro correo.','correo-repetido')
            return redirect(url_for('registro_cliente'))
        
        return redirect(url_for('sesion_cliente')) 
    else:    
        return render_template('registro_cliente.html')

@app.route("/registro_proveedor", methods=['GET', 'POST'])
def registro_proveedor():
    if request.method == 'POST':
        nomP = request.form['input_nombre']
        apPaternoR = request.form['input_ap_pat']
        apMaternoR = request.form['input_ap_mat']
        ofi_giro = request.form['input_ofigiro']
        dir = request.form['input_dir']
        telP = request.form['input_tel']
        correoP = request.form['input_correo']
        contraP = generate_password_hash(request.form['input_contra'], method="sha256",salt_length=5)
        
        try:
            controlador.insertar_proveedor(nomP,apPaternoR,apMaternoR,ofi_giro,dir,telP,correoP,contraP)
        except pymysql.err.IntegrityError as except_detail:
            if except_detail.args[0] == 1062:
                flash('El correo ya está registrado en la aplicación. Por cuestiones del buen funcionamiento '+
                'de la aplicación, le pedimos que ingrese otro correo.','correo-repetido')
            return redirect(url_for('registro_proveedor'))

        return redirect(url_for('sesion_proveedor'))
    else:    
        return render_template('registro_proveedor.html')

@app.route("/registrar-servicio", methods = ["GET", "POST"])
@login_required
def registrar_servicio():
    if request.method == "POST":
        id_proveedor = session['id_usuarioP']
        nomS = request.form['input_nom']
        descS = request.form['input_desc']
        imgs_subidas = request.files.getlist('input_imgs')
        tipo_servicio = request.form["radio_opcion"]
        
        imgsPaths = []
        for archivos in imgs_subidas:
            nomArchivo = secure_filename(utilidadesRyM.nombrarNArchivo(archivos.filename))
            imgsPaths.append(os.path.join('static\imgs_servicios',nomArchivo))
            archivos.save(os.path.join('static\imgs_servicios',nomArchivo))
        
        controlador.registrar_servicio(id_proveedor,nomS,descS,tipo_servicio)
        controlador.registrar_img_servicio(id_proveedor,nomS,imgsPaths)
        
        msj_serv_reg = "El servicio fue registrado exitosamente."
        flash(msj_serv_reg, 'servicio-registrado')

        return redirect(url_for('registrar_servicio'))
    else:    
        return render_template('registrar_servicio.html')

@app.route("/inicio-p")
@login_required
def inicio_proveedor():
    return render_template('inicio_proveedor.html')

@app.route("/mis-servicios")
@login_required
def mis_servicios():
    id_proveedor = session["id_usuarioP"]
    misServicios = controlador.obtener_mis_servicios(id_proveedor)    
    return render_template('mis_servicios.html', misServicios=misServicios)

@app.route("/eliminar-servicio", methods=["POST"])
@login_required
def eliminar_servicio():
    id_servicio = request.values["inputE_id_servicio"]
    imgs = controlador.obtener_imgs_servicio(id_servicio)
    for img in imgs:
        imagen = img[0]
        if os.path.exists(imagen):
            os.remove(imagen)
    
    controlador.eliminar_servicio(id_servicio)
    return redirect(url_for('mis_servicios'))

@app.route("/modificar-servicio", methods=["GET","POST"])
@login_required
def modificar_servicio():
    if request.method == 'POST':
        id_servicio = request.values['inputM_id_servicio']
        servicio = controlador.obtener_mi_servicio(id_servicio)
        imgs = controlador.obtener_imgs_mi_servicio(id_servicio)
        return render_template('modificar_servicio.html', miServicio=servicio,idServicio=id_servicio,imgs=imgs)
    else:
        return redirect(url_for('index'))

@app.route("/modificar-info-servicio",methods=["POST"])
@login_required
def modificar_info_servicio():
    id_servicio = request.values["input_id_servicio"]
    nomServicio = request.values["input_nom"]
    desc = request.values["input_desc"]
    
    controlador.modificar_info_servicio(id_servicio,nomServicio,desc)
    return redirect(url_for('mis_servicios'))

@app.route("/agregar-img-servicio",methods=["POST"])
@login_required
def agregar_img_servicio():
    id_servicio = request.values["input_id_servicio"]
    imgs = request.files.getlist('input_imgs')
    imgsPaths = []
    for archivos in imgs:
        nomArchivo = secure_filename(utilidadesRyM.nombrarNArchivo(archivos.filename))
        imgsPaths.append(os.path.join('static\imgs_servicios',nomArchivo))
        archivos.save(os.path.join('static\imgs_servicios',nomArchivo))   
    controlador.agregar_imgs_servicio(id_servicio,imgsPaths)
    return redirect(url_for('mis_servicios'))

@app.route("/eliminar-img-servicio", methods=["POST"])
@login_required
def eliminar_img_servicio():
    id_imgS = request.values["input_id_img"]
    imgs = controlador.obtener_img_servicio(id_imgS)
    if os.path.exists(imgs[0]):
        os.remove(imgs[0])
    controlador.eliminar_img_servicio(id_imgS)
    return redirect(url_for('mis_servicios'))

@app.route("/buscar_servicio")
@login_required
def inicio_cliente():
    servicios = controlador.obtener_servicios()
    return render_template('inicio_cliente.html', servicios=servicios)

@app.route("/buscar_proveedor")
@login_required
def buscar_proveedor():
    tipoServicio = request.values["input_servicio"]
    servicios = controlador.obtener_serv_por_tipoSer(tipoServicio)
    return render_template('buscar_proveedor.html',servicios=servicios)

@app.route("/proveedor",methods=["GET","POST"])
@login_required
def proveedor():
    if request.method == 'POST':
        id_servicio = request.values["input_id_servicio"]
        nom_servicio = request.values["input_nom_servicio"]
        id_proveedor = controlador.obtener_idProveedor_por_idServicio(id_servicio)[0]
        proveedor = controlador.obtener_nomProveedor_por_id_servicio(id_servicio)
        imgs = controlador.obtener_imgs_servicio(id_servicio)
        comentarios = controlador.obtener_comentarios(id_servicio)

        return render_template('proveedor.html',proveedor=proveedor,
        imgs=imgs,idServicio=id_servicio,comentarios=comentarios,
        id_proveedor=id_proveedor, nomServicio=nom_servicio)
    else:
        return redirect(url_for('index'))
@app.route("/mensajes_c")
@login_required
def mensajes_cliente():
    id_cliente = session["id_usuarioC"]
    conversaciones = controlador.obtener_conversacionesC(id_cliente)

    return render_template('mensajes_cliente.html',conversaciones=conversaciones)

@app.route("/mensajes_p")
@login_required
def mensajes_proveedor():
    id_proveedor = session["id_usuarioP"]
    conversaciones = controlador.obtener_conversacionesP(id_proveedor)

    return render_template('mensajes_proveedor.html',conversaciones=conversaciones)

@app.route("/calificar-servicio",methods=["POST"])
@login_required
def calificar_servicio():
    cali = request.values["input_califi"]
    id_cliente = session["id_usuarioC"]
    id_servicio = request.values["input_id_servicio"]
    
    controlador.registrar_cali(id_servicio,id_cliente,cali)

    flash('Se ha guardado la calificación del servicio del proveedor.','calificar-servicio')
    return redirect(url_for('inicio_cliente'))

@app.route("/recordar-contra-c", methods=["POST"])
def recordar_contra_c():
    correo = request.values["input_correo"]
    n_contra =utilidadesRyM.generar_nueva_contra()
    hn_contra = generate_password_hash(n_contra, method="sha256",salt_length=5)

    controlador.recuperar_contraC(correo,hn_contra)
    
    msg_correo = Message(subject='Recuperación de contraseña',
    recipients=[correo],sender=app.config["MAIL_USERNAME"],
    html= render_template("correo_recuperar_contra.html",nContra=n_contra))

    mail.send(msg_correo)

    flash('Le enviamos un correo con su nueva contraseña. Le recomendamos cambiarla después de haber ingresado.',
    'contra-recuperada')

    return redirect(url_for('sesion_cliente'))

@app.route("/recordar-contra-p",methods=["POST"])
def recordar_contra_p():
    correo = request.values["input_correo"]
    n_contra = utilidadesRyM.generar_nueva_contra()
    hn_contra = generate_password_hash(n_contra,method="sha256",salt_length=5)

    msg_correo = Message(subject='Recuperacion de contraseña',
    recipients=[correo],sender=app.config["MAIL_USERNAME"],
    html = render_template("correo_recuperar_contra.html", nContra=n_contra))

    controlador.recuperar_contraP(correo,hn_contra)

    mail.send(msg_correo)

    flash('Le enviamos un correo con su nueva contraseña. Le recomendamos cambiarla después de haber ingresado.',
    'contra-recuperada')

    return redirect(url_for('sesion_proveedor'))



@app.route("/solicitar-servicio",methods=["POST"])
@login_required
def solictar_servicio():
    id_cliente = session["id_usuarioC"]
    id_servicio = request.values["input_id_servicio"]
    asunto = request.values["input_asunto"]
    solicitud = request.values["input_solicitud"]

    infoCliente = controlador.obtener_infoCliente_solicitud(id_cliente)
    infoProveedor = controlador.obtener_infoProveedor_solicitud(id_servicio)

    msg_correo = Message(subject=asunto,recipients=[infoProveedor[0]],
                sender=app.config["MAIL_USERNAME"],
                html= render_template('solicitud_servicio.html',infoCliente=infoCliente,servicio=infoProveedor[1],solicitud=solicitud))

    mail.send(msg_correo)

    flash('Se ha enviado su solicitud al proveedor por correo. Este a la espera de que este le conteste.','solicitud-servicio')
    return redirect(url_for('inicio_cliente'))

@app.route("/chat", methods=["POST"])
@login_required
def chat():
    id_usuario = session["id_usuarioC"]
    id_proveedor = request.values["input_id_proveedor"]
    verificacion = controlador.obtener_conversacion(id_usuario,id_proveedor)
    if verificacion == None:
        controlador.crear_conversacion(id_usuario,id_proveedor)
        id_conversacion = controlador.obtener_conversacion(id_usuario,id_proveedor)
        return render_template("chat.html",id_usuario=id_usuario,
        id_proveedor=id_proveedor,
        id_conversacion=id_conversacion[0],mensajesD_c="cliente")
    else:
        id_conversacion = controlador.obtener_conversacion(id_usuario,id_proveedor)
        mensajes = controlador.obtener_mensajes(id_conversacion)

        return render_template("chat.html",id_usuario=id_usuario,
        id_otro=id_proveedor,
        id_conversacion=id_conversacion[0],mensajes=mensajes,mensajesD_c="cliente")

@app.route("/chat/<id_usuario>", methods=["GET"])
@login_required
def chat_g(id_usuario):
    if "id_usuarioP" in session:
        id_proveedor = session["id_usuarioP"]
        id_conversacion = controlador.obtener_conversacion(id_usuario,id_proveedor)
        mensajes = controlador.obtener_mensajes(id_conversacion)

        return render_template("chat.html",id_usuario=id_proveedor,
        id_otro=id_usuario,
        id_conversacion=id_conversacion[0],mensajes=mensajes,mensajesD_p="proveedor")
    elif "id_usuarioC" in session:
        id_cliente = session["id_usuarioC"]
        id_conversacion = controlador.obtener_conversacion(id_cliente,id_usuario)
        mensajes = controlador.obtener_mensajes(id_conversacion)

        return render_template("chat.html",id_usuario=id_cliente,
        id_otro=id_usuario,
        id_conversacion=id_conversacion[0],mensajes=mensajes,mensajesD_c="cliente")

@socketio.on('join_room')
def handles_join_room_event(data):
    app.logger.info("{} inició una la conversación con {}".format(data['username'],data['room']))
    join_room(data['room'])
#     socketio.emit('join_room_announcement',data)

@socketio.on('enviar_mensaje')
def handle_enviar_mensaje_evento(data):
    app.logger.info("{} a enviado un mensaje a la conversacion {}: {}".format(data['username'],data['room'],data['mensaje']))
    data['fecha'] = datetime.now().strftime("%d/%m/%Y - %H:%M:%S")
    controlador.registrar_mensaje(data['room'],data['mensaje'],data['username'])

    socketio.emit('recibir_mensaje', data,room=data['room'])

@app.route("/modificar-informacion-p")
@login_required
def modificar_info_p():
    id_proveedor = session["id_usuarioP"]
    infoP = controlador.obtener_info_proveedor(id_proveedor)
    return render_template('modificar_info_p.html',nombre=infoP[0],apPaterno=infoP[1],apMaterno=infoP[2],
    telefono=infoP[3],ofigiro=infoP[4],direc=infoP[5])

@app.route("/modificar-info-personal-p", methods=["POST"])
@login_required
def modi_info_personal_p():
    id_proveedor = session["id_usuarioP"]
    informacion = request.values
    nomP = informacion['input_nombre']
    apPaternoP = informacion['input_ap_pat']
    apMaternoP = informacion['input_ap_mat']
    ofi_giro = informacion['input_ofigiro']
    dir = informacion['input_dir']
    telP = informacion['input_tel']
    
    controlador.modificar_infoP_p(id_proveedor,nomP,apPaternoP,apMaternoP,ofi_giro,dir,telP)

    return redirect(url_for('modificar_info_p'))

@app.route("/modificar-info-cuenta-p", methods =["POST"])
@login_required
def modi_info_cuenta_p():
    id_proveedor = session["id_usuarioP"]
    contra = generate_password_hash(request.values["input_contra"],method="sha256",salt_length=5) 
    controlador.modificar_contra_p(id_proveedor,contra)
    return redirect(url_for('modificar_info_p'))

@app.route("/modificar-informacion-c")
@login_required
def modificar_info_c():
    id_cliente = session["id_usuarioC"]
    infoC = controlador.obtener_info_cliente(id_cliente)    
    return render_template('modificar_info_c.html',nombre=infoC[0],apPaterno=infoC[1],
    apMaterno=infoC[2],telefono=infoC[3],imgPerfil=infoC[4])

@app.route("/modificar-info-personal-c", methods=["POST"])
@login_required
def modi_info_personal_c():
    id_cliente = session["id_usuarioC"]
    nombC = request.values['input_nombre']
    apPaternoC = request.values['input_ap_pat']
    apMaternoC = request.values['input_ap_mat']
    telC = request.values['input_tel']
    
    controlador.modificar_infoP_c(id_cliente,nombC,apPaternoC,apMaternoC,telC)

    return redirect(url_for('modificar_info_c'))

@app.route("/modificar-info-cuenta-c", methods=["POST"])
@login_required
def modi_info_cuenta_c():
    id_cliente = session["id_usuarioC"]
    contra = generate_password_hash(request.values["input_contra"],method="sha256",salt_length=5)

    controlador.modificar_contra_c(id_cliente,contra)

    return redirect(url_for('modificar_info_c'))

@app.route("/modificar-img-perfil", methods=["POST"])
@login_required
def modificar_img_perfil():
    id_cliente = session["id_usuarioC"]

    img_perfil_anterior = controlador.obtener_img_perfil(id_cliente)[0]
    if os.path.exists(img_perfil_anterior):
        os.remove(img_perfil_anterior)

    img_perfil = request.files['img_perfil']
    f_img = secure_filename(img_perfil.filename)
    imgPath = os.path.join('static\img_perfiles',f_img)
    img_perfil.save(imgPath)

    controlador.modificar_img_perfil(id_cliente,imgPath)

    return redirect(url_for('modificar_info_c'))

@app.route("/solicitud-datos-contacto")
@login_required
def solicitud_dat_contacto():
    id_cliente = session["id_usuarioC"]
    id_servicio = request.values["input_id_servicio"]
    info = controlador.obtener_infoProveedor_por_id_servicio(id_servicio)
    correoC = controlador.obtener_correoC(id_cliente)[0]

    msg_corre = Message('Datos del proveedor: '+info[0]+" "+info[1]+" "+info[2],
                        sender= app.config["MAIL_USERNAME"], recipients= [correoC],
                        html= render_template('correo_solicitudDat_proveedor.html',info=info))
    mail.send(msg_corre)

    flash('Los datos de contacto del proveedor han sido enviados a su correo.','solicitud-datos')
    return redirect(url_for('inicio_cliente'))

@app.route("/registrar-comentario",methods=["POST"])
@login_required
def registrar_comentario():
    id_cliente= session["id_usuarioC"]
    comentario = request.values["input_comentario"]
    servicio = request.values["input_id_servicio"]

    controlador.registrar_comentario(id_cliente,servicio,comentario)

    flash('Su comentario fue registrado exitosamente.','registrar-comentario')

    return redirect(url_for('inicio_cliente'))

@app.route("/cerrar-sesion")
@login_required
def cerrar_sesion():
    if "id_usuarioP" in session:
        session.pop("id_usuarioP",None)
    elif "id_usuarioC" in session:
        session.pop("id_usuarioC",None)

    return redirect(url_for('index'))

if __name__ == "__main__":
    socketio.run(app, debug=True)