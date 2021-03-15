def Miller_Rabin(n,b):
  """
  Retorna True se o teste de Miller--Rabin para n com base b **prova**
  que n é composto, False nos outros casos
  """  
  b %= n
  if b <= 1:
    return False
  
  q = n-1
  k = 0
  while q%2 == 0:
    k += 1
    q //= 2
  
  R = pow(b,q,n)
  if R==1 or R==n-1:
    return False

  i = 0
  while True:
    R = pow(R,2,n)
    i += 1
    if R == 1:
      return True
    if i == k:
      return True
    if R == n-1:
      return False

def Euclides_estendido(a,b):

  Dividendo, Divisor = a,b
  x_ant, y_ant = 1,0
  x_novo, y_novo = 0,1
  while Divisor != 0:
    Quociente, Resto = divmod(Dividendo, Divisor)
    x_ant, x_novo = x_novo, (x_ant - x_novo*Quociente)
    y_ant, y_novo = y_novo, (y_ant - y_novo*Quociente)
    Dividendo, Divisor = Divisor, Resto
  return x_ant

from random import randint
def gerar_n_primo(n):
  """
  Recebe natural n e gera um numero possivelmente primo por miller-rabin satisfazendo 10^n < p < 10^n+2
  e gera um numero p que será testado 10x em bases b aleatórias tal que 1 < b < p-1
  """
  p=0
  bases_usadas= []
  base_atual = 0
  i = 10
  while len(bases_usadas) != 10:
    while i > 0:
      while p%2 == 0:
        p = randint(10**n, 10**(n+2));
        final_base = p-1

      base_atual = randint(1,final_base)
      if Miller_Rabin(p, base_atual) == True:
        j=0
        for j in range(1, len(bases_usadas)+1):
          bases_usadas.remove(i)
          j+=1
        p=0
        i=10
      else:
        bases_usadas.append(base_atual)
        i-=1

  return p

from random import randint
def gera_chaves():
  p = gerar_n_primo(50)
  q = gerar_n_primo(100)
  n = p*q
  phi = (p-1)*(q-1)
  e=0
  d=0
  while (e*d) % phi != 1:
    e = randint(10**6, 10**7)
    d = phi + Euclides_estendido(e, phi)

  p_linha = q + Euclides_estendido(p,q)
  q_linha = p + Euclides_estendido(q,p)

  forma_reduzida_d_em_q = pow(d,1,q-1)
  forma_reduzida_d_em_p = pow(d,1,p-1)

  return [p, q, n, phi, e, d, p_linha, q_linha, forma_reduzida_d_em_q, forma_reduzida_d_em_p]

lista_de_parâmetros = [gera_chaves()]
p, q, n, phi, e, d, p_linha, q_linha, forma_reduzida_d_em_q, forma_reduzida_d_em_p = lista_de_parâmetros[0][0],lista_de_parâmetros[0][1],lista_de_parâmetros[0][2],lista_de_parâmetros[0][3], lista_de_parâmetros[0][4],lista_de_parâmetros[0][5],lista_de_parâmetros[0][6],lista_de_parâmetros[0][7],lista_de_parâmetros[0][8],lista_de_parâmetros[0][9]
print(lista_de_parâmetros)

