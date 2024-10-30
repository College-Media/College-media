from .models import Student

def student_profile(request):
    if request.user.is_authenticated:
        try:
            # Fetch the Student instance associated with the logged-in user
            student = Student.objects.get(user=request.user)
            return {'student_profile': student}
        except Student.DoesNotExist:
            return {}  # No Student instance found
    return {}