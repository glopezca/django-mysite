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

### Controladores.

# 1. Controlador del listado de preguntas (index)

#   A) Clase

class IndexView(generic.ListView):
    template_name = 'polls/index.html' # Página que lanzaré
    context_object_name = 'latest_question_list' # Le mandaré a esa página el resultado de get_queryset() como variable de contexto
    # NOTA: El peso de los datos del controlador lo lleva la variable de contexto

    def get_queryset(self): # Devuelve un iterable con la lista de elementos que forman parte del controlador
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')#[:5]#

#    B) Función

def index(request):
    latest_question_list = Question.objects.filter(
        pub_date__lte=timezone.now()
    ).order_by('-pub_date')#[:5]# # Variable de contexto
    context = {'latest_question_list': latest_question_list}
    return render(request, 'polls/index.html', context)

# 2. Controlador de la vista en detalle de una pregunta (con sus opciones)

#   A) Clase

class DetailView(generic.DetailView):
    model = Question # Tabla de la BD principal para este controlador
    template_name = 'polls/detail.html' # Página que lanzaré
    # NOTA: El peso de los datos del controlador lo lleva el modelo (Question)
    
    def get_queryset(self): # Devuelve un iterable con la lista de elementos que forman parte del controlador
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        )

#   B) Función

def detail(request, question_id):
    question = get_object_or_404(
        Question.objects.filter(
            pub_date__lte=timezone.now()
        ), pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})    

# 3. Controlador de la vista en detalle de una pregunta (con sus opciones y resultados)

#    A) Clase

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

#    B) Función

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})

# 4. Controlador para votar (incrementar en uno el voto)

# Es una función

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice']) # Obtengo la pk de un formulario
    except (KeyError, Choice.DoesNotExist): # Si es nula (no hay selección)
        return render(request, 'polls/detail.html', { # Redirijo a esta página
            'question': question, # Variable de contexto: pregunta
            'error_message': "No has seleccionado ninguna opción.", # Variable de contexto: mensaje de error
        })
    else: # Si es válida, voto
        selected_choice.votes += 1 # Voto
        selected_choice.save() # Almaceno cambios
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,))) # Redirijo
    
# 5. Controlador para borrar una pregunta (y, en cascada, sus opciones)

# Es una clase

class QuestionDelete(generic.DeleteView):
    model = Question
    success_url = reverse_lazy('polls:index')

# 6. Controlador para añadir una pregunta con 3 opciones

#    A) Clase

class QuestionCreate(generic.FormView): 
    # Esta clase hace dos cosas:
    #    1. Si no ha recibido nada de la petición HTTP mediante el método POST, devuelve un formulario vacío
    #    2. En caso contrario, procesa el formulario y redirige a otra página

    model = Question # Tabla principal de la BD para los datos de este controlador
    form_class = QuestionCreateForm # Clase formulario definida en forms.py
    template_name = 'polls/question_create.html' # Página que incluye el formulario

    def get(self, request): # Método para enviar un formulario vacío
        form = self.form_class()
        return render(request, self.template_name, {
            'action_url': request.path, # Variable de contexto: el campo "action" del formulario
            'form': form # Variable de contexto: el formulario
        })

    def form_valid(self, form): # Método para validar los datos de un formulario relleno
        # A este método se le llama cuando se ha recibido con éxito una solicitud POST
        # Devuelve un objeto de tipo HttpResponse.
        q_text = form.cleaned_data['question_text']
        q_date = timezone.now()
        choice1 = form.cleaned_data.get('choice1', 'Sí') # choice1 = form.cleaned_data['choice1']
        choice2 = form.cleaned_data.get('choice2', 'No') # choice1 = form.cleaned_data['choice2']
        choice3 = form.cleaned_data.get('choice3', 'NS/NC') # choice1 = form.cleaned_data['choice3']
        q = self.model(question_text=q_text, pub_date=q_date)
        q.save()
        q.choice_set.create(choice_text=choice1, votes=0)
        q.choice_set.create(choice_text=choice2, votes=0)
        q.choice_set.create(choice_text=choice3, votes=0)
        return HttpResponseRedirect(reverse("polls:index"))
        #return HttpResponseRedirect(reverse("polls:detail", kwargs = {'pk': q.id,})) # Si redirijo al formulario de resultados

#   B) Función

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

#   C) Función que emplea una clase

def crea_pregunta2(request):
    controlador = QuestionCreate() # Creo la clase que implementa el controlador

    # Compruebo las solicitudes
    if request.method == 'POST': # Si ha llegado algo mediante POST:
        form = controlador.form_class(request.POST) # Obtengo los datos de la HttpRequest
        if form.is_valid(): # Si él formulario es válido, lo proceso
            return controlador.form_valid(form) # Método para procesar formulario y devolver respuesta HTTP
    # Si no ha llegado nada:
    return controlador.get(request) # Método para enviar formulario a rellenar y devolver respuesta HTTP