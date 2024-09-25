# views.py

from django.shortcuts import render, redirect
from myapp.formys import ClientForm, ImmobileForm, RegisterLocationForm
from myapp.models import Immobile, ImmobileImage
from django.db.models import Q
from .models import Immobile, Banner

# Create your views here.
def mysite(request):
    return render(request, 'index.html')

def list_location(request):
    immobiles = Immobile.objects.filter(is_locate=False)
    banners = Banner.objects.all()  # Pega todos os banners
    context = {
        'immobiles': immobiles,
        'banners': banners  # Adiciona os banners ao contexto
    }
    return render(request, 'list-location.html', context)

def form_client(request):
    form = ClientForm() 
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list-location')   
    return render(request, 'form-client.html', {'form': form})

def form_immobile(request):
    form = ImmobileForm()
    if request.method == 'POST':
        form = ImmobileForm(request.POST, request.FILES)
        if form.is_valid():
            immobile = form.save()
            files = request.FILES.getlist('immobile')  # Pega todas as imagens
            if files:
                for f in files:
                    ImmobileImage.objects.create(  # Cria instância para imagens
                        immobile=immobile, 
                        image=f)
            return redirect('list-location')  
    return render(request, 'form-immobile.html', {'form': form})

def form_location(request, id):
    get_locate = Immobile.objects.get(id=id)  # Pega objeto
    form = RegisterLocationForm()  
    if request.method == 'POST':
        form = RegisterLocationForm(request.POST)
        if form.is_valid():
            location_form = form.save(commit=False)
            location_form.immobile = get_locate  # Salva id do imóvel 
            location_form.save() 
            # Muda status do imóvel para "Alugado"
            immo = Immobile.objects.get(id=id)
            immo.is_locate = True  # Passa a ser True
            immo.save() 
            return redirect('list-location')  # Retorna para lista
    context = {'form': form, 'location': get_locate}
    return render(request, 'form-location.html', context)

def reports(request):  # Relatórios   
    immobile = Immobile.objects.all() 
    client = request.GET.get('client')
    dt_start = request.GET.get('dt_start')
    dt_end = request.GET.get('dt_end')
    type_item = request.GET.get('type_item')
    is_locate = request.GET.get('is_locate')
    address = request.GET.get('address')

    
    if client:  # Filtra por nome e email do cliente
        immobile = Immobile.objects.filter(Q(reg_location__client__name__icontains=client) | Q(reg_location__client__email__icontains=client))
    if dt_start and dt_end:  # Por data
        immobile = Immobile.objects.filter(reg_location__create_at__range=[dt_start, dt_end])
    if type_item:  # Tipo de Imóvel
        immobile = Immobile.objects.filter(type_item=type_item) 
    if is_locate:  # Imóvel foi locado ou não
        immobile = Immobile.objects.filter(is_locate=is_locate) 
    if address:  # Filtra por nome e email do cliente
        immobile = Immobile.objects.filter(Q(reg_location__client__name__icontains=address) | Q(reg_location__client__email__icontains=address))  
        
    return render(request, 'reports.html', {'immobiles': immobile})
