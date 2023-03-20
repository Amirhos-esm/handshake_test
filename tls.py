import socket
import ssl
import time
from threading import Thread
import ipaddress


def test_tls(host,sni,url,result,index):
    context = ssl.create_default_context()
    start=time.time();
    tcpPing=0
    tlsPing=0;
    res='';
    try:
        with socket.create_connection(address=(host, 443),timeout=5) as sock:
            tcpPing=round(time.time()-start,3) 
            start=time.time();
            sock.settimeout(1.5
                            )
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
                tlsPing=round(time.time()-start,3) 
                result[index]= True,(tlsPing,tcpPing),res;
    except Exception as e:
        result[index]= False,(tlsPing,tcpPing),e;


cidr='104.16.209.0/22'
sni = 'dl1.the-keepers.ir'
url='/text.txt'


ip,subnet=cidr.split('/');
subnet=int(subnet)
ip=ipaddress.IPv4Address(ip)
numberOfIps=1<<32-subnet;
interval=64



print(ip)
print(f"{numberOfIps} ip`s need to check")


if __name__ == "__main__":
    
    results=[None]*interval
    threads=[None]*interval
    while numberOfIps>0:
        print('*testing from {} to {}'.format(ip,ipaddress.IPv4Address(int(ip)+interval-1)))
        for i in range(interval):
            _ip=ipaddress.IPv4Address(int(ip)+i)
            threads[i] = Thread(target = test_tls, args = (str(_ip),'www.speedtest.net','/test.txt',results,i))
            threads[i].start()
        for i in range(interval):
            threads[i].join()

        for i in range(interval):
            if results[i][0]:
                print("\tip: {} status: {}".format(
                    ipaddress.IPv4Address(int(ip)+i),
                    results[i][1] if results[i][0] else ("error: "+str(results[i][2]))
                    ))
        ip=ipaddress.IPv4Address(int(ip)+interval)    
        numberOfIps-=interval



