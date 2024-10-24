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
});