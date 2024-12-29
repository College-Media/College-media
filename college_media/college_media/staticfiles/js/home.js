document.addEventListener("DOMContentLoaded", () => {
  var menuTable = document.querySelector("#post-menu-table");
  var rightContainer = document.querySelector(".right");
 
  document.querySelector('.post-menu-icon').addEventListener('click',()=>{
    menuTable.style.display = "block";
    document.getElementById('overlay').style.display = 'block';
    rightContainer.style.overflow = "hidden";
  });
  document.querySelector(".cancelBtnHome").addEventListener('click',()=>{
    document.querySelector("#post-menu-table").style.display = 'none';
    console.log('hidden');
    document.getElementById('overlay').style.display = 'none';
    document.querySelector(".right").style.overflow = "auto"; // Enable scrolling
 
  });
});
// function fun1() {
  

//   // Show the menu and overlay, disable scroll on right container
//   // Disable scrolling
// }

// function fun() {
//   // var menuTable = document.querySelector("#post-menu-table");
//   // var rightContainer = document.querySelector(".right");

//   // Hide the menu and overlay, re-enable scroll on right container
//   menuTable.style.display = "none";
//   document.getElementById('overlay').style.display = 'none';
//   rightContainer.style.overflow = "auto"; // Enable scrolling
// }
