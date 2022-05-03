function mostrarPreImagen(event){
    if (event.target.files.length > 0) {
        let src = URL.createObjectURL(event.target.files[0]);
        let preImg = document.getElementById("pre_img");
        preImg.src = src;
        preImg.style.display = "block";
    }
}