let formulario, inputs
const expresiones = {
    nombre: /^[a-zA-ZÀ-ÖØ-öø-ÿ]+(\s[a-zA-ZÀ-ÖØ-öø-ÿ]+)*$/,
    apellidos: /^[a-zA-ZÀ-ÖØ-öø-ÿ]+$/,
    telefono: /^[0-9]{10}$/,
    correo: /^[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?$/,
    contraseña: /^.{4,}$/,
    ofigiro: /^[a-zA-ZÀ-ÖØ-öø-ÿ]+\.?(( |\-)[a-zA-ZÀ-ÖØ-öø-ÿ]+\.?)*$/,
    dir:/^[a-zA-Z1-9À-ÖØ-öø-ÿ]+\.?(( |\-)[a-zA-Z1-9À-ÖØ-öø-ÿ]+\.?)*$/
}
let camposValidos = {
    nombre: false,
    apPaterno: false,
    apMaterno: false,
    telefono: false,
    correo: false,
    contra: false,
    check: false
}
document.addEventListener("DOMContentLoaded", function () {
    formulario = document.getElementById('formulario-registro')
    inputs = document.querySelectorAll('#formulario-registro input')
    check = document.getElementById('CheckCondicionesTerminos')

    /* Se evita que el formulario se envie */
    formulario.addEventListener('submit', (e) =>{
        
        if (camposValidos.nombre && camposValidos.apPaterno && camposValidos.apMaterno && camposValidos.telefono
            && camposValidos.correo && camposValidos.contra && camposValidos.check) {
            formulario.submit()
        } else {
            e.preventDefault()
        }
    })
    /* Función que valida los campos del form */
    validarFormulario = (e) => {
        switch(e.target.name){
            case "input_nombre":
                validarCampo(expresiones.nombre, e.target, 'nombre')
            break;
            case "input_ap_pat":
                validarCampo(expresiones.apellidos, e.target, 'apPaterno')
            break;
            case "input_ap_mat":
                validarCampo(expresiones.apellidos, e.target, 'apMaterno')
            break;
            case "input_tel":
                validarCampo(expresiones.telefono, e.target, 'telefono')
            break;
            case "input_correo":
                validarCampo(expresiones.correo, e.target, 'correo')
            break;
            case "input_contra":
                validarCampo(expresiones.contraseña, e.target, 'contra')
                validarReContra()
            break;
            case "input_re_contra":
                validarReContra()
            break;
            case "input_ofigiro":
                validarCampo(expresiones.ofigiro, e.target, 'ofigiro')
            break;
            case "input_aceptar":
                validarCheck(e.target,'check')
            break;
        }
    }

    const validarCheck = (input,campo) => {
        if (input.checked){
            camposValidos[campo] = true
        } else {
            camposValidos[campo] = false
        }
    }

    const validarCampo = (expresion, input, campo) => {
        if (expresion.test(input.value)) {
            document.getElementById(`f_${campo}`).classList.remove('input-val-incorrecto')
            document.getElementById(`f_${campo}`).classList.add('input-val-correcto')
            document.getElementById(`msj-${campo}-noval`).classList.remove('msj-input-incorrecto')
            camposValidos[campo] = true
        } else {
            document.getElementById(`f_${campo}`).classList.remove('input-val-correcto')
            document.getElementById(`f_${campo}`).classList.add('input-val-incorrecto')
            document.getElementById(`msj-${campo}-noval`).classList.add('msj-input-incorrecto')
            camposValidos[campo] = false
        }
    }

    const validarReContra = () => {
        let inputContra = document.getElementById('f_contra')
        let inputReContra = document.getElementById('f_repContra')

        if (inputContra.value !== inputReContra.value) {
            document.getElementById('f_repContra').classList.remove('input-val-correcto')
            document.getElementById('f_repContra').classList.add('input-val-incorrecto')
            document.getElementById('msj-repContra-noval').classList.add('msj-input-incorrecto')
            camposValidos['contra'] = false
        } else {
            document.getElementById('f_repContra').classList.remove('input-val-incorrecto')
            document.getElementById('f_repContra').classList.add('input-val-correcto')
            document.getElementById('msj-repContra-noval').classList.remove('msj-input-incorrecto')
            camposValidos['contra'] = true
        }
    }


    check.addEventListener('change', validarFormulario)

    /* Se agrega un evento a todos los inputs */
    inputs.forEach((input) =>{
        input.addEventListener('keyup',validarFormulario);
        input.addEventListener('blur', validarFormulario);
    })
})

