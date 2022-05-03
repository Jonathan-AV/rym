let formulario1,formulario2,formulario3, inputs
const expresiones = {
    nombre: /^[a-zA-ZÀ-ÖØ-öø-ÿ]+(\s[a-zA-ZÀ-ÖØ-öø-ÿ]+)*$/,
    apellidos: /^[a-zA-ZÀ-ÖØ-öø-ÿ]+$/,
    telefono: /^[0-9]{10}$/,
    contraseña: /^.{4,}$/
}
let camposValidos = {
    nombre: false,
    apPaterno: false,
    apMaterno: false,
    telefono: false,
    contra: false
}
document.addEventListener("DOMContentLoaded", function () {
    formulario1 = document.getElementById('form-modi-info-personal')
    formulario2 = document.getElementById('form-modi-contra')
    inputs = document.querySelectorAll('#formulario-modificacion input')

    /* Se evita que el formulario se envie */
    formulario1.addEventListener('submit', (e) =>{
        
        if (camposValidos.nombre && camposValidos.apPaterno && camposValidos.apMaterno && camposValidos.telefono) {
            formulario1.submit()
        } else {
            e.preventDefault()
            document.getElementById('msj-form1').classList.add('msj-input-incorrecto')
        }
    })

    formulario2.addEventListener('submit', (e) => {
        if(camposValidos.contra){
            formulario2.submit()
        }else{
            document.getElementById('msj-form2').classList.add('msj-input-incorrecto')
            e.preventDefault()
        }
    })
    /* Función que valida los campos del form */
    validarFormulario = (e) => {
        document.getElementById('msj-form1').classList.remove('msj-input-incorrecto')
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
            case "input_contra":
                validarCampo(expresiones.contraseña, e.target, 'contra')
                validarReContra()
            break;
            case "input_re_contra":
                validarReContra()
            break;
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
        document.getElementById('msj-form2').classList.remove('msj-input-incorrecto')
        if(inputContra.value == ""){
            camposValidos['contra'] = false
        }else{
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
    }

    /* Se agrega un evento a todos los inputs */
    inputs.forEach((input) =>{
        input.addEventListener('keyup',validarFormulario);
        input.addEventListener('blur', validarFormulario);
    })
})

