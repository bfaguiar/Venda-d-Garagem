
from django.shortcuts import render


def index(request):
    # aqui aparece lista de carros com os detalhes: id (marca,modelo,versão), wheel drive, horse power, aceleração, consumo, cor e preço
    return render(request, 'index.html')


def login(request):
    # username id = "user"
    # password id = "pass"
    # login id = "login"
    return render(request, 'login.html')


def loginreq(request):
    # Este é só para redireccionar para a página do login caso não tenha login feito
    return render(request, 'loginreq.html')


def signup(request):
    # username id = "user"
    # email id = "email"
    # password id = "pass"
    # register id = "register"
    return render(request, 'signup.html')


def motos(request):
    # Não sei se querem por motos também
    return render(request, 'motos.html')


def profile(request):
    # Aqui aparece nome, email e anúncios feitos pelo próprio

    # ADICIONAR ANUNCIO DE CARRO
    # id do carro id = "id"
    # cor do carro id = "color"
    # preço do carro id = "price"
    # adicionar anuncio id = "announce"
    return render(request, 'profile.html')


def friends(request):
    # Aqui aparece nome, email e anúncios feitos por cada amigo

    # ADICIONAR AMIGO
    # nome do amigo id = "name"
    # email do amigo id = "email"
    # adicionar amigo id = "add"
    # Se não existir dizer que não existe
    return render(request, 'friends.html')
