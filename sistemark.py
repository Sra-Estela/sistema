from tkinter import *

import requests
from datetime import datetime
import pickle
import sqlite3
import json

import pytz

from googletrans import Translator
#pip install googletrans==4.0.0-rc1

class App_Clima:
    def __init__(self):
        self.janela = Tk()
        self.janela.title('SISTEMA DE TEMPO')
        self.janela.geometry('660x330')
        self.janela.iconbitmap('icon(1).ico')

        self.janela['bg'] = 'white'
        # Frames
        self.conteiner = Frame(self.janela, bg='#D3D3D3', width=660, height=330, highlightbackground="black", highlightthickness=1)
        self.conteiner.place(x=0, y=0)

        self.frame1 = Frame(self.conteiner, bg='#B0C4DE', width=380, height=329, highlightbackground="black", highlightthickness=1)
        self.frame1.place(x=279, y=0)

        # Labels
        self.dia = Label(self.conteiner, bg='#D3D3D3', text='Nomeie o Arquivo:', width=20, height=1, padx=7, anchor='w', font=('Arial 14 bold'))
        self.dia.place(x=10, y=15)

        self.label2 = Label(self.frame1, bg='#B0C4DE', fg='black', text='D/M/A | H:M:S p', font=('Arial 14 bold')) #Horário
        self.label2.place(x=40, y=20)

        self.label3 = Label(self.frame1, bg='#B0C4DE', fg='black', text='Caicó-RN\n59300-000', font=('Arial 14 bold'))
        self.label3.place(x=240, y=20)

        # informações
        self.label4 = Label(self.frame1, bg='white', fg='black', width=12, height=2, text='Temperatura', anchor='center', font=('Arial 14')) #Temperatura
        self.label4.place(x=220, y=80)

        self.label5 = Label(self.frame1, bg='white', fg='black', width=12, height=2, text='Umidade', anchor='center', font=('Arial 14')) #Umidade
        self.label5.place(x=220, y=140)

        self.label6 = Label(self.frame1, bg='white', fg='black', width=12, height=2, text='Pressão', anchor='center', font=('Arial 14')) #Pressão
        self.label6.place(x=220, y=200)

        self.label7 = Label(self.frame1, bg='white', fg='black', width=37, height=2, text='<Descrição do tempo>', anchor='center', font=('Arial 12'), borderwidth=1, relief="solid") #Descrição
        self.label7.place(x=20, y=266)

        self.imagem = PhotoImage(file='imagem.png').subsample(10)
        self.imagem1 = PhotoImage(file='imagem(1).png').subsample(10)
        self.label8 = Label(master= self.frame1, image= self.imagem, bg='#B0C4DE')
        self.label8.place(x=10, y=70)

        self.label9 = Label(self.conteiner, bg='white', width=35, height=2, borderwidth=2, relief="solid")
        self.label9.place(x=15, y=53)

        # Input
        self.caixa1 = Entry(self.conteiner, width=39, highlightbackground="white", highlightthickness=1)
        self.caixa1.place(x=20, y=60) #Dia

        # Button
        self.b_apagar = Button(self.conteiner, width=12, height=1, bg='#FF6347',  text='⌫', font=('Arial 10 bold'), command=self.apagar)
        self.b_apagar.place(x=20, y=105)

        self.b_ok = Button(self.conteiner, width=14, height=1, bg='#90EE90',  text='OK', font=('Arial 10 bold'), command=self.coleta_dados)
        self.b_ok.place(x=140, y=105)

        self.botao1 = Button(self.conteiner, width=29, height=2, bg='#C0C0C0',  text='INSERIR', font=('Arial 10 bold'), command=self.inserir_dic)
        self.botao1.place(x=20, y=150)

        self.botao2 = Button(self.conteiner, width=29, height=2, bg='#C0C0C0',  text='CONSULTAR', font=('Arial 10 bold') , command=lambda: [self.informacao(), self.decoracao()],)
        self.botao2.place(x=20, y=200)

        self.botao3 = Button(self.conteiner, width=29, height=2, bg='#C0C0C0',  text='EXCLUIR', font=('Arial 10 bold'), command=self.excluir)
        self.botao3.place(x=20, y=250)

        self.janela.mainloop()
    
    # Função que retorna as informações:

    def informacao (self):

        self.chave = 'ac1e36a5348d22ffd8bb5b70d312f40f'
        self.cidade = 'Caicó'
        self.api_link = (f'https://api.openweathermap.org/data/2.5/weather?q={self.cidade}&appid={self.chave}')

        # Chamando API com o request

        self.r = requests.get(self.api_link)

        self.dados = self.r.json()

        print(self.dados)
        print('=*'*30)

        # Obtendo a zona e as horas
        self.pais_codigo = self.dados['sys']['country']
        print(self.pais_codigo)

        self.zona_fuso = pytz.country_timezones[self.pais_codigo]

        self.zona =  pytz.timezone(self.zona_fuso[3])

        self.zona_horas = datetime.now(self.zona)
        self.zona_horas = self.zona_horas.strftime("%d/%m/%Y\n%H:%M:%S %p")

        print(self.zona_horas)

        self.checagem = int(self.zona_horas[11] + self.zona_horas[12])

        self.tempo = int(self.dados['main']['temp']-273.15)
        self.pressao = self.dados['main']['pressure']
        self.humidade = self.dados['main']['humidity']
        self.descricao = self.dados['weather'][0]['description']

        # Informações dos Label:
        self.label4['text'] = (f'{self.tempo}°C')
        self.label2['text'] = self.zona_horas
        self.label6['text'] = (f'{self.humidade}%')
        self.label5['text'] = (f'{self.pressao}hPa')

        self.tradutor = Translator()
        self.linguagem = 'pt'

        self.text_traduzido = self.tradutor.translate(self.descricao, dest=self.linguagem)

        self.label7['text'] = self.text_traduzido.text

        self.lista_c = []
        self.lista_d = []

        for i in range(0, 10):
            self.lista_c.append(self.zona_horas[i])
            self.data = ''.join(self.lista_c)
            
        for c in range(12, 22):
            self.lista_d.append(self.zona_horas[c])
            self.horario = ''.join(self.lista_d)

        self.tupla = ('Cidade', 'Dia', 'Horário', 'Temperatura', 'Umidade', 'Pressão', 'Descrição', 'Média')

        self.lista = [0]*8
        self.lista[0] = self.cidade
        self.lista[1] = self.data
        self.lista[2] = self.horario
        self.lista[3] = (f'{self.tempo}°C')
        self.lista[4] = (f'{self.humidade}%')
        self.lista[5] = (f'{self.pressao}hPa')
        self.lista[6] = self.text_traduzido.text
        self.lista[7] = '27,5°C'

        self.op = 'consultar'

        return

    def decoracao (self):

        if self.checagem < 18:
            self.label8['image'] = self.imagem
            self.frame1['bg'] = '#B0C4DE'
            self.label2['bg'] = '#B0C4DE'
            self.label3['bg'] = '#B0C4DE'
            self.label8['bg'] = '#B0C4DE' 
            self.label2['fg'] = 'black'
            self.label3['fg'] = 'black'
            self.label7['font'] = ('Arial 12')
            self.label7['width'] = 37
            self.label7['fg'] = 'black'
        else:
            if self.checagem > 18:
                self.label8['image'] = self.imagem1
                self.frame1['bg'] = '#0D0033'
                self.label2['bg'] = '#0D0033'
                self.label3['bg'] = '#0D0033'
                self.label8['bg'] = '#0D0033'
                self.label2['fg'] = 'white'
                self.label3['fg'] = 'white'
                self.label7['font'] = ('Arial 12')
                self.label7['width'] = 37
                self.label7['fg'] = 'black'

        return
    
    # Coletor dos dados e criador de arquivo.json
    def coleta_dados(self):

        # self.tupla = ('Cidade', 'Dia', 'Horário', 'Temperatura', 'Umidade', 'Pressão', 'Descrição')
        # self.lista = ['Caicó', '25/12/2023', '6:39:20 PM', '34°C', '37%', '1010hPa', 'nuvens quebradas']
        self.dicionario = {}
        try:
            for i in range(0, 8):
                self.dicionario[self.tupla[i]] = self.lista[i]

        except AttributeError:
            print('É necessário "CONSULTAR" os dados primeiro.')
            self.label7['text'] = 'É necessário "CONSULTAR" os dados primeiro.'
            self.label7['fg'] = 'red'
            self.label7['font'] = ('Arial 11 bold')
            self.label7['width'] = 38

        try:
            self.variavel = self.caixa1.get() + '.db'
            self.arquivo = open(self.variavel, 'ab')
            pickle.dump(self.dicionario, self.arquivo)
        
        except FileNotFoundError:
            print("Arquivo não encontrado.")

        return
    
    # Inserir o dicionário no arquivo json

    def inserir_dic (self):

        self.arquivo = open(self.variavel, 'wb') #arq = open('agenda.json','w')
        pickle.dump(self.dicionario, self.arquivo)

        self.arquivo = open(self.variavel, 'wb') #arq = open('agenda.json','w')
        pickle.dump(self.dicionario, self.arquivo)

        self.arquivo = open(self.variavel, 'rb')
        self.agenda = pickle.load(self.arquivo)
        print(self.agenda)

        self.op = 'inserir'

    # Modo SQLite
    def ok(self):
        try:
            if self.op == 'inserir':
                con = sqlite3.connect(self.variavel)
                sql = con.cursor()
                sql.execute('INSERT INTO registros (nome,telefone) VALUES (?,?)',(self.caixa1.get()))
                con.commit()
                con.close()
                self.op = ''
            elif self.op == 'consultar':
                con = sqlite3.connect(self.variavel)
                sql = con.cursor()
                sql.execute('SELECT * FROM registros WHERE nome = ?',(self.caixa1.get(),))
                resultado = sql.fetchone()
                self.caixa1.insert(0,resultado[1])
        except:
            print('')

    def apagar(self):
        if self.caixa1.get():
            self.caixa1.delete(len(self.caixa1.get())-1)

    def excluir(self):
        self.arquivo = open(self.variavel, 'w')
        self.arquivo.write('{}')
    
aplicacao=App_Clima()

contador = 0

while True:
    if contador != 5:
        print('Feliz Natal e próspero Ano Novo!!!')
        contador += 1