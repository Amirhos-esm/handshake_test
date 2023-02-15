import socket
import ssl
import time

def test_tls(host,sni,url):
    context = ssl.create_default_context()
    start=time.time();
    res='';
    try:
        with socket.create_connection((host, 443)) as sock:
            sock.settimeout(3)
            with context.wrap_socket(sock, server_hostname=sni) as ssock:
                ssock.write(f'GET {url} HTTP/1.1\r\n'.encode());
                ssock.write(f'Host: {sni}\r\n'.encode());
                ssock.write("User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36\r\n".encode());
                ssock.write("Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9\r\n".encode());
                # ssock.write("Accept-Encoding: gzip, deflate\r\n".encode());
                ssock.write("Accept-Language: en-US,en;q=0.9,fa;q=0.8\r\n".encode());
                ssock.write("Connection: close\r\n".encode());
                ssock.write("Upgrade-Insecure-Requests: 1\r\n\r\n".encode());
                res=ssock.recv(1024*5);
                start=round(time.time()-start,3) 
                ssock.close()
                return start,res;
    except:
        return False,0



