import subprocess

import subprocess

output = subprocess.check_output([
    "docker", "exec", "router_rip_0", "vtysh", "-c", "show ip route"
]).decode()

linhas = output.strip().splitlines()
rotas = [l for l in linhas if l.startswith(('R', 'O'))]  # R = RIP, O = OSPF
print("Quantidade de rotas:", len(rotas))
