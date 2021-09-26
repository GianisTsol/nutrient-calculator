var formData = new FormData(); // Currently empty

$("#loader").hide();

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
    $tmp.insertBefore($('#drop'));
    $("#myDropdown").hide();
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
  var error = false;
  console.log($('#inputs').children().length);
  if ($('#inputs').children().length < 3){
    $("#notification").text("Add atleast one element.");
    $("#notification").show();
    return false;
  }
  children.each(function(i) {
    if ($(this).attr("__item") != null){
      if ($(this).children("input").first().val() == ""){
        $("#notification").text("Please fill in all of the values.");
        $("#notification").show();
        error = true;
        return false;
      }
      setValue($(this).attr("__item"), $(this).children("input").first().val());
    }
  });

  if (error){
    return false;
  }
  $("#myDropdown").hide();

  var request = new XMLHttpRequest();
  request.open("POST", "/data");
  request.send(formData);
  $("#loader").show();
  request.onreadystatechange = function() {
  if (request.readyState == XMLHttpRequest.DONE) {
      var resp = request.responseText;
      window.location = '/result?id='+resp;
  }

}

}



/* When the user clicks on the button,
toggle between hiding and showing the dropdown content */
function ToggleDropdown() {
$("#myDropdown").toggle();
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
