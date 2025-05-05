#!/bin/bash

ROUTERS=(router_rip_0 router_rip_1 router_rip_2 router_rip_3 router_ospf_0 router_ospf_1 router_ospf_2 router_ospf_3)

for r in "${ROUTERS[@]}"; do
  mkdir -p ./volumes/$r

  cat > ./volumes/$r/daemons <<EOF
zebra=yes
bgpd=no
ospfd=yes
ripd=yes
staticd=yes
EOF

  # cria frr.conf vazio
  touch ./volumes/$r/frr.conf

  # cria vtysh.conf com hostname adequado
  cat > ./volumes/$r/vtysh.conf <<EOF
service integrated-vtysh-config
hostname $r
EOF

done
