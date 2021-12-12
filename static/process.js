main = () => {
    let image_input = document.querySelector("#image_input")

    let blur_element = document.querySelector("#blur")
    let gamma_element = document.querySelector("#gamma")
    let hue_element = document.querySelector("#hue")
    let saturate_element = document.querySelector("#saturate")
    let vibrance_element = document.querySelector("#vibrance")
    let sharpen_element = document.querySelector("#sharpen")

    let blur_val = 0
    let gamma_val = 1
    let hue_val = 1
    let saturate_val = 1
    let vibrance_val = 1
    let sharpen_val = 1

    let process = document.querySelector("#process")
    let reset = document.querySelector("#reset")

    let preview_canvas = document.querySelector("#preview_canvas")
    let preview_ctx = preview_canvas.getContext("2d")
    let preview_w = preview_canvas.getAttribute("width")
    let preview_h = preview_canvas.getAttribute("height")

    let hidden_canvas = document.querySelector("#hidden_canvas")
    let hidden_ctx = hidden_canvas.getContext("2d")
    let hidden_canvas_data = null

    let preview_image = new Image()
    let hidden_image = new Image()

    let link_section = document.querySelector("#link_section")
    let link = document.querySelector("a")

    blur_element.addEventListener("change", () => {
        blur_val = blur_element.value
    })

    gamma_element.addEventListener("change", () => {
        gamma_val = gamma_element.value
    })

    hue_element.addEventListener("change", () => {
        hue_val = hue_element.value
    })

    saturate_element.addEventListener("change", () => {
        saturate_val = saturate_element.value
    })

    vibrance_element.addEventListener("change", () => {
        vibrance_val = vibrance_element.value
    })

    sharpen_element.addEventListener("change", () => {
        sharpen_val = sharpen_element.value
    })

    image_input.addEventListener("change", (e1) => {
        if(e1.target.files){
            let imageFile = e1.target.files[0]
            let reader = new FileReader()
            reader.readAsDataURL(imageFile)
            reader.onload = (e2) => {
                hidden_image.src = e2.target.result
                preview_image.src = e2.target.result

                hidden_image.onload = () => {
                    preview_ctx.drawImage(preview_image, 0, 0, preview_w, preview_h)

                    hidden_canvas.setAttribute("width", hidden_image.width)
                    hidden_canvas.setAttribute("height", hidden_image.height)

                    hidden_ctx.drawImage(hidden_image, 0, 0, hidden_canvas.width, hidden_canvas.height)
                    hidden_canvas_data = hidden_canvas.toDataURL("image/jpeg", 0.92)
                }
            }
        }
    })

    process.addEventListener("click", () => {
        // console.log(blur_val, saturate_val, sharpen_val)
        if (hidden_canvas_data === null){
            alert("Please Upload an Image First")
        }
        else{
            
            let data = {
                data : JSON.stringify({
                    imageData : hidden_canvas_data,
                    blur : blur_val,
                    gamma : gamma_val,
                    hue : hue_val,
                    saturate : saturate_val,
                    vibrance : vibrance_val,
                    sharpen : sharpen_val,
                }),
            }

            $.ajax({
                type : "POST",
                url : "",
                headers : {
                    "X-CSRFToken" : Cookies.get("csrftoken"),
                },
                data : data,
                success : (response) => {
                    console.log("----------")
                    console.log(`Success, StatusText : ${response["statusText"]}`)
                    console.log("----------")
                    
                    hidden_image.src = response["imageData"]
                    hidden_image.onload = () => {
                        preview_image.src = response["imageData"]
                        preview_ctx.drawImage(preview_image, 0, 0, preview_w, preview_h)
                        hidden_ctx.drawImage(hidden_image, 0, 0, hidden_canvas.width, hidden_canvas.height)

                        link.setAttribute("target", "_blank")
                        link.setAttribute("download", "image.jpg")
                        link.setAttribute("href", hidden_canvas.toDataURL("image/jpeg", 0.92))
                        link_section.hidden = false
                    }
                }
            })
        }
    })

    reset.addEventListener("click", () => {
        image_input.value = ""
        preview_ctx.clearRect(0, 0, preview_w, preview_h)
        preview_image.src = ""
        hidden_image.src = ""
        hidden_canvas_data = null
        blur_element.value = 3
        gamma_element.value = 1
        hue_element.value = 1
        saturate_element.value = 1
        vibrance_element.value = 1
        sharpen_element.value = 1
        link_section.hidden = true
    })

}

main()