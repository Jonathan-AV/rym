let formulario_cali,input_cali
let campoValido = {
    cali: false
}

document.addEventListener("DOMContentLoaded", function (){
    formulario_cali = document.getElementById("form_calif")
    input_cali = document.getElementById("f_cali")

    formulario_cali.addEventListener("submit", (e) =>{
        if(input_cali.value != ""){
            formulario_cali.submit()
        }else{
            e.preventDefault()
        }
    })

    validarFormCali = (e) =>{
        if(e.target.value = ""){
            campoValido["cali"] = false
        }else{
            campoValido["cali"] = true
        }
    }
})