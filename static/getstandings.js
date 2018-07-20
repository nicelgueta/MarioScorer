function callApi(endpoint){
  var xhttp = new XMLHttpRequest();
  xhttp.open("GET", endpoint, false);
  xhttp.setRequestHeader("Content-type", "application/json");
  xhttp.send();
  var response = JSON.parse(xhttp.responseText);
  console.log(response);
  return response;
}
function getImgStr(name){
  var imgStr = "./static/"+name+".png";
  return imgStr;
}
window.onload = function(){
  var response = callApi("./ping");
  document.getElementById("versionSub").innerHTML = ("v."+response.version);
  // call api for podium
  var name;
  var player;
  var image;
  var i;
  var imageStr;
  // call api for names
  var responseList = callApi("./getPodium")["podium"];
  console.log(responseList);
  console.log(responseList.length);
  //create the str
  for (i = 0; i < responseList.length;i++ ){
    player = "player"+(i+1);
    console.log(player);
    name = responseList[i];
    image = "image"+(i+1);
    // set header name
    imageStr = getImgStr(name);
    console.log(imageStr);
    document.getElementById(player).innerHTML = name;
    document.getElementById(image).src = imageStr;
  }
}
