const events = ['dragenter', 'dragover', 'dragleave', 'drop'];
const dropArea = document.getElementById('drop-area');
const csrfmiddlewaretoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
const gallery = document.getElementById('gallery');


document.querySelector("#fileElem").addEventListener("change", (e) => {
    if(window.File && window.FileReader && window.FileList && window.Blob) {
        const files = e.target.files;
        const output = document.querySelector("#gallery");
        for(let i = 0; i < files.length; i++) {
            if(!files[i].type.match("image")) continue;
            const picReader = new FileReader();
            picReader.addEventListener("load", function(event) {
                const picFile = event.target;
                const li = document.createElement("li");
                li.classList.add("list-inline-item");
                li.innerHTML = `
                    <div class="portfolio_item">
                        <img class="img-fluid" src="${picFile.result}" alt="${picFile.name}">
                        <div class="edu_stats_list" data-toggle="tooltip" data-placement="top" title="Delete" data-original-title="Delete"><a href="#"><span class="flaticon-garbage"></span></a></div>
                    </div>`;
                gallery.appendChild(li);
            });
            picReader.readAsDataURL(files[i]);
        }
    } else {
        toastr.error('Your browser does not support the File API');
    }
});

<!--        const viewImage = src => {-->
<!--            gallery.innerHTML = `-->
<!--                <li class="list-inline-item">-->
<!--                    <div class="portfolio_item">-->
<!--                        <img class="img-fluid" src="${src}" alt="img">-->
<!--                        <div class="edu_stats_list" data-toggle="tooltip" data-placement="top" title="Delete" data-original-title="Delete"><a href="#"><span class="flaticon-garbage"></span></a></div>-->
<!--                    </div>-->
<!--                </li>-->
<!--            `;-->
<!--        }-->

const uploadFiles = files => {
    //console.log(files);

    const url = '/properties/create/';
    let formData = new FormData();

    for(let file of files) {
        formData.append('file', file);
    }

    fetch(url, {
        method: 'POST',
        header: {
            "XCSRFToken": csrfmiddlewaretoken
        },
        body: formData,
    })
    .then(response => {
        return response.json();
    })
    .then(data => {
        console.log(data);
<!--                [...data].forEach(file => viewImage(file));-->
    })
    .catch(error => {
        console.log(error);
    })
}

const handleFiles = files => {
    //console.log(files);
    uploadFiles(files);
}

const preventDefaultBehaviour = event => {
    event.preventDefault();
    event.stopPropagation();
}

const handleDrop = event => {
    const files = event.dataTransfer.files;
    console.log(files);
    handleFiles(files);
}

events.forEach(event => {
    dropArea.addEventListener(event, preventDefaultBehaviour);
});

dropArea.addEventListener('drop', handleDrop);