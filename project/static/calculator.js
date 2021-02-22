// as soon as the HTML document is fully loaded, do the following
$(document).ready(function() {

    // add placeholders in the boxes in the picture
    document.getElementById("eingabewaende").innerHTML = ("Abstand");
    document.getElementById("eingabewinkel").innerHTML = ("Winkel");
    document.getElementById("eingabehoehe").innerHTML = ("Sitzhöhe");
    document.getElementById("eingabegewicht").innerHTML = ("Gewicht");
    document.getElementById("eingabelaengehaenge").innerHTML = ("Länge Hängematte");
    document.getElementById("eingabelaengeridge").innerHTML = ("Länge Ridgeline");

    document.getElementById("ergebnishoehe").innerHTML = ("Höhe");
    document.getElementById("ergebnisquerkraft").innerHTML = ("Querkraft");
    document.getElementById("ergebnisseilspannung").innerHTML = ("Seilspannung");
    document.getElementById("ergebnislaengeaufhaengung").innerHTML = ("Länge Aufhängung");
});

function calculate() {
    // remove any remaining alert or warning windows and change the color of the box of Länge Aufhängung
    if (document.getElementById("alert-div")) {
        removeText("alert-div");
        changeColor("ergebnislaengeaufhaengung", "#FFFFFF", "#000000");
    } else if (document.getElementById("warning-div")) {
        removeText("warning-div");
        changeColor("ergebnislaengeaufhaengung", "#FFFFFF", "#000000");
    }


    let distance = document.getElementById('abstandwaende').value;
    document.getElementById('eingabewaende').innerHTML = distance + " cm";

    let angle = document.getElementById('winkel').value;
    document.getElementById('eingabewinkel').innerHTML = angle + "°";

    let seatingHeight = document.getElementById('sitzhoehe').value;
    document.getElementById('eingabehoehe').innerHTML = seatingHeight + " cm";

    let weight = document.getElementById('gewicht').value;
    document.getElementById('eingabegewicht').innerHTML = weight + " kg";

    // query all possible options
    let lengthHammockQuery = document.getElementById('haengelaenge');

    // get the index of the selected option
    let index = lengthHammockQuery.selectedIndex;
    // get an array of all possible options
    let optionsAll = lengthHammockQuery.options;

    let lengthHammock;
    let lengthRidgeline;

    // get the value (integer) that the user entered for the length of either the ridgeline or the hammock
    let lengthInput = document.getElementById('laenge').value;

    // display the entered value for the relevant option and calculate the other one
    if (optionsAll[index].value == "laengehaengematte") {
        // print entered value
        lengthHammock = lengthInput;
        document.getElementById('eingabelaengehaenge').innerHTML = lengthHammock + " cm";

        // print derived value based on calculation
        lengthRidgeline = Math.round(lengthInput * Math.cos(2 * Math.PI / 360 * angle));
        document.getElementById('eingabelaengeridge').innerHTML = lengthRidgeline + " cm";
    } else if (optionsAll[index].value == "laengeridgeline") {
        // print entered value
        lengthRidgeline = lengthInput;
        document.getElementById('eingabelaengeridge').innerHTML = lengthRidgeline + " cm";

        // print derived value based on calculation
        lengthHammock = Math.round(lengthInput / Math.cos(2 * Math.PI / 360 * angle));
        document.getElementById('eingabelaengehaenge').innerHTML = lengthHammock + " cm";
    } else {
        console.log("no value");
    }


    // prompt user to enter data in all input fields if something is missing
    if (lengthInput == false || distance == false || angle == false || seatingHeight == false || weight == false) {
        alert("Bitte gib Werte in jedes Feld ein, damit die Aufhängehöhe und Belastung richtig berechnet werden können");
    }


    // calculate different values to output in blue boxed on image
    let fixingHeight = Math.round((distance / (2 * (Math.cos(2 * Math.PI / 360 * angle))) * Math.sin(2 * Math.PI / 360 * angle))) +
        parseInt(seatingHeight);
    document.getElementById('ergebnishoehe').innerHTML = fixingHeight + " cm";
    document.getElementById('statichoehe').innerHTML = fixingHeight + " cm";

    let forceRope = Math.round(weight / (2 * Math.sin(2 * Math.PI / 360 * angle)));
    document.getElementById('ergebnisseilspannung').innerHTML = forceRope + " kg";
    document.getElementById('staticseilspannung').innerHTML = forceRope + " kg";

    let forceHorizontal = Math.round(Math.cos(2 * Math.PI / 360 * angle) * forceRope);
    document.getElementById('ergebnisquerkraft').innerHTML = forceHorizontal + " kg";
    document.getElementById('staticquerkraft').innerHTML = forceHorizontal + " kg";

    let lengthSuspension = Math.round(distance / (2 * Math.cos(2 * Math.PI / 360 * angle)) - lengthHammock / 2);
    document.getElementById('ergebnislaengeaufhaengung').innerHTML = lengthSuspension + " cm";
    document.getElementById('staticlaengeaufhaengung').innerHTML = lengthSuspension + " cm";

    // add alert or warning if lengthSuspension is below certain value
    if (lengthSuspension <= 0) {
        addAlert();
    } else if (lengthSuspension > 0 && lengthSuspension <= 10) {
        addWarning();
    }

}

function addAlert() {
    // show an alert text at the top of the image
    let newNode = document.createElement("div");
    let alertText = document.createTextNode(
        "Die Hängematte ist zu lang. Bitte such dir einen breiteren Aufhängeort oder eine kürzere Hängematte.");
    let existingDiv = document.getElementById("imageBlock");

    newNode.appendChild(alertText);
    existingDiv.appendChild(newNode);
    newNode.id = "alert-div";

    // change the color of the box for Länge Aufhängung
    changeColor("ergebnislaengeaufhaengung", "#FF0000", "#FFFFFF");
    changeColor("staticlaengeaufhaengung", "#FFFFFF", "#FF0000");
}

function addWarning() {
    // show a warning text at the top of the image
    let warningNode = document.createElement("div");
    let warningText = document.createTextNode(
        "Achtung, die Länge der Aufhängung wird sehr knapp mit weniger als 10 cm auf jeder Seite");
    let existingDiv = document.getElementById("imageBlock");

    warningNode.appendChild(warningText);
    existingDiv.appendChild(warningNode);
    warningNode.id = "warning-div";

    // change the color of the box for Länge Aufhängung
    changeColor("ergebnislaengeaufhaengung", "#F7820C", "#FFFFFF");
    changeColor("staticlaengeaufhaengung", "FFFFFF", "#F7820C");
}

function changeColor(id, background, color) {
    // change the color of the box for Länge Aufhängung
    let x = document.getElementById(id);
    x.style.backgroundColor = background;
    x.style.color = color;
    x.style.fontWeight = "700";
}

function removeText(id) {
    let child = document.getElementById(id);
    child.parentNode.removeChild(child);
}