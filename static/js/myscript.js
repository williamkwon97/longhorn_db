/**
 * 
 */

function myFunction() {
    var x,y,z, text;

    // Get the value of input field with id="numb"

    x = document.getElementById("phone").value;
    y = document.getElementById("status").value;
    z = document.getElementById("pool_type").value;

    // If x is Not a Number or less than one or greater than 10

    if (isNaN(x) || x < 1 || x > 10) {
        text = "Invalid input.";
    } else {
        text = "Correct input.";
    }
    if (isNaN(y) || y == "Closed" || y == "Open", y == "In Renovation") {
        text = "Correct input.";
    } else {
        text = "Invalid input.";
    }
    if (isNaN(z) || z == "Neighborhood" || z == "University", z == "Community") {
        text = "Correct input.";
    } else {
        text = "Invalid input.";
    }
    
    document.getElementById("demo").innerHTML = text;
    
    console.log("Testing console.");
    console.log(text);
}