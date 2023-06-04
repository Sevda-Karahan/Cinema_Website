from django.shortcuts import render
from django.shortcuts import render
from .forms import FeedbackForm
# Create your views here.

def submit_feedback(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.author = request.user
            feedback.save()
            return render(request, 'feedback/feedback_success.html')
    else:
        form = FeedbackForm()
    return render(request, 'feedback/submit_feedback.html', {'form': form})

def feedback_success(request):
    return render(request, 'feedback/feedback_success.html')