var possiblePositions = ["winner","runner1","runner2","loser"];
var possibleChoices = ["Choose runner up", "Choose 2nd runner up","Choose loser","All done!"]
var choiceText = [];
var playerList = [];
var index = 0;
var useList = [];
var override = false;
var submitParamString = "";

function resetVars() {
  choiceText = [];
  playerList = [];
  index = 0;
  useList = [];
  override = false;
  submitParamString = "";
}
function checkPlayerNotUsed(name){
  console.log(playerList.indexOf(name) > -1)
  if (playerList.indexOf(name) > -1){
    raiseError(name+" has already been chosen - refresh page to start again");
    override = true;
  }
}
function kickOffScores(no_players){
  document.getElementById("choice").innerHTML = "Choose the winner";
  // reset variables if chosen again
  resetVars();
  // hide submission button if available
  hideElement("submission");
  if (no_players === 2){
    hideElement("runner1p");
    useList = useList.concat(possiblePositions.slice(0,1),possiblePositions.slice(3));
    choiceText = possibleChoices.slice(2);
  } else if (no_players === 3) {
    showElement("runner1p","inline-block");
    useList = useList.concat(possiblePositions.slice(0,2),possiblePositions.slice(3));
    choiceText = choiceText.concat(possibleChoices.slice(0,1),possibleChoices.slice(2));
  } else {
    useList = possiblePositions;
    choiceText = possibleChoices;
  }
  console.log("Choices length: "+choiceText.length);
  console.log("use list length: "+useList.length);
}
function usePlayer(name){
  checkPlayerNotUsed(name);
  let player = document.getElementById(name).id;
  document.getElementById(useList[index]).innerHTML = name;
  document.getElementById("choice").innerHTML = choiceText[index];
  playerList.push(name);
  console.log("Playerlist = "+playerList);
  index++;
  console.log("index: "+index);
  checkComplete(override);
}
function showElement(element,displayType) {
    var x = document.getElementById(element);
    x.style.display = displayType;
}
function hideElement(element) {
    var x = document.getElementById(element);
    x.style.display = "none";
}
function checkComplete(override){
  console.log("Positions length: "+(useList.length))
  console.log("Complete? "+(index === useList.length))
  if (! override){
    console.log(index);
    if (index === useList.length){
      let element = "submission";
      showElement(element,"inline-block");
      // create string to send to python
      document.getElementById("marioSubmit").value = playerList.toString();
    }
  }
}
function raiseError(errorMsg){
    console.log("raising error: "+errorMsg);
    document.getElementById("errormsg").innerHTML = errorMsg;
    showElement("errormsg","block");
    // prevent scores being submitted
    hideElement("submission");
}
