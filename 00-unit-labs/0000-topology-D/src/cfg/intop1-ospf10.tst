description interop1: ospf p2mp te

exit

addrouter r1
int eth1 eth 0000.0000.1111 $1a$ $1b$
!
vrf def v1
 rd 1:1
 exit
router ospf4 1
 vrf v1
 router 4.4.4.1
 traffeng 2.2.2.1
 area 0 ena
 area 0 traff
 red conn
 exit
router ospf6 1
 vrf v1
 router 6.6.6.1
 traffeng 6.6.6.1
 area 0 ena
 area 0 traff
 red conn
 exit
int eth1
 vrf for v1
 ipv4 addr 1.1.1.1 255.255.255.0
 ipv6 addr fe80::1 ffff::
 router ospf4 1 ena
 router ospf6 1 ena
 mpls enable
 mpls rsvp4
 mpls rsvp6
 exit
int lo0
 vrf for v1
 ipv4 addr 2.2.2.1 255.255.255.255
 ipv6 addr 4321::1 ffff:ffff:ffff:ffff:ffff:ffff:ffff:ffff
 mpls enable
 mpls rsvp4
 mpls rsvp6
 exit
interface tunnel1
 bandwidth 11
 tunnel source loopback0
 tunnel destination 9.9.9.9
 tunnel domain-name 2.2.2.3
 tunnel vrf v1
 tunnel mode p2mpte
 vrf for v1
 ipv4 addr 3.3.3.1 255.255.255.0
 exit
!

addother r2
int eth1 eth 0000.0000.2211 $1b$ $1a$
int eth2 eth 0000.0000.2222 $2a$ $2b$
!
ip routing
ipv6 unicast-routing
mpls traffic-eng tunnels
no mpls traffic-eng signalling advertise implicit-null
interface loopback0
 ip addr 2.2.2.2 255.255.255.255
 ipv6 addr 4321::2/128
 exit
router ospf 1
 mpls traffic-eng router-id Loopback0
 mpls traffic-eng area 0
 redistribute connected subnets
 exit
ipv6 router ospf 1
 redistribute connected
 exit
interface gigabit2
 ip address 1.1.1.2 255.255.255.0
 ipv6 enable
 ip ospf network point-to-point
 ip ospf 1 area 0
 ipv6 ospf network point-to-point
 ipv6 ospf 1 area 0
 ip rsvp bandwidth
 mpls traffic-eng tunnels
 no shutdown
 exit
interface gigabit1
 ip address 1.1.2.2 255.255.255.0
 ipv6 enable
 ip ospf network point-to-point
 ip ospf 1 area 0
 ipv6 ospf network point-to-point
 ipv6 ospf 1 area 0
 ip rsvp bandwidth
 mpls traffic-eng tunnels
 no shutdown
 exit
!

addrouter r3
int eth1 eth 0000.0000.3333 $2b$ $2a$
!
vrf def v1
 rd 1:1
 exit
router ospf4 1
 vrf v1
 router 4.4.4.3
 traffeng 2.2.2.3
 area 0 ena
 area 0 traff
 red conn
 exit
router ospf6 1
 vrf v1
 router 6.6.6.3
 traffeng 6.6.6.3
 area 0 ena
 area 0 traff
 red conn
 exit
int eth1
 vrf for v1
 ipv4 addr 1.1.2.1 255.255.255.0
 ipv6 addr fe80::3 ffff::
 router ospf4 1 ena
 router ospf6 1 ena
 mpls enable
 mpls rsvp4
 mpls rsvp6
 exit
int lo0
 vrf for v1
 ipv4 addr 2.2.2.3 255.255.255.255
 ipv6 addr 4321::3 ffff:ffff:ffff:ffff:ffff:ffff:ffff:ffff
 mpls enable
 mpls rsvp4
 mpls rsvp6
 exit
interface tunnel1
 bandwidth 11
 tunnel source loopback0
 tunnel destination 9.9.9.9
 tunnel domain-name 2.2.2.1
 tunnel vrf v1
 tunnel mode p2mpte
 vrf for v1
 ipv4 addr 3.3.3.3 255.255.255.0
 exit
!


r1 tping 100 60 2.2.2.2 /vrf v1 /int lo0
r1 tping 100 60 4321::2 /vrf v1 /int lo0
r1 tping 100 60 2.2.2.3 /vrf v1 /int lo0
r1 tping 100 60 4321::3 /vrf v1 /int lo0

r3 tping 100 60 2.2.2.2 /vrf v1 /int lo0
r3 tping 100 60 4321::2 /vrf v1 /int lo0
r3 tping 100 60 2.2.2.1 /vrf v1 /int lo0
r3 tping 100 60 4321::1 /vrf v1 /int lo0

r1 tping 100 60 3.3.3.3 /vrf v1 /int lo0
r3 tping 100 60 3.3.3.1 /vrf v1 /int lo0
