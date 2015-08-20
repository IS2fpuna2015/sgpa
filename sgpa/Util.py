from django.core.mail import send_mail
from reportlab.lib.pagesizes import  cm
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from sgpa.settings import MEDIA_URL

def generarcodigo(id, codigo_proyecto):
    return codigo_proyecto + "-" + str(id)


def enviar_notificacion(asunto, mensaje , destinatario, remitente):
    try:
        send_mail(asunto, mensaje,remitente,
                  [destinatario], fail_silently=True)
        return True
    except:
        return False

def usuario_es_scrum_de_proyecto(usuario,proyecto):
    return proyecto.scrum_master.id==usuario.id

def usuario_es_desarrollador_asignado(usuario,userstory):
    return userstory.usuario_asignado.id==usuario.id

def usuario_es_Administrador(usuario):

    if usuario.groups.filter(name='Administrador').exists():
        return True
    else:
        return False

def cabecera_alpie(canvas,doc):
    canvas.saveState()
    canvas.drawString(1 * cm, 27 * cm,'Grupo R07')
    canvas.drawString(1 * cm, 26.5 * cm,'Ingenieria de Software II')
    canvas.restoreState()

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        canvas.Canvas.__init__(self, *args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        """add page info to each page (page x of y)"""
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_number(self, page_count):
        self.setFont("Helvetica", 7)
        self.drawRightString(200*mm, 20*mm,
            "Pagina %d of %d" % (self._pageNumber, page_count))
