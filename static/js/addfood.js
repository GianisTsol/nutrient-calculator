var formData = new FormData(); // Currently empty
var inputdiv = document.getElementById("inputs");
var demofield = document.getElementById("input-default");
var paramlist = document.getElementById("myDropdown");

function addParam(id){
  var element =  document.getElementById(`input-${id}`);
  if (element == null)
  {
    formData.append(id, 0);
    var tmp = demofield.cloneNode(true);
    tmp.setAttribute("style", "display:block;");
    tmp.setAttribute("id", `input-${id}`);
    tmp.setAttribute("__item", id);
    tmp.children[1].setAttribute("onClick", `deleteParam(${id})`);
    tmp.children[0].innerHTML = paramlist.children[id+1].innerHTML;
    inputdiv.appendChild(tmp);
  }
}

function deleteParam(id){
  var obj = document.getElementById(`input-${id}`);
  obj.remove();
  formData.delete(id);
}

function setValue(id, value){
  formData.set(id, value);
}

function sendParams(){
  var children = Array.from(inputdiv.children);
  children.forEach(function(i) {
    if (i.getAttribute("__item") != null){
      setValue(i.getAttribute("__item"), i.children[2].value);
    }
  });

  formData.append("file", '');

  setValue('name', document.getElementById(`food-name`).value);
  setValue('auth', document.getElementById(`user-key`).value);
  setValue('limit', document.getElementById(`food-limit`).value);
  setValue('file', document.getElementById(`photo-file`).files[0]);
  var request = new XMLHttpRequest();
  request.open("POST", "{{ url_for('addfood') }}");
  request.send(formData);

  request.onreadystatechange = function() {
  if (request.readyState == XMLHttpRequest.DONE) {
      var resp = request.responseText;
      alert(resp);
  }
}

}
</script>

<script>
/* When the user clicks on the button,
toggle between hiding and showing the dropdown content */
function myFunction() {
document.getElementById("myDropdown").classList.toggle("show");
}

function filterFunction() {
var input, filter, ul, li, a, i;
input = document.getElementById("myInput");
filter = input.value.toUpperCase();
div = document.getElementById("myDropdown");
a = div.getElementsByTagName("a");
for (i = 0; i < a.length; i++) {
  txtValue = a[i].textContent || a[i].innerText;
  if (txtValue.toUpperCase().indexOf(filter) > -1) {
    a[i].style.display = "";
  } else {
    a[i].style.display = "none";
  }
}
}
