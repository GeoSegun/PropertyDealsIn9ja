
const csrfmiddlewaretoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
let img_list = [];

const uploadImage = () => {
    let button = document.getElementsByClassName("images pic");
    let uploader = document.querySelector('<input type="file" name="file" accept="image/*" />')
    let images = document.getElementsByClassName("images");

    button.addEventListener('click', function () {
        if (img_list.length == 5) {
            document.querySelector(this).hide()
        } else {
            uploader.click()
        }
        //uploader.click()
    })

    uploader.addEventListener('change', function () {
        var reader = new FileReader()
        reader.onload = function(event) {
            images.prepend('<div class="img" style="background-image: url('' + event.target.result + '');" rel="'+ event.target.result  +'"><span>remove</span></div>')
        }
        reader.readAsDataURL(uploader[0].files[0])

        // add uploaded images to a list...
        img_list.push(uploader[0].files[0])
        console.log(img_list)
    })

    images.addEventListener('click', '.img', function () {
        document.querySelector(this).remove()
    })
}


document.querySelector('#send').addEventListener('click', function () {
    console.log(img_list);

    const url = "/properties/create/";
    let formData = new FormData();

    for(let file of img_list) {
        formData.append('file', file);
    }

    fetch(url,  {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrfmiddlewaretoken
        },
        body: formData
    })
    .then((response) => response.json())
    .then( data => console.log(data))
    .catch(error => console.log(error))

    $.ajax({
        url: "{% url 'properties:create' %}",
        type: 'POST',
        data: {'imgFiles[]': img_list},
        contentType: 'application/x-www-form-urlencoded',
        dataType: 'json',
        success: function (response) {
            console.log(response)
            setTimeout(function () {
                window.location.replace("{% url 'properties:get_my_property_list' %}");
            }, 5000);
        },
        error: function (response) {
        },
    })
})