let formulario, input_n,txta,imgs,radio_btns
const expresiones = {
    nomServicio:/^[a-zA-ZÀ-ÖØ-öø-ÿ]+\.?(( |\-)[a-zA-ZÀ-ÖØ-öø-ÿ]+\.?)*$/,
    desc:/^[a-zA-Z1-9À-ÖØ-öø-ÿ]+\.?(( |\-)[a-zA-ZÀ-ÖØ-öø-ÿ]+\.?)*$/
}
let camposValidos = {
    nom: false,
    desc: false,
    imgs: false,
    radio: false
}
document.addEventListener("DOMContentLoaded", function () {
    formulario = document.getElementById('formulario-reg-servicio')
    input_n = document.getElementById('f_nom_serv')
    txta = document.getElementById('f_desc_serv')
    imgs = document.getElementById('f_img_serv')
    radio_btns = document.querySelectorAll('input[type="radio"][name="radio_opcion"]')

    /* Se evita que el formulario se envie */
    formulario.addEventListener('submit', (e) =>{
        
        if (camposValidos.nom && camposValidos.desc && camposValidos.imgs && camposValidos.radio) {
            formulario.submit()
        } else {
            if(document.querySelector('input[name="radio_opcion"]:checked') == null){
                document.getElementById('contenedor-radio-btns').classList.add('radio-cont-no-val')
                document.getElementById('msj-radios-noval').classList.add('msj-input-incorrecto')
                camposValidos['radio'] = false
            }
            e.preventDefault()
        }
    })
    /* Función que valida los campos del form */
    validarFormulario = (e) => {
        switch(e.target.name){
            case "input_nom":
                validarCampo(expresiones.nomServicio, e.target,"nom")
            break;
            case "input_desc":
                validarCampo(expresiones.desc,e.target,"desc")
            break;
            case "input_imgs":
                validarImgF(e.target,"imgs")
            break;
            case "radio_opcion":
                if(document.querySelector('input[name="radio_opcion"]:checked') == null){
                    document.getElementById('contenedor-radio-btns').classList.add('radio-cont-no-val')
                    document.getElementById('msj-radios-noval').classList.add('msj-input-incorrecto')
                    camposValidos['radio'] = false
                } else {
                    document.getElementById('contenedor-radio-btns').classList.remove('radio-cont-no-val')
                    document.getElementById('msj-radios-noval').classList.remove('msj-input-incorrecto')
                    camposValidos['radio'] = true
                }
            break    
        }
    }

    const validarCampo = (expresion, input, campo) => {
        if (expresion.test(input.value)) {
            document.getElementById(`f_${campo}_serv`).classList.remove('input-val-incorrecto')
            document.getElementById(`f_${campo}_serv`).classList.add('input-val-correcto')
            document.getElementById(`msj-${campo}-noval`).classList.remove('msj-input-incorrecto')
            camposValidos[campo] = true
        } else {
            document.getElementById(`f_${campo}_serv`).classList.remove('input-val-correcto')
            document.getElementById(`f_${campo}_serv`).classList.add('input-val-incorrecto')
            document.getElementById(`msj-${campo}-noval`).classList.add('msj-input-incorrecto')
            camposValidos[campo] = false
        }
    }

    const validarImgF = (input, campo) =>{
        let imgs = input.files;
        if (imgs.length == 0){
            camposValidos[campo] = false
        } else {
            camposValidos[campo] = true
        }
    }

    /* Se agrega un evento a todos los inputs */
    input_n.addEventListener('keyup', validarFormulario);
    input_n.addEventListener('blur', validarFormulario);
    txta.addEventListener('keyup', validarFormulario);
    txta.addEventListener('blur', validarFormulario);
    imgs.addEventListener('change', validarFormulario);

    radio_btns.forEach(radio => radio.addEventListener('change', validarFormulario))
})

