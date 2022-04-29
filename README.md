# RPG_redes

CLIENTE

Você está na [sala], na area [area], onde tem [numeroinimigos] [nomeinimigo].
Esta sala tem [itens].
Você tem [actionPointsCurrent]/[totalactionpoints].

1. Movimentar-se
2. Combate
3. Acessar mochila
4. Informacoes do outro jogador
5. Finalizar rodada

6. ENVIA MOVE, RECEBE INFO
   PROTOCOLO
   MOVE FLAG DATA
   FLAG 0 REQ SALAS DISPONIVEIS
   FLAG 1 SET SALA PARA ONDE VAI

Você está na [sala], na area [area].
Esta sala tem [itens].

Você pode ir para:
[sala1], [descricao1]
[sala2], [descricao2]
[sala3], [descricao3]

1. sala1
2. sala2
3. sala3

4. ENVIA BATT, RECEBE INFO
   COMB FLAG
   FLAG 0 ATAQUE
   FLAG 1 CURAR
   FLAG 3 DEFESA

Você atacou [nomeinimigo], e causou [dano].

3. ENVIA BPAC, RECEBE INFO
   BPAC FLAG DATA

Sua mochila tem [espacoMochila], e voce tem os itens [itens].

4. ENVIA PART, RECEBE INFO
   BOAR FLAG

5. ENVIA NEXT, RECEBE TEXT
   EXIT FLAG
