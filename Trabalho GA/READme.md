# Trabalho GA - Redes II

## Desenvolvido por:

- Rafael Hansen Klauck

## Arquivos

- `docker-compose.yml`: arquivo de configuração do docker-compose
- `image.png`: imagem da topologia utilizada
- `performance-evaluation.py`: script para avaliar a performance dos protocolos
- `script.sh`: script para criar os volumes utilizados no docker-compose. Ativa os daemons necessários (ospfd, ripd)

# Como rodar?

1. Instalar o docker
2. Rodar o script `script.sh` para criar as os volumes que serão utilizados no `docker-compose`
3. Rodar o comando `docker-compose up` na pasta do projeto
4. Caso não tenha realizado a configuração dos protocolos, siga os passos abaixo para configurar o RIP e OSPF

## Protocolo RIP

1. Acesse o container novamente com o comando `docker exec -it router_rip_<x> bash`
2. Acesse o terminal do roteador com o comando `vtysh`
3. Acesse o modo de configuração com o comando `configure terminal`
4. Acesse o modo de configuração do protocolo RIP com o comando `router rip`
5. Adicione as redes que deseja anunciar com o comando `network <ip_da_rede>`
6. Escreva `exit` para sair do modo de configuração do protocolo RIP
7. Escreva `exit` para sair do modo de configuração do roteador
8. Escreva `write` para salvar as configurações
9. Refaça os passos para o próximo roteador

### Redes de cada roteador

**router_rip_0:**

- network 192.168.1.0/24
- network 192.168.4.0/24

**router_rip_1:**

- network 192.168.1.0/24
- network 192.168.2.0/24

**router_rip_2:**

- network 192.168.2.0/24
- network 192.168.3.0/24

**router_rip_3:**

- network 192.168.3.0/24
- network 192.168.4.0/24

## Protocolo OSPF

1. Acesse o container novamente com o comando `docker exec -it router_ospf_<x> bash`
2. Acesse o terminal do roteador com o comando `vtysh`
3. Acesse o modo de configuração com o comando `configure terminal`
4. Acesse o modo de configuração do protocolo OSPF com o comando `router ospf`
5. Adicione as redes que deseja anunciar com o comando `network <ip_da_rede> <wildcard_mask> area <area_id>`
6. Escreva `exit` para sair do modo de configuração do protocolo OSPF
7. Escreva `exit` para sair do modo de configuração do roteador
8. Escreva `write` para salvar as configurações
9. Refaça os passos para o próximo roteador

### Redes de cada roteador

**router_ospf_0:**

- network 192.168.5.0/24 area 0
- network 192.168.8.0/24 area 0

**router_ospf_1:**

- network 192.168.5.0/24 area 0
- network 192.168.6.0/24 area 0

**router_ospf_2:**

- network 192.168.6.0/24 area 0
- network 192.168.7.0/24 area 0

**router_ospf_3:**

- network 192.168.7.0/24 area 0
- network 192.168.8.0/24 area 0
