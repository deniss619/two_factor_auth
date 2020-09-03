var modal = document.getElementById("my_modal");
var btn = document.getElementById("btn_modal_window");
var span = document.getElementsByClassName("close_modal_window")[0];

span.onclick = function () {
    modal.style.display = "none";
}

window.onclick = function (event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
}
function back_to_auth(){
    location="/";
}

var ajax = new XMLHttpRequest();
ajax.onreadystatechange = function() {
    var errorMark=0;
    if (ajax.readyState == 4) {
        if (ajax.status == 200) {
            if(ajax.responseText=="success"){
                location="success";
        	}

	        else if(ajax.responseText=='error'){
	            document.getElementById("errorMessage").innerHTML='Ошибка в логине или пароле';
	            document.getElementById("errorMessage").className='';
	        }
	        else if(ajax.responseText=='banned'){
	            modal.style.display = "block";
	        }
            else if(ajax.responseText=='checkMethodForm'){
                document.getElementById("firstFactorContainer").className='hidden';
	            document.getElementById("formForCheckMethod").className='';
            }

	        else{
                document.getElementById("loginImg").src="data:image/png;base64,"+ajax.responseText;
                document.getElementById("errorMessage").className='hidden';
                document.getElementById('firstFactorContainer').className='hidden';
                document.getElementById('flash').className='hidden';
                document.getElementById("formForCheckMethod").className='hidden';
                document.getElementById("radio").className='';
            }
    	}
	}
}


function checkLoginPassword(){
    params='login=' + document.getElementById('login').value + '&password=' + document.getElementById('password').value;
    ajax.open('POST', '/');
    ajax.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    ajax.send(params);
}


function printMousePos(event) {
    var methods=document.getElementsByName('method');
    for (var i=0; i<3; ++i)
        if (methods[i].checked){
            method=i+1
            }
    console.log("clientX: " + event.offsetX + " - clientY: " + event.offsetY);
    mass=[event.offsetX,event.offsetY]
    params='login=' + document.getElementById('login').value + '&password=' + document.getElementById('password').value
    + '&coordinate=' + mass.join() + '&fastMod=' + document.getElementById('checkMod').checked + '&method=' + method;
    ajax.open('POST', '/secondFactor');
    ajax.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    ajax.send(params);
}


function checkMethod(e){
    e.preventDefault();
    var methods=document.getElementsByName('method');
    for (var i=0; i<3; ++i)
        if (methods[i].checked){
            method=i+1
            }
    params='login=' + document.getElementById('login').value + '&password=' + document.getElementById('password').value
    + '&method=' + method;
    ajax.open('POST', '/secondFactor');
    ajax.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    ajax.send(params);
}

document.getElementById("submitMethod").addEventListener("click", checkMethod);
document.getElementById("containerForLogin").addEventListener("click", printMousePos);