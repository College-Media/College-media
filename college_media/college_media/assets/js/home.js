function fun1() {
  var menuTable = document.querySelector("#post-menu-table");
  var rightContainer = document.querySelector(".right");

  // Show the menu and overlay, disable scroll on right container
  menuTable.style.display = "block";
  document.getElementById('overlay').style.display = 'block';
  rightContainer.style.overflow = "hidden"; // Disable scrolling
}

function fun() {
  var menuTable = document.querySelector("#post-menu-table");
  var rightContainer = document.querySelector(".right");

  // Hide the menu and overlay, re-enable scroll on right container
  menuTable.style.display = "none";
  document.getElementById('overlay').style.display = 'none';
  rightContainer.style.overflow = "auto"; // Enable scrolling
}
