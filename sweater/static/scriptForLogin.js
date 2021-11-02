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
                if(method ==3){
	                mass = JSON.parse(ajax.responseText).img1;
	                var hint_text = ["Шаг 1. Мысленно найти свое парольное изображение на картинке слева",
                    "Шаг 2. Найти свое парольное изображение на изображении справа",
                    'Шаг 3. Двигая правое изображение кнопками влево вправо, поместить свое парольное\nизображение на '+
                    'правой картинке в тот же толбец или строку, что и в левой'];
	                var frame_block = `<div class="hint" title="${hint_text.join('\n')}">
                    <img id="hint_logo" src="./static/hint.png">
                    Подсказка
                    </div>
                    <div id="passImgBlock">
                        <img id='passImg' src = '' alt="passImg">
                    </div>
                    <div id="frame_block">
                        <div id="frame"></div>
                        <div class="button_bar">
                            <button id="shiftLeft">Сдвинуть влево</button>
                            <button id="shiftRight">Сдвинуть вправо</button>
                            <button id="sendImgMass">Отправить</button>
                        </div>
                    </div>`;

                    document.getElementById("container").innerHTML = frame_block;
                    document.getElementById('passImg').src = "data:image/png;base64," + JSON.parse(ajax.responseText).img2;

                    for(var i in mass){
                        var newdiv = document.createElement("div");
                        newdiv.id=String(i);
                        newdiv.classList.add("frame_img");
                        document.getElementById("frame").appendChild(newdiv);
                        newdiv.style.background = "url(./static/image/"+String(mass[i])+".png)";
                    }
                    document.getElementById("shiftRight").addEventListener("click", shiftRight);
                    document.getElementById("shiftLeft").addEventListener("click", shiftLeft);
                    document.getElementById("sendImgMass").addEventListener("click", sendImgMass);

	            }
	            else{
	                if(method==1){
                        var hint_text = ['Шаг 1. Мысленно найти 3 свои парольные изображения',
                        'Шаг 2. Мысленно построить треугольник, вершинами которого являются эти 3 изображения',
                        'Шаг 3. Кликнуть внутри построенного треугольника'];

                        var hint = `<div class="hint" title="${hint_text.join('\n')}">
                            <img id="hint_logo" src="./static/hint.png">
                            Подсказка
                        </div>`;
                        document.getElementById("container").innerHTML = hint;
	                }
                    else if(method ==2) {
                        var hint_text = ["Шаг 1. Мысленно найти 4 свои парольные изображения",
                        "Шаг 2. Мысленно построить четырехугольник, вершинами которого являются эти 4 изображения",
                        "Шаг 3. Найти точку пересечения диагоналей",
                        "Шаг 4. Кликнуть на точку пересечения диагонале(допустимый радиус погрешности 15 пикселей"];
                        var hint = `<div class="hint" title="${hint_text.join('\n')}">
                                <img id="hint_logo" src="./static/hint.png">
                                Подсказка
                                </div>`;
                            document.getElementById("container").innerHTML = hint;
                    }

                    var loginImg = document.createElement("div");
                    loginImg.id = 'containerForLogin';
                    document.getElementById("container").appendChild(loginImg);
                    var img = document.createElement("img");
                    img.src = "data:image/png;base64,"+ ajax.responseText;
                    document.getElementById("containerForLogin").appendChild(img);
                    document.getElementById("containerForLogin").addEventListener("click", printMousePos);
	            }
	            document.getElementById("errorMessage").className='hidden';
                document.getElementById('firstFactorContainer').className='hidden';
                document.getElementById('flash').className='hidden';
                document.getElementById("formForCheckMethod").className='hidden';
                document.getElementById("radio").className='';
                document.getElementById("container").className='';

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
    document.getElementById("containerForLogin").remove();
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

function shiftRight(){
    mass = mass.splice(-1).concat(mass);
    var container = document.getElementById("containerForLogin");
    for(var i in mass){
        var newdiv = document.getElementById(i);
        newdiv.style.background = "url(./static/image/"+String(mass[i])+".png)";

    }
}
function shiftLeft(){
    mass = mass.concat(mass.splice(0,1));
    var container = document.getElementById("containerForLogin");
    for(var i in mass){
        var newdiv = document.getElementById(i);
        newdiv.style.background = "url(./static/image/"+String(mass[i])+".png)";

    }
}

function sendImgMass(){
    params='login=' + document.getElementById('login').value + '&password=' + document.getElementById('password').value
    + '&coordinate=' + mass + '&method=' + method + '&fastMod=' + document.getElementById('checkMod').checked;
    document.getElementById("frame").remove();
    document.getElementById("passImg").remove();
    ajax.open('POST', '/secondFactor');
    ajax.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    ajax.send(params);

}

document.getElementById("submitMethod").addEventListener("click", checkMethod);
//document.getElementById("containerForLogin").addEventListener("click", printMousePos);

//document.getElementById("shiftRight").addEventListener("click", shiftRight);
//document.getElementById("shiftLeft").addEventListener("click", shiftLeft);
//document.getElementById("sendImgMass").addEventListener("click", sendImgMass);