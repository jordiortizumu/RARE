set a [exec "show ipv4 ospf 100 database 0 | inc router"]
puts "$a"
