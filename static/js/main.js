var formData = new FormData(); // Currently empty
var values = {};
var except = [];
var include = [];
var food_context = 0;


$("#loader").hide();


$('#adv').prop('checked', false);

$('#adv').click(function() {
    $("#opts").toggle(this.checked);
});

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
  values[id] = value;
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
      setValue($(this).attr("__item"), parseInt($(this).children("input").first().val())+1);
    }
  });

  if (error){
    return false;
  }
  $("#myDropdown").hide();

  formData.set("values", JSON.stringify(values));
  formData.set("except", JSON.stringify(except));
  var request = new XMLHttpRequest();
  request.open("POST", "/data");
  request.send(formData);
  $("#loader").show();
  $("#xd").show();
  request.onreadystatechange = function() {
  if (request.readyState == XMLHttpRequest.DONE) {
      var resp = request.responseText;
      window.location = '/result?id='+resp;
  }

}

}

function ToggleFoodDropdown(ctx) {
  $("#food-dropdown").toggle();
  food_context = ctx;
  console.log(food_context);
}

function deleteFood(id, ctx){
  var obj = $(`#${getPrefix()}-food-${Number(id)}`);
  switch (food_context) {
    case 0:
      var index = except.indexOf(id);
      if (index !== -1) {
        except.splice(index, 1);
      }
      break;

    case 1:
      var index = include.indexOf(id);
      if (index !== -1) {
        include.splice(index, 1);
      }
      break;
  }

  obj.remove();
}

function getPrefix() {
  var prefix = "";
  switch (food_context) {
    case 0:
      prefix = "ex";
      break;

    case 1:
      prefix = "in";
      break;
  }
  return prefix;
}


function addFood(id) {
  var prefix = getPrefix();
  var optid = `${prefix}-food-${id}`;

  if ($("#" + optid).length == 0) {
    var $tmp = $("#food-default").clone(true);
    $tmp.attr("style", "display:block;");
    $tmp.attr("__item", id);
    $tmp.children("button").first().click(function(){
      deleteFood(id, food_context);
    });
    $tmp.children("h2").first().text($(`#food-${id}`).text());
    $tmp.attr("id", optid);
    $(`#${prefix}-foods`).prepend($tmp);
  }

  switch (food_context) {
    case 0:
      except.push(id);
      break;

    case 1:
      include.push(id);
      break;
  }

  $("#food-dropdown").hide();


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
