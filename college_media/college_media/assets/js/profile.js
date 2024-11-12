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
    document.querySelectorAll('.post').forEach(img => {
        img.addEventListener('click', function () {
        document.getElementById('editProfileForm').style.display = 'block';
        document.getElementById('overlay').style.display = 'block';
        
    });
    });
   
});