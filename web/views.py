from django.shortcuts import render
from django.http import Http404
from .forms import AreaForm
from django.template import RequestContext, loader
from django.http import HttpResponse
from web.models import Entrada, Area
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.core.urlresolvers import reverse

# Create your views here.
def index(request):
    lista_ultimas_entradas = Entrada.objects.order_by('-fecha')[:4]
    areas = Area.objects.all()
    template = loader.get_template('noticias/index.html')
    context = RequestContext(request, {
        'lista_ultimas_entradas': lista_ultimas_entradas,
        'areas': areas,
    })
    return HttpResponse(template.render(context))

def about(request):
    # TODO
    # sobran datos
    lista_ultimas_entradas = Entrada.objects.order_by('-fecha')[:4]
    areas = Area.objects.all()
    template = loader.get_template('noticias/about.html')
    context = RequestContext(request, {
        'lista_ultimas_entradas': lista_ultimas_entradas,
        'areas': areas,
    })
    return HttpResponse(template.render(context))

def contact_view(request):
    template = loader.get_template('noticias/contacts.html')
    context = RequestContext(request, {
        # no info
    })
    return HttpResponse(template.render(context))

def faq_view(request):
    template = loader.get_template('noticias/preguntas_frecuentes.html')
    context = RequestContext(request, {
        # no info
    })
    return HttpResponse(template.render(context))

def politica_privacidad(request):
    # TODO
    template = loader.get_template('noticias/politica_privacidad.html')
    context = RequestContext(request, {})
    return HttpResponse(template.render(context))

def entrada(request, entrada_id):
    try:
        entrada = Entrada.objects.get(id=entrada_id)
    except Entrada.DoesNotExist:
        raise Http404("La entrada no existe")
    entradaActual = Entrada.objects.order_by('-fecha')[:5]
    template = loader.get_template('noticias/noticia.html')
    context = RequestContext(request, {
        'entrada': entrada,
    })
    return HttpResponse(template.render(context))

#def detail(request, question_id):
    #question = get_object_or_404(Question, pk=question_id)
    #return render(request, 'polls/detail.html', {'question': question})

def area(request, area):
    try:
        areaObject = Area.objects.get(nombre=area)
    except Area.DoesNotExist:
        raise Http404("El area no existe")
    try:
        entradas = Entrada.objects.filter(id_area=areaObject.id).order_by('-fecha')
    except Entrada.DoesNotExist:
        raise Http404("La entrada no existe")

    template = loader.get_template('noticias/area.html')
    context = RequestContext(request, {
        'area': areaObject,
        'entradas': entradas
    })
    return HttpResponse(template.render(context))

@login_required
def areasAdmin_view(request):
    areas = Area.objects.all()
    template = loader.get_template('noticias/areasAdmin.html')
    context = RequestContext(request, {
        'areas': areas,
    })
    return HttpResponse(template.render(context))

@login_required
def entradasAdmin_view(request):
    return render(request, 'noticias/entradasAdmin.html')



def createArea_view(request):
    if request.method == 'POST':
        # Si el method es post, obtenemos los datos del formulario
        form = AreaForm(request.POST)

        # Comprobamos si el formulario es valido
        if form.is_valid():
            # En caso de ser valido, obtenemos los datos del formulario.
            # form.cleaned_data obtiene los datos limpios y los pone en un
            # diccionario con pares clave/valor, donde clave es el nombre del campo
            # del formulario y el valor es el valor si existe.
            cleaned_data = form.cleaned_data
            nombre_data = cleaned_data.get('nombre')
            # E instanciamos un objeto Area
            area_model = Area()
            area_model.nombre = nombre_data
            area_model.save()
            # Ahora, redireccionamos a la pagina accounts/gracias.html
            # Pero lo hacemos con un redirect.
            return redirect(reverse('web.areasAdmin'))
    else:
        # Si el mthod es GET, instanciamos un objeto RegistroUserForm vacio
        form = AreaForm()
    # Creamos el contexto
    context = {'form': form}
    # Y mostramos los datos
    return render(request, 'noticias/createArea.html', context)