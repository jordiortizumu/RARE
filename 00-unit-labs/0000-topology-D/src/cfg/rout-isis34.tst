description isis broadcast subnet with narrow metric

addrouter r1
int eth1 eth 0000.0000.1111 $1a$ $1b$
!
vrf def v1
 rd 1:1
 exit
bridge 1
 exit
bridge 2
 exit
router isis4 1
 vrf v1
 net 48.4444.0000.1111.00
 no metric-wide
 red conn
 exit
router isis6 1
 vrf v1
 net 48.6666.0000.1111.00
 no metric-wide
 red conn
 exit
int lo1
 vrf for v1
 ipv4 addr 2.2.2.1 255.255.255.255
 ipv6 addr 4321::1 ffff:ffff:ffff:ffff:ffff:ffff:ffff:ffff
 exit
int eth1.11
 bridge-gr 1
 exit
int eth1.12
 bridge-gr 2
 exit
int bvi1
 vrf for v1
 ipv4 addr 1.1.1.1 255.255.255.0
 router isis4 1 ena
 router isis4 1 net broad
 exit
int bvi2
 vrf for v1
 ipv6 addr 1234::1 ffff::
 router isis6 1 ena
 router isis6 1 net broad
 exit
!

addrouter r2
int eth1 eth 0000.0000.2222 $1b$ $1a$
int eth2 eth 0000.0000.2222 $2a$ $2b$
!
vrf def v1
 rd 1:1
 exit
bridge 1
 mac-learn
 exit
bridge 2
 mac-learn
 exit
router isis4 1
 vrf v1
 net 48.4444.0000.2222.00
 no metric-wide
 red conn
 exit
router isis6 1
 vrf v1
 net 48.6666.0000.2222.00
 no metric-wide
 red conn
 exit
int lo1
 vrf for v1
 ipv4 addr 2.2.2.2 255.255.255.255
 ipv6 addr 4321::2 ffff:ffff:ffff:ffff:ffff:ffff:ffff:ffff
 exit
int eth1.11
 bridge-gr 1
 exit
int eth1.12
 bridge-gr 2
 exit
int eth2.11
 bridge-gr 1
 exit
int eth2.12
 bridge-gr 2
 exit
int bvi1
 vrf for v1
 ipv4 addr 1.1.1.2 255.255.255.0
 router isis4 1 ena
 router isis4 1 net broad
 exit
int bvi2
 vrf for v1
 ipv6 addr 1234::2 ffff::
 router isis6 1 ena
 router isis6 1 net broad
 exit
!


addrouter r3
int eth1 eth 0000.0000.3333 $2b$ $2a$
!
vrf def v1
 rd 1:1
 exit
bridge 1
 exit
bridge 2
 exit
router isis4 1
 vrf v1
 net 48.4444.0000.3333.00
 no metric-wide
 red conn
 exit
router isis6 1
 vrf v1
 net 48.6666.0000.3333.00
 no metric-wide
 red conn
 exit
int lo1
 vrf for v1
 ipv4 addr 2.2.2.3 255.255.255.255
 ipv6 addr 4321::3 ffff:ffff:ffff:ffff:ffff:ffff:ffff:ffff
 exit
int eth1.11
 bridge-gr 1
 exit
int eth1.12
 bridge-gr 2
 exit
int bvi1
 vrf for v1
 ipv4 addr 1.1.1.3 255.255.255.0
 router isis4 1 ena
 router isis4 1 net broad
 exit
int bvi2
 vrf for v1
 ipv6 addr 1234::3 ffff::
 router isis6 1 ena
 router isis6 1 net broad
 exit
!

r1 tping 100 20 2.2.2.1 /vrf v1 /int lo1

r1 tping 100 20 2.2.2.2 /vrf v1 /int lo1
r1 tping 100 20 2.2.2.3 /vrf v1 /int lo1
r1 tping 100 20 4321::2 /vrf v1 /int lo1
r1 tping 100 20 4321::3 /vrf v1 /int lo1

r2 tping 100 20 2.2.2.1 /vrf v1 /int lo1
r2 tping 100 20 2.2.2.3 /vrf v1 /int lo1
r2 tping 100 20 4321::1 /vrf v1 /int lo1
r2 tping 100 20 4321::3 /vrf v1 /int lo1

r3 tping 100 20 2.2.2.1 /vrf v1 /int lo1
r3 tping 100 20 2.2.2.2 /vrf v1 /int lo1
r3 tping 100 20 4321::1 /vrf v1 /int lo1
r3 tping 100 20 4321::2 /vrf v1 /int lo1
