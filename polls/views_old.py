from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import timezone
from django.utils.html import escape
#from django.template import loader
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views import generic

from .models import Question
from .forms import QuestionCreateForm

# Create your views here.

def index(request):
    #return HttpResponse(escape("Hola, mundo. Estás en el polls index."))
    latest_question_list = Question.objects.order_by('-pub_date')#[:5]#
    #output = ', '.join([q.question_text for q in latest_question_list])
    #return HttpResponse(output)
    context = {'latest_question_list': latest_question_list}
    ##template = loader.get_template('polls/index.html')
    ##return HttpResponse(template.render(context, request))
    return render(request, 'polls/index.html', context)

def detail(request, question_id):
    #return HttpResponse(escape("Estás consultando la pregunta %s." % question_id))
    ##try:
    ##    question = Question.objects.get(pk=question_id)
    question = get_object_or_404(Question, pk=question_id)
    ##except Question.DoesNotExist:
    ##    raise Http404("La pregunta no existe")
    return render(request, 'polls/detail.html', {'question': question})    

def results(request, question_id):
    #response = "Estás consultando la respuesta a la pregunta %s."
    #return HttpResponse(escape(response % question_id))
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "No has seleccionado ninguna opción.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
    
class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last #five# published questions."""
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')#[:5]#

class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'
    
    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

class QuestionDelete(generic.DeleteView):
    model = Question
    success_url = reverse_lazy('polls:index')

class QuestionCreate(generic.FormView): # Forma recomendada
    model = Question
    form_class = QuestionCreateForm
    template_name = 'polls/question_create.html'

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'action_url': request.path, 'form': form})

    def form_valid(self, form):
        # A este método se le llama cuando se ha recibido con éxito una solicitud POST
        # Devuelve un objeto de tipo HttpResponse.
        q_text = form.cleaned_data['question_text']
        q_date = timezone.now()
        choice1 = form.cleaned_data['choice1']
        choice2 = form.cleaned_data['choice2']
        choice3 = form.cleaned_data['choice3']
        q = self.model(question_text=q_text, pub_date=q_date)
        q.save()
        q.choice_set.create(choice_text=choice1, votes=0)
        q.choice_set.create(choice_text=choice2, votes=0)
        q.choice_set.create(choice_text=choice3, votes=0)
        return HttpResponseRedirect(reverse("polls:index"))
        #return HttpResponseRedirect(reverse("polls:detail", kwargs = {'pk': q.id,})) # Si redirijo a los votos

def crea_pregunta1(request):
    template_name = 'polls/question_create.html'

    form = QuestionCreateForm() ## Un formulario vacío listo para rellenar
    # Compruebo las solicitudes
    if request.method == 'POST':
        form = QuestionCreateForm(request.POST) ## Obtener datos de la HttpRequest
        if form.is_valid():
            # Procesar formulario
            # A este método se le llama cuando se ha recibido con éxito una solicitud POST
            # Devuelve un objeto de tipo HttpResponse.
            q_text = form.cleaned_data['question_text']
            q_date = timezone.now()
            choice1 = form.cleaned_data['choice1']
            choice2 = form.cleaned_data['choice2']
            choice3 = form.cleaned_data['choice3']
            q = Question(question_text=q_text, pub_date=q_date)
            q.save()
            q.choice_set.create(choice_text=choice1, votes=0)
            q.choice_set.create(choice_text=choice2, votes=0)
            q.choice_set.create(choice_text=choice3, votes=0)
            return HttpResponseRedirect(reverse("polls:index"))
    # Si el formulario está vacío:
    return render(request, template_name, {'action_url': request.path, 'form': form})


def crea_pregunta2(request):
    controlador = QuestionCreate()

    # Compruebo las solicitudes
    if request.method == 'POST':
        # form = QuestionCreateForm(request.POST) ## Obtener datos de la HttpRequest
        form = controlador.form_class(request.POST)
        if form.is_valid():
            # Procesar formulario
            return controlador.form_valid(form)
    # Si el formulario está vacío:
    return controlador.get(request)
