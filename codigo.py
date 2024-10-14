import flet as ft

# Função principal
def main(page):
    # Título
    titulo = ft.Text("Hashzap")
    page.add(titulo)
    
    # Campo para o nome do usuário
    cx_nome = ft.TextField(label="Digite seu nome")

    # Coluna que armazenará as mensagens do chat
    chat = ft.Column()

    # Função que lida com as mensagens recebidas via pubsub
    def receber_mensagem(mensagem):
        tipo = mensagem["tipo"]
        if tipo == "mensagem":
            nome_usuario = mensagem["usuario"]
            texto_mensagem = mensagem["texto"]
            chat.controls.append(ft.Text(f"{nome_usuario}: {texto_mensagem}"))
        elif tipo == "entrada":
            nome_usuario = mensagem["usuario"]
            chat.controls.append(ft.Text(f"{nome_usuario} entrou no chat!", italic=True, color=ft.colors.ORANGE_500))
        page.update()

    # Subscreve a função para receber mensagens via pubsub
    page.pubsub.subscribe(receber_mensagem)

    # Função para enviar uma mensagem
    def enviar_msg():
        nome_usuario = cx_nome.value
        texto_campo_msg = campo_enviar_msg.value
        if texto_campo_msg:
            # Publica a mensagem para todos os usuários
            page.pubsub.send_all({"tipo": "mensagem", "usuario": nome_usuario, "texto": texto_campo_msg})
            campo_enviar_msg.value = ""  # Limpa o campo de texto após o envio
            page.update()

    # Campo para enviar mensagem e botão de envio
    campo_enviar_msg = ft.TextField(label="Digite aqui a sua mensagem", on_submit=lambda e: enviar_msg())
    btn_enviar = ft.ElevatedButton("Enviar", on_click=lambda e: enviar_msg())

    # Linha que contém o campo de envio de mensagem e o botão enviar
    linha_enviar = ft.Row([campo_enviar_msg, btn_enviar])

    # Função para abrir o popup de entrada de nome
    def abrir_popup(evento):
        titulo_popup = ft.Text("Bem-vindo ao Hashzap")
        btn_popup = ft.ElevatedButton("Entrar no chat", on_click=lambda e: entrar_chat())
        popup = ft.AlertDialog(title=titulo_popup, content=cx_nome, actions=[btn_popup])
        
        # Atribuir o popup à página e mostrar o diálogo
        page.dialog = popup
        popup.open = True
        page.update()

    # Função para entrar no chat
    def entrar_chat():
        # Publica a entrada do usuário para todos os conectados
        page.pubsub.send_all({"tipo": "entrada", "usuario": cx_nome.value})
        page.dialog.open = False
        page.remove(titulo)
        page.remove(botao)
        page.add(chat)
        page.add(linha_enviar)
        page.update()

    # Botão para abrir o popup
    botao = ft.ElevatedButton("Iniciar Chat", on_click=abrir_popup)
    page.add(botao)

# Iniciar a aplicação
ft.app(target=main, view=ft.AppView.WEB_BROWSER)