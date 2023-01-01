// get all stars

const one = document.getElementById('first');
const two = document.getElementById('second');
const three = document.getElementById('third');
const four = document.getElementById('fourth');
const five = document.getElementById('fifth');

const form = document.querySelector('.rate-form');
const ratingls = document.querySelector('.rating-list');
const submit = document.getElementById('review-submit');
const csrfToken = document.getElementsByName('csrfmiddlewaretoken');

let agentID;
let starRatingVal = 0;
let commentVal = document.getElementById('comment-value').value;

const handleStarSelect = (size) => {
    const children = ratingls.children
    for(let i=0; i < children.length; i++) {
        if(i <= size) {
            children[i].classList.add('checked');
        } else {
            children[i].classList.remove('checked');
        }
    }
}

// longer version - to be optimized
const handleSelect = (selection) => {
    switch(selection){
        case 'first': {
//            one.classList.add('checked')
//            two.classList.remove('checked')
//            three.classList.remove('checked')
//            four.classList.remove('checked')
//            five.classList.remove('checked')
            handleStarSelect(1)
            return
        }
        case 'second': {
//            one.classList.add('checked')
//            two.classList.add('checked')
//            three.classList.remove('checked')
//            four.classList.remove('checked')
//            five.classList.remove('checked')
            handleStarSelect(2)
            return
        }
        case 'third': {
//            one.classList.add('checked')
//            two.classList.add('checked')
//            three.classList.add('checked')
//            four.classList.remove('checked')
//            five.classList.remove('checked')
            handleStarSelect(3)
            return
        }
        case 'fourth': {
//            one.classList.add('checked')
//            two.classList.add('checked')
//            three.classList.add('checked')
//            four.classList.add('checked')
//            five.classList.remove('checked')
            handleStarSelect(4)
            return
        }
        case 'fifth': {
//            one.classList.add('checked')
//            two.classList.add('checked')
//            three.classList.add('checked')
//            four.classList.add('checked')
//            five.classList.add('checked')
            handleStarSelect(5)
            return
        }
    }
}

const getNumericValue = (stringValue) => {
    let numericValue;
    if (stringValue === "first") {
        numericValue = 1;
    } else if (stringValue === "second") {
        numericValue = 2;
    } else if (stringValue === "third") {
        numericValue = 3;
    } else if (stringValue === "fourth") {
        numericValue = 4;
    } else if (stringValue === "fifth") {
        numericValue = 5;
    } else {
        numericValue = 0;
    }
    return numericValue;
}

if (one) {
    const arr = [one, two, three, four, five];

    arr.forEach(item => item.addEventListener('mouseover', (event) => {
        handleSelect(event.target.id)
    }));

    arr.forEach(item => item.addEventListener('click', (event) => {
        const val = event.target.id;
        console.log(val);

        ratingls.addEventListener('click', (e) => {
            e.preventDefault();
            const id = e.target.id;
            starRatingVal = getNumericValue(id);
            console.log(`current rating is ${starRatingVal}`);
        })
    }));
}

form.addEventListener('submit', (e) => {
    e.preventDefault();
    console.log(`Agent ID: ${e.target.id}`);
    $.ajax({
        type: 'POST',
        url: `/ratings/${e.target.id}/`,
        data: {
            'csrfmiddlewaretoken': csrfToken[0].value,
            'rating': starRatingVal,
            'comment': commentVal,
        },
        success: function(response){
            console.log(response)
            toastr.success(`Agent successfully rated with ${response.score}`);
        },
        error: function(response){
            toastr.error(`Oops... something went wrong do check your internet`);
        }
    });
});
