from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from polls.models import Question, Choice
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import generic

# Create your views here.
class IndexView(generic.ListView):
    model = Question
    context_object_name = "latest_question_list"
    template_name = "polls/index.html"

    def get_queryset(self):
        return Question.objects.order_by('-pub_date')[:5]
    

class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"

class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"

def vote(request: HttpRequest, question_id: int):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        return render(
            request,
            "polls/detail.html",
            {"question": question, "error_message": "You didn't select a choice"},
        )
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse("polls:results", args=(question_id,)))