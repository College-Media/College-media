
function checkCred() {
    const success = document.getElementsByClassName('SuccessCred')[0];
    const fail = document.getElementsByClassName('failCred')[0];
    
    const user = document.getElementById("username").value;
    const pass = document.getElementById("password").value;

    if (user === "X" && pass === "v") {
        fail.style.display = 'flex';
        
        
        setTimeout(function() {
            fail.style.display = 'none';
        }, 3000);
       
    } else {
        success.style.display = 'flex';
        setTimeout(function() {
            success.style.display = 'none';
        }, 3000);
       
    }
}
