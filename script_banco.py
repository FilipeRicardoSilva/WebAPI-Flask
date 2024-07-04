import mysql.connector
from mysql.connector import errorcode
from flask_bcrypt import generate_password_hash

print("Conectando no Container Docker...")
try:
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='bp1234',
        port='3307'
    )
    print("Conexão bem sucedida!")
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print('Existe algo errado no nome de usuário ou senha')
    else:
        print(err)
    exit(1)  # Encerra o script se não conseguir conectar ao banco de dados

cursor = conn.cursor()

try:
    cursor.execute("DROP DATABASE IF EXISTS `gamestory`;")
    cursor.execute("CREATE DATABASE `gamestory`;")
    cursor.execute("USE `gamestory`;")

    # criando tabelas
    TABLES = {}
    TABLES['Jogos'] = ('''
          CREATE TABLE `jogos` (
          `id` int(11) NOT NULL AUTO_INCREMENT,
          `nome` varchar(50) NOT NULL,
          `categoria` varchar(40) NOT NULL,
          `console` varchar(20) NOT NULL,
          PRIMARY KEY (`id`)
          ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;''')

    TABLES['Usuarios'] = ('''
          CREATE TABLE `usuarios` (
          `nome` varchar(20) NOT NULL,
          `nickname` varchar(8) NOT NULL,
          `senha` varchar(100) NOT NULL,
          PRIMARY KEY (`nickname`)
          ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;''')

    for tabela_nome in TABLES:
        tabela_sql = TABLES[tabela_nome]
        try:
            print('Criando tabela {}:'.format(tabela_nome), end=' ')
            cursor.execute(tabela_sql)
            print('OK')
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print('Já existe')
            else:
                print(err.msg)

    # inserindo usuarios
    usuario_sql = 'INSERT INTO usuarios (nome, nickname, senha) VALUES (%s, %s, %s)'
    usuarios = [
        ("Filipe", "FR", generate_password_hash("senha").decode('utf-8')),
    ]
    cursor.executemany(usuario_sql, usuarios)

    cursor.execute('SELECT * FROM gamestory.usuarios')
    print(' -------------  Usuários:  -------------')
    for user in cursor.fetchall():
        print(user[1])

    # inserindo jogos
    jogos_sql = 'INSERT INTO jogos (nome, categoria, console) VALUES (%s, %s, %s)'
    jogos = [
        ('Tetris', 'Puzzle', 'Atari'),
        ('God of War', 'Hack n Slash', 'PS2'),
        ('Mortal Kombat', 'Luta', 'PS2'),
        ('Valorant', 'FPS', 'PC'),
        ('Crash Bandicoot', 'Hack n Slash', 'PS2'),
        ('Need for Speed', 'Corrida', 'PS2'),
    ]
    cursor.executemany(jogos_sql, jogos)

    cursor.execute('SELECT * FROM gamestory.jogos')
    print(' -------------  Jogos:  -------------')
    for jogo in cursor.fetchall():
        print(jogo[1])

    # commitando para efetivar as operações no banco
    conn.commit()

except mysql.connector.Error as err:
    print("Erro no MySQL: {}".format(err))
finally:
    if 'conn' in locals() and conn is not None and conn.is_connected():
        cursor.close()
        conn.close()
        print("Conexão com MySQL foi fechada.")
