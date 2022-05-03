let formulario1, input_n,txta,imgs
const expresiones = {
    nomServicio:/^[a-zA-ZÀ-ÖØ-öø-ÿ]+\.?(( |\-)[a-zA-ZÀ-ÖØ-öø-ÿ]+\.?)*$/,
    desc:/^[a-zA-Z1-9À-ÖØ-öø-ÿ]+\.?(( |\-)[a-zA-ZÀ-ÖØ-öø-ÿ]+\.?)*$/
}
let camposValidos = {
    nom: false,
    desc: false,
    imgs: false
}
document.addEventListener("DOMContentLoaded", function () {
    formulario1 = document.getElementById('form-modi-info-serv')
    input_n = document.getElementById('f_nom_serv')
    txta = document.getElementById('f_desc_serv')
    imgs = document.getElementById('f_img_serv')

    /* Se evita que el formulario se envie */
    formulario1.addEventListener('submit', (e) =>{
        
        if (camposValidos.nom && camposValidos.desc) {
            formulario1.submit()
        } else {
            e.preventDefault()
            document.getElementById('msj-form1').classList.add('msj-input-incorrecto')
        }
    })
    /* Función que valida los campos del form */
    validarFormulario = (e) => {
        document.getElementById('msj-form1').classList.remove('msj-input-incorrecto')
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
    input_n.addEventListener('keyup', validarFormulario);
    input_n.addEventListener('blur', validarFormulario);
    txta.addEventListener('keyup', validarFormulario);
    txta.addEventListener('blur', validarFormulario);
    imgs.addEventListener('change', validarFormulario);
})

