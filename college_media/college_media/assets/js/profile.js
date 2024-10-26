document.addEventListener('DOMContentLoaded', function () {
    document.querySelector('.editBtn').addEventListener('click', function () {
        document.getElementById('editProfileForm').style.display = 'block';
        document.getElementById('overlay').style.display = 'block';
    });

    document.getElementById('closeButton').addEventListener('click', function () {
        document.getElementById('editProfileForm').style.display = 'none';
        document.getElementById('overlay').style.display = 'none';
    });

    document.getElementById('overlay').addEventListener('click', function () {
        document.getElementById('editProfileForm').style.display = 'none';
        document.getElementById('overlay').style.display = 'none';
    });
    document.getElementById('profile-image-edit').addEventListener('click',function(){
        
        document.getElementById('profile-edit-pic-table').style.display='block';
        document.getElementById('overlay').style.display = 'block';
    });
    document.getElementById('cancelBtn').addEventListener('click',function(){
        document.getElementById('overlay2').style.display = 'block';
    });
});