from django.shortcuts import render
from django.core.paginator import Paginator

# Create your views here.
QUESTIONS = [
        {
        'id': i,
        'title': f'Question {i}',
        'content': f'dgjsudfg {i}'
    } for i in range (20)
    ]

def paginate(objects, page, per_page=15):
    paginator = Paginator(objects, per_page)
    #page_items = paginator.page(1).object_list
    return paginator.page(page)
def index(request):

    page = request.GET.get('page', 1)

    return render(request, "index.html", {'questions': paginate(QUESTIONS, page)})


def question(request, question_id):
    item = QUESTIONS[question_id]
    return render(request, "question.html", {'question': item})
