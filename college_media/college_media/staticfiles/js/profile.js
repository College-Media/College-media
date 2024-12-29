document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.editBtn').forEach(button => {
        button.addEventListener('click', function () {
        document.getElementById('editProfileForm').style.display = 'block';
        document.getElementById('overlay').style.display = 'block';
        
    });
    });
    document.getElementById('closeButton').addEventListener('click', function () {
        document.getElementById('editProfileForm').style.display = 'none';
        document.getElementById('overlay').style.display = 'none';
    });

    document.getElementById('overlay').addEventListener('click', function () {
        document.getElementById('editProfileForm').style.display = 'none';
        document.getElementById('overlay').style.display = 'none';
        document.getElementById('overlay2').style.display = 'none';
        document.getElementById('profile-edit-pic-table').style.display='none';
    });
    document.getElementById('profile-in-edit').addEventListener('click',function(){
        document.getElementById('overlay2').style.display = 'block';
        document.getElementById('profile-edit-pic-table').style.display='block';
       
    });
    document.getElementById('cancelBtn').addEventListener('click',function(){
        document.getElementById('overlay2').style.display = 'none';
        document.getElementById('profile-edit-pic-table').style.display='none';
       
    });


    document.getElementById('overlay').addEventListener('click', function () {
        document.getElementById('editPostForm').style.display = 'none';
        document.getElementById('overlay').style.display = 'none';
        document.getElementById('overlay2').style.display = 'none';
       
    });
    document.getElementById('post-in-edit-actions').addEventListener('click',function(){
        document.getElementById('overlay2').style.display = 'block';
       
    });
    document.getElementById('cancelBtnP').addEventListener('click',function(){
        document.getElementById('editPostForm').style.display = 'none';
        document.getElementById('overlay2').style.display = 'none';
      
        document.getElementById('editPostForm').style.dispaly="none";
        document.getElementById('overlay').style.display = 'none';
    });
    let timeoutId;
    document.querySelectorAll(".div-svg-not-approve").forEach(div => {
        div.addEventListener('mouseover', function() {
            timeoutId=setTimeout(function(){
            div.querySelector(".span-svg-not-approve").style.display = "block";
         },900);
         
        });
        div.addEventListener('mouseout', function() {
            clearTimeout(timeoutId);
          div.querySelector(".span-svg-not-approve").style.display = "none";
        });
    });
    
    document.querySelectorAll('.div-svg-approve').forEach(div => {
      
      
        div.addEventListener('mouseover', function() {
          
          timeoutId = setTimeout(function() {
            div.querySelector(".span-svg-approve").style.display = "block";
          }, 890);
        });
      
        div.addEventListener('mouseout', function() {
          clearTimeout(timeoutId);
          div.querySelector(".span-svg-approve").style.display = "none";
        });
      });
      
    
});
