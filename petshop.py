# bibliotecas
import mysql.connector
import smtplib
import email.message
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# conectar com banco de dados mySQL 
def connect_db():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="petshop"
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error connecting to the database: {err}")
        return None

# cria a tabela 'pets' no banco de dados (essa parte do código roda apenas 1x)
def create_table():
    connection = connect_db()
    if connection:
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS pet (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nome_dono VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL,
                especie VARCHAR(255) NOT NULL,
                raca VARCHAR(255) NOT NULL,
                nome_pet VARCHAR(255) NOT NULL,
                data_nascimento DATE NOT NULL,
                vacina VARCHAR(3) NOT NULL,
                prox_vacina DATE NOT NULL
            )
        """)
        connection.commit()
        connection.close()

# função para adicionar um novo registro
def add_pet():
    nome_dono = input("nome do Dono: ")
    email = input("Email: ")
    especie = input("Espécie: ")
    raca = input("Raça: ")
    nome_pet = input("Nome do Pet: ")
    data_nascimento = input("Data de nascimento (AAAA-MM-DD): ")
    vacina = input("Qual vacina tomou?: ")
    prox_vacina = input("Data da próxima vacina (AAAA-MM-DD): ")

    connection = connect_db()
    if connection:
        cursor = connection.cursor()
        cursor.execute("""
            INSERT INTO pet (nome_dono, email, especie, raca, nome_pet, data_nascimento, vacina, prox_vacina)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (nome_dono, email, especie, raca, nome_pet, data_nascimento, vacina, prox_vacina))
        connection.commit()
        connection.close()
        print("\nPet adicionado com sucesso!")

# função para alterar um registro
def edit_pet():
    id_pet = input("Digite o ID do pet que você quer editar: ")
    new_pet_name = input("Novo nome do Pet: ")
    new_birth_date = input("Nova data de nascimento do Pet (AAAA-MM-DD): ")
    new_vaccination = input("Nova vacina tomada: ")
    new_next_vaccination = input("Nova data de vacinação do Pet (AAAA-MM-DD): ")

    connection = connect_db()
    if connection:
        cursor = connection.cursor()
        cursor.execute("""
            UPDATE pet
            SET nome_pet = %s, data_nascimento = %s, vacina = %s, prox_vacina = %s
            WHERE id = %s
        """, (new_pet_name, new_birth_date, new_vaccination, new_next_vaccination, id_pet))
        connection.commit()
        connection.close()
        print("\nPet atualizado com sucesso!")

# função para excluir um registro
def delete_pet():
    id_pet = input("Digite o ID do pet que deseja excluir: ")

    connection = connect_db()
    if connection:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM pet WHERE id = %s", (id_pet,))
        connection.commit()
        connection.close()
        print("\nPet excluído com sucesso!")

# função para listar todos os registros já feitos
def list_pets():
    connection = connect_db()
    if connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM pet")
        pet = cursor.fetchall()
        connection.close()

        if len(pet) == 0:
            print("Nenhum pet encontrado.")
        else:
            print("Listas de pets:") 
            for pet in pet:
                print(f"ID: {pet[0]}, Dono: {pet[1]}, Email: {pet[2]}, Espécie: {pet[3]}, Raça: {pet[4]}, Nome do Pet: {pet[5]}, Data de nascimento: {pet[6]}, Vacina: {pet[7]}, Próxima Vacina: {pet[8]}\n")

# Funçao que pede o ID e dispara o envio dos dados para o email do dono do pet
def send_data_by_email():
    id_pet = input("Digite o ID do pet para enviar os dados para o dono: ")

    connection = connect_db()
    if connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM pet WHERE id = %s", (id_pet,))
        pet = cursor.fetchone()
        connection.close()

        if pet:
            enviar_email(pet)
        else:
            print("Pet não encontrado!")

# Função para enviar email para o dono do pet
def enviar_email(pet):
    # SMTP server settings
    smtp_server = "smtp.office365.com"  # troque pro seu servidor SMTP
    smtp_port = 587  # Digite aqui a porta do servidor SMTP
    smtp_user = "petshopplanaltina@hotmail.com"  # Coloque o email da estabelecimento
    smtp_password = "petshop123"  # insira a senha do email do estabelecimento

    # pega o email do dono e armazena na variável recipient
    recipient = pet[2]

    # configuração de msg do email
    subject = "Dados do seu pet"
    message = MIMEMultipart()
    message["From"] = smtp_user
    message["To"] = recipient
    message["Subject"] = subject

    # corpo do email
    body_message = f"Dono: {pet[1]}\nEspécie: {pet[3]}\nRaça: {pet[4]}\nNome do Pet: {pet[5]}\nData de Nascimento: {pet[6]}\nQual vacina tomou?: {pet[7]}\nPróxima vacinação: {pet[8]}"
    message.attach(MIMEText(body_message, "plain"))

    # conectar ao servidor SMTP
    try:
        smtp_server = smtplib.SMTP(smtp_server, smtp_port)
        smtp_server.starttls()
        smtp_server.login(smtp_user, smtp_password)
    except smtplib.SMTPException as e:
        print(f"Error ao conectar ao servidor SMTP: {e}")
        return

    # exibe msg se email foi enviado ou não
    try:
        smtp_server.sendmail(smtp_user, recipient, message.as_string())
        print("\nEmail enviado com sucesso!")
    except smtplib.SMTPException as e:
        print(f"\nError ao enviar email: {e}")

    # fecha a conexão com o serrvidr SMTP
    smtp_server.quit()


# menu principal
while True:
    print("\nMENU:")
    print("1 - Cadastrar")
    print("2 - Editar informações")
    print("3 - Excluir")
    print("4 - Listar Pets")
    print("5 - Enviar dados por email")
    print("0 - SAIR")
    option = input("Escolha uma opção: ")

    if option == "1":
        add_pet()
    elif option == "2":
        edit_pet()
    elif option == "3":
        delete_pet()
    elif option == "4":
        list_pets()
    elif option == "5":
        send_data_by_email()
    elif option == "0":
        print("Saindo do sistema.")
        break
    else:
        print("Opção INVÁLIDA!. Tente novamente.")




"""
DADOS PARA USAR

nome do database: petshop

nome da tabela: pet

email: petshopplanaltina@hotmail.com

senha: petshop123

"""