def encriptar(texto:str, n, e):
  mensagem_em_codigo = 0
  texto_recebido = texto
  blocos_de_codigos = []
  símbolos_para_códigos = {'0': 111, '1': 112, '2': 113, '3': 114, '4': 115,
'5': 116, '6': 117, '7': 118, '8': 119, '9': 121, '=': 122, '+': 123,
'-': 124, '/': 125, '*': 126, 'a': 127, 'b': 128, 'c': 129, 'd': 131,
'e': 132, 'f': 133, 'g': 134, 'h': 135, 'i': 136, 'j': 137, 'k': 138,
'l': 139, 'm': 141, 'n': 142, 'o': 143, 'p': 144, 'q': 145, 'r': 146,
's': 147, 't': 148, 'u': 149, 'v': 151, 'w': 152, 'x': 153, 'y': 154,
'z': 155, 'á': 156, 'à': 157, 'â': 158, 'ã': 159, 'é': 161, 'ê': 162,
'í': 163, 'ó': 164, 'ô': 165, 'õ': 166, 'ú': 167, 'ç': 168, 'A': 169,
'B': 171, 'C': 172, 'D': 173, 'E': 174, 'F': 175, 'G': 176, 'H': 177,
'I': 178, 'J': 179, 'K': 181, 'L': 182, 'M': 183, 'N': 184, 'O': 185,
'P': 186, 'Q': 187, 'R': 188, 'S': 189, 'T': 191, 'U': 192, 'V': 193,
'W': 194, 'X': 195, 'Y': 196, 'Z': 197, 'Á': 198, 'À': 199, 'Â': 211,
'Ã': 212, 'É': 213, 'Ê': 214, 'Í': 215, 'Ó': 216, 'Ô': 217, 'Õ': 218,
'Ú': 219, 'Ç': 221, ',': 222, '.': 223, '!': 224, '?': 225, ';': 226,
':': 227, '_': 228, '(': 229, ')': 231, '"': 232, '#': 233, '$': 234,
'%': 235, '@': 236, ' ': 237, '\n': 238}
  
  for i in range(0, len(texto)): #transforma o texto recebido em uma sequencia de numeros
    mensagem_em_codigo *= 10**(len(str(símbolos_para_códigos[texto[i]])))
    mensagem_em_codigo += símbolos_para_códigos[texto[i]]

  for i in range(0, (len(str(mensagem_em_codigo))+1)):
    blocos_de_codigos.append(int(mensagem_em_codigo) % 10000)
    mensagem_em_codigo = (int(mensagem_em_codigo)//10000)
  
  for i in range(0, len(blocos_de_codigos)):
    if blocos_de_codigos[i] != 0:
      blocos_de_codigos[i] = pow(blocos_de_codigos[i], e, n)

  for i in range(0, len(blocos_de_codigos)):
    if 0 in blocos_de_codigos:
      blocos_de_codigos.remove(0)

  blocos_de_codigos.reverse()
  return blocos_de_codigos

def descriptar(blocos_de_codigos, n, d):
  mensagem_em_codigo = 0
  mensagem_em_texto = ""
  blocos_de_texto = []
  códigos_para_símbolos = {111: '0', 112: '1', 113: '2', 114: '3', 115: '4',
116: '5', 117: '6', 118: '7', 119: '8', 121: '9', 122: '=', 123: '+',
124: '-', 125: '/', 126: '*', 127: 'a', 128: 'b', 129: 'c', 131: 'd',
132: 'e', 133: 'f', 134: 'g', 135: 'h', 136: 'i', 137: 'j', 138: 'k',
139: 'l', 141: 'm', 142: 'n', 143: 'o', 144: 'p', 145: 'q', 146: 'r',
147: 's', 148: 't', 149: 'u', 151: 'v', 152: 'w', 153: 'x', 154: 'y',
155: 'z', 156: 'á', 157: 'à', 158: 'â', 159: 'ã', 161: 'é', 162: 'ê',
163: 'í', 164: 'ó', 165: 'ô', 166: 'õ', 167: 'ú', 168: 'ç', 169: 'A',
171: 'B', 172: 'C', 173: 'D', 174: 'E', 175: 'F', 176: 'G', 177: 'H',
178: 'I', 179: 'J', 181: 'K', 182: 'L', 183: 'M', 184: 'N', 185: 'O',
186: 'P', 187: 'Q', 188: 'R', 189: 'S', 191: 'T', 192: 'U', 193: 'V',
194: 'W', 195: 'X', 196: 'Y', 197: 'Z', 198: 'Á', 199: 'À', 211: 'Â',
212: 'Ã', 213: 'É', 214: 'Ê', 215: 'Í', 216: 'Ó', 217: 'Ô', 218: 'Õ',
219: 'Ú', 221: 'Ç', 222: ',', 223: '.', 224: '!', 225: '?', 226: ';',
227: ':', 228: '_', 229: '(', 231: ')', 232: '"', 233: '#', 234: '$',
235: '%', 236: '@', 237: ' ', 238: '\n'}
  
  for i in range(0, len(blocos_de_codigos)):
    blocos_de_codigos[i] = pow(blocos_de_codigos[i], d, n)

  for j in range(0,len(blocos_de_codigos)):
      mensagem_em_codigo *= 10**len(str(blocos_de_codigos[j]))
      mensagem_em_codigo += blocos_de_codigos[j]

  for k in range(0, (len(str(mensagem_em_codigo))//3)): #transforma a sequência recebida de numeros em texto, separa em blocos de 3 numeros
    blocos_de_texto.append(mensagem_em_codigo % 1000)
    mensagem_em_codigo = mensagem_em_codigo // 1000
    mensagem_em_texto += códigos_para_símbolos[blocos_de_texto[k]]


  mensagem_em_texto_inversa = mensagem_em_texto[::-1]
  print(mensagem_em_texto_inversa)

#código não terminado
def descriptar_otimizado(blocos_de_codigos, n, d,p, q, p_linha, q_linha, forma_reduzida_d_em_p, forma_reduzida_d_em_q):
  mensagem_em_codigo = 0
  mensagem_em_texto = ""
  blocos_de_texto = []
  codigo_intermediario = 0
  códigos_para_símbolos = {111: '0', 112: '1', 113: '2', 114: '3', 115: '4',
116: '5', 117: '6', 118: '7', 119: '8', 121: '9', 122: '=', 123: '+',
124: '-', 125: '/', 126: '*', 127: 'a', 128: 'b', 129: 'c', 131: 'd',
132: 'e', 133: 'f', 134: 'g', 135: 'h', 136: 'i', 137: 'j', 138: 'k',
139: 'l', 141: 'm', 142: 'n', 143: 'o', 144: 'p', 145: 'q', 146: 'r',
147: 's', 148: 't', 149: 'u', 151: 'v', 152: 'w', 153: 'x', 154: 'y',
155: 'z', 156: 'á', 157: 'à', 158: 'â', 159: 'ã', 161: 'é', 162: 'ê',
163: 'í', 164: 'ó', 165: 'ô', 166: 'õ', 167: 'ú', 168: 'ç', 169: 'A',
171: 'B', 172: 'C', 173: 'D', 174: 'E', 175: 'F', 176: 'G', 177: 'H',
178: 'I', 179: 'J', 181: 'K', 182: 'L', 183: 'M', 184: 'N', 185: 'O',
186: 'P', 187: 'Q', 188: 'R', 189: 'S', 191: 'T', 192: 'U', 193: 'V',
194: 'W', 195: 'X', 196: 'Y', 197: 'Z', 198: 'Á', 199: 'À', 211: 'Â',
212: 'Ã', 213: 'É', 214: 'Ê', 215: 'Í', 216: 'Ó', 217: 'Ô', 218: 'Õ',
219: 'Ú', 221: 'Ç', 222: ',', 223: '.', 224: '!', 225: '?', 226: ';',
227: ':', 228: '_', 229: '(', 231: ')', 232: '"', 233: '#', 234: '$',
235: '%', 236: '@', 237: ' ', 238: '\n'}

  for i in range(0, len(blocos_de_codigos)):
    codigo_intermediario = blocos_de_codigos[i]
    blocos_de_codigos[i] = pow(((codigo_intermediario**forma_reduzida_d_em_q)*p*p_linha)+((codigo_intermediario**forma_reduzida_d_em_p)*q*q_linha),1,n)

  for j in range(0,len(blocos_de_codigos)):
      mensagem_em_codigo *= 10**len(str(blocos_de_codigos[j]))
      mensagem_em_codigo += blocos_de_codigos[j]

  for k in range(0, (len(str(mensagem_em_codigo))//3)): #transforma a sequência recebida de numeros em texto, separa em blocos de 3 numeros
    blocos_de_texto.append(mensagem_em_codigo % 1000)
    mensagem_em_codigo = mensagem_em_codigo // 1000
    mensagem_em_texto += códigos_para_símbolos[blocos_de_texto[k]]


  mensagem_em_texto_inversa = mensagem_em_texto[::-1]
  return mensagem_em_texto_inversa