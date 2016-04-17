from django.shortcuts import render
from django.http import HttpResponse
from models import Url
from django.views.decorators.csrf import csrf_exempt
import urllib

# Create your views here.

def obtener_lista_URLs():
    URLs = Url.objects.all()
    lista = ""
    for url in URLs:
        lista = lista + "<p><a href=" +  url.URL_original + ">" + \
                url.URL_original + "</a>" + \
                " --> " + "<a href=" + url.URL_acortada + ">" + \
                url.URL_acortada + "</a></p>"

    return lista

@csrf_exempt
def recurso_barra(request):
    metodo = request.method
    if metodo == "GET":

        info_inicial = "<p><h2> Aplicacion web que acorta URLs</h2></p>"
        formulario = '<form action="http://localhost:8000"' + \
                    ' method="POST" accept-charset="UTF-8">' + \
                    'Introducir URL: <input type="text" name="url">' + \
                    '<input type="submit" value="Acortar"></p></form>'
        try:
            URLs = Url.objects.all()
            if len(URLs) == 0:
                info_lista_URLs = "<p><font color='green'><h4>Lista de URLs " + \
                                    "acortadas, actualmente vacia!</h4></font></p>"
                lista_URLs = ""
            else:
                info_lista_URLs = "<p><font color='green'><h4>Lista de URLs ya " + \
                                    "acortadas en este momento:</h4></font></p>" + \
                                    "<h5>(Accede, si lo deseas, a las paginas a " + \
                                    "traves de los enlaces disponibles)</h5>"
                lista_URLs = obtener_lista_URLs()

        except Url.DoesNotExist:
            http_Error = "<h3><font color='red'>Error! No existe el modelo " +\
                        "Url!</font></h3>"

        try:
            return HttpResponse(info_inicial + formulario + info_lista_URLs + \
                                lista_URLs)
        except UnboundLocalError:
            return HttpResponse(http_Error)

    elif metodo == "POST":
        URL_inicial = "http://localhost:8000/"
        info_incial = "<p><h2> Aplicacion web que acorta URLs</h2></p>"
        cuerpo = request.body
        url_cuerpo = cuerpo.split("=")[1]

        if url_cuerpo == "":
            http_Error = "<html><body><h3><font color='red'>Error: " +\
                        "Formulario no correcto! " + \
                        "Vuelve a intentarlo...</font></h3>" + \
                        "<p>Accede a la pagina incial a traves se este enlace: " + \
                        "<a href=" + URL_inicial + ">" + URL_inicial + \
                        "</p></body></html>"

            return HttpResponse(http_Error)
        else:
            url_cuerpo = urllib.unquote(url_cuerpo).decode('utf8')

            if url_cuerpo.split("://")[0] != "http" and \
                url_cuerpo.split("://")[0] != "https":

                url_cuerpo = "http://" + url_cuerpo

            try:
                URLs = Url.objects.get(URL_original=url_cuerpo)
                url_corta = URLs.URL_acortada
                info_mensaje_url_ya_acort = "<font color='red'> Esta URL ya " + \
                                            "habia sido acortada previamente. " + \
                                            "Mirar lista URL acortadas!</font>"
            except Url.DoesNotExist:
                info_mensaje_url_ya_acort = ""

                URLs = Url.objects.all()
                indice_recurso = 0
                for indice in URLs:
                    indice_recurso = indice_recurso + 1

                url_corta = "http://localhost:8000/" + str(indice_recurso)

                new_URL = Url(URL_original=url_cuerpo, URL_acortada=url_corta)
                new_URL.save()

            http_Resp = "<html><body>" + info_incial + \
                        "<p><h4>" + info_mensaje_url_ya_acort + "</h4></p>" + \
                        "<p>URL original: <a href=" + url_cuerpo + ">" + url_cuerpo + \
                        "</a> --> URL acortada: <a href=" + url_corta + ">" + \
                        url_corta + "</a></p></body></html>"

        return HttpResponse(http_Resp)

    else:
        http_Error = "<h3><font color='red'>Error! Metodo no valido.</font></h3>"
        return HttpResponse(http_Error)

def recurso_redirect(request, indice):
    URL_inicial = "http://localhost:8000/"
    url_acortada = "http://localhost:8000/" + indice
    try:
        URLs = Url.objects.get(URL_acortada=url_acortada)
    except Url.DoesNotExist:
        http_Error = "<html><body><h3><font color='red'>Error! " + \
                    "Dicha url acortada no existe en la base de datos." +\
                    "Vuelve a intentarlo...</font></h3>" + \
                    "<p>Accede a la pagina incial a traves se este enlace: " + \
                    "<a href=" + URL_inicial + ">" + URL_inicial + \
                    "</p></body></html>"

    try:
        http_Resp = '<html><head><meta http-equiv="Refresh" content="3; url=' + \
        		  URLs.URL_original + '"/></head' + \
                  '<body>Seras redirigido a la siguiente URL tras 3 segundos ' + \
                  'de espera: <b>' + URLs.URL_original + '</b></body></html>'

        return HttpResponse(http_Resp)
    except UnboundLocalError:
        return HttpResponse(http_Error)

def error(request):
    URL_inicial = "http://localhost:8000/"
    http_Error = "<h3><font color='red'>Error! Pagina no encontrada</font></h3>" +\
                "<p>Accede a la pagina incial a traves se este enlace: " + \
                "<a href=" + URL_inicial + ">" + URL_inicial + \
                "</p>"

    return HttpResponse(http_Error)
