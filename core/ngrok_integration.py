############################
#   _  _  ___         _   
#  | \| |/ __|_ _ ___| |__
#  | .` | (_ | '_/ _ \ / /
#  |_|\_|\___|_| \___/_\_\
#                         
############################

from pyngrok import ngrok

def kill_all_ngrok_tunnels():
    for tunnel in ngrok.get_tunnels():
        ngrok.disconnect(tunnel.public_url)

def forward_port(port: int, ngrok_auth_token: str) -> (str, int, ngrok.NgrokTunnel):
    ngrok.set_auth_token(ngrok_auth_token)
    tunnel = ngrok.connect(port, "tcp")
    url = tunnel.public_url.split('/')[-1]
    if url.count(':') != 1:
        raise ValueError(f"\"{url}\" does not looks like an actual TCP URL (host:port)")
    host, port = url.split(':')
    return (host, int(port), tunnel)