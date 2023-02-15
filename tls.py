import functions
import ipaddress

#host='dl1.the-keepers.ir';
host='';
#or 
cidr='188.114.96.0/20'
#only ipv4 accepted

sni = 'dl1.the-keepers.ir'
url='/index.nginx-debian.html'


if  host:
    ping,result=functions.test_tls(host,sni,url)
    print(ping);
    print(result);
    exit();

ip,subnet=cidr.split('/');
subnet=int(subnet)
ip=ipaddress.IPv4Address(ip)
numberOfIps=1<<32-subnet;

print(ip)
print(int(subnet))
print(numberOfIps)

for i in range(numberOfIps):
    ping,result=functions.test_tls(str(ip),sni,url)
    print(f'ip:{ip} ping={ping}');
    ip=ipaddress.IPv4Address(int(ip)+1) #next ip
    

        
        