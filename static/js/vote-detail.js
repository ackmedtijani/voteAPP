var submit = document.querySelector('.btn-submit');
const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
var questions = document.querySelectorAll('.questions');
var next_button = document.querySelector('.btn-next');
var prev_button = document.querySelector('.btn-previous');

var base_polls_url = "https://127.0.0.1:8000/polls"
var current_path = window.location.href;

var radio_inputs = document.querySelectorAll('input[type="radio"]');
console.log(radio_inputs);


var dat = {};


var first_question = questions[0]
first_question.className ="questions active";
first_question.style.display = "block";


for (i = 0; i < radio_inputs.length ; i++){
    radio_inputs[i].addEventListener('click' , loadNextPage);
}


next_button.addEventListener('click' ,  loadNextPage);
prev_button.addEventListener('click' , loadPreviousPage);

submit.addEventListener('click' , loadoptions);

function loadNextPage(e){

    var active_page = document.querySelector('.active');
    let index = Array.from(questions).indexOf(active_page);

    if (index == questions.length - 1){
        questions[index].style.display = "none"; 
        questions[index].classList.remove("active");
        index = 0;
        questions[index].classList.add("active"); 
        questions[index].style.display = "block";

    }

    else{
        questions[index].style.display = "none"; 
        questions[index + 1].classList.add("active"); 
        questions[index + 1].style.display = "block";
        questions[index].classList.remove("active");
    }


}


function loadPreviousPage(){
    var active_page = document.querySelector('.active');
    let index = Array.from(questions).indexOf(active_page);
    
    if (index == 0){

        questions[index].style.display = "none"; 
        questions[index].classList.remove("active");
        index = questions.length - 1;
        questions[index].classList.add("active"); 
        questions[index].style.display = "block";

    }

    else {
        questions[index].style.display = "none"; 
        questions[index - 1].classList.add("active"); 
        questions[index - 1].style.display = "block";
        questions[index].classList.remove("active");

    }
}

function loadoptions(e){
    e.preventDefault();
    var options = document.querySelectorAll('input:checked');
    console.log("Checked options" , options);
    if (options.length != 0){
        for(i=0 ; i < options.length  ; i++) {
            try{
                if (dat[options[i].name])
                    dat[options[i].name].push(options[i].value);
                else{
                    dat[options[i].name] = [options[i].value];
                }
            }
            catch{
                dat[options[i].name] = [options[i].value];
            }

        }
        console.log(dat);
        submitPoll(dat);
    }
    else{
        alert("You can't submit an empty Poll");
    }

}

function submitPoll(data){
    var request = new XMLHttpRequest();
    request.open('post' ,current_path ,  true);
    request.setRequestHeader("Content-Type", "text/plain;charset=UTF-8");
    request.setRequestHeader('X-CSRFToken' , csrftoken);
    
    request.onload = function(){
        if (request.status == 200){

            setTimeout(1000);
            windows.location.replace(base_polls_url);

        }

        else{
            var warningbox = document.querySelector('.warning-alert');
            warningbox.style.display = "block";
            console.log(warningbox);

        }
    }

    request.send(JSON.stringify(data));
    location.reload();
}