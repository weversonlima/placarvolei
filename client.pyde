import socket 


#conexao socket cliente
sock = socket(AF_INET,SOCK_STREAM) # Criação do socket
sock.connect(('localhost',23003)) # Conexão com o servidor
# Envia a mensagem

#importa a biblioteca que cuida da GUI
add_library('controlP5')

#Classe que trata as excecoes
class TextListener(ControlListener):

    #metodo que trata quando o botão enviar é pressionado
    def controlEvent(self, e):
        a = e.getName()
        print '%s -> %s' % (e.getName(), e.getStringValue())
        if(a == 'enviar'):
            print(e.getName())
            envia()

#parametros iniciais
def setup():
    size(700, 400)
    font = createFont("sansserif", 20)
    global cp5
    #instanciando objeto da classe ControlP5
    cp5 = ControlP5(this)
    
    #criacao dos campos de texto
    cp5.addTextfield("input").setPosition(20, 100).setSize(
        200, 40).setFont(font).setFocus(True).setColor(color(255, 0, 0))

    cp5.addTextfield("textValue").setPosition(20, 170).setSize(
        200, 40).setFont(createFont("arial", 20)).setAutoClear(False)
    # criacao do botao
    cp5.addBang("enviar").setPosition(240, 170).setSize(
        80, 40).getCaptionLabel().align(ControlP5.CENTER, ControlP5.CENTER)

    textFont(font)

    cp5.getController("enviar").addListener(TextListener())
    
# funcao de desenho principal
def draw():
    background(0)
    fill(255)
    text(cp5.get(Textfield, "input").getText(), 360, 130)
    text(cp5.get(Textfield, "textValue").getText(), 360, 180)

#action do botao
def envia():
    global sock
    #pega valor do campo input
    time = (cp5.get(Textfield, "input").getText())
    tipo_ponto = (cp5.get(Textfield, "textValue"))
    cp5.get(Textfield, "input").clear()
    cp5.get(Textfield, "textValue").clear()
    sock.send (str(time) + ", " + str(tipo_ponto))