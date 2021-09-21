var formData = new FormData(); // Currently empty

function addParam(id){
  var element = $(`#input-${id}`);
  if (element.length == 0)
  {
    formData.append(id, 0);
    var $tmp = $("#input-default").clone(true);
    $tmp.attr("style", "display:block;");
    $tmp.attr("id", `input-${id}`);
    $tmp.attr("__item", id);
    $tmp.children("button").first().click(function(){
      deleteParam(id);
    });
    $tmp.children("h2").first().text($(`#option-${id}`).text());
    $tmp.appendTo($('#inputs'))
  }
}

function deleteParam(id){
  var obj = $(`#input-${Number(id)}`);
  obj.remove();
  formData.delete(id);
}

function setValue(id, value){
  formData.set(id, value);
}

function sendParams(){
  var children = $('#inputs').children();
  children.each(function(i) {
    if ($(this).attr("__item") != null){
      setValue($(this).attr("__item"), $(this).children("input").first().val());
    }
  });


  var request = new XMLHttpRequest();
  request.open("POST", "/data");
  request.send(formData);

  request.onreadystatechange = function() {
  if (request.readyState == XMLHttpRequest.DONE) {
      var resp = request.responseText
      window.location = '/result?id='+resp;
  }

}

}

/* When the user clicks on the button,
toggle between hiding and showing the dropdown content */
function ToggleDropdown() {
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
