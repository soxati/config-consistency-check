# Checking router config vs excel data file

Script to gather data from cisco XR routers:
```
show arp vrf all
show evpn evi
show ipv4 int bri | i "(Loopback|TenGigE|FortyGigE|GigabitEthernet|HundredGigE|BVI|Bundle-Ether)[0-9\.]+ "
show int desc | i "(Fo|Te|Gi|Hu|BE|Lo|BV)[0-9\.]+ "
show route
show l2vpn bridge-domain detail | i "bridge-domain:|evi:|AC:" 
show run formal vrf | i "policy"
show vrf all
```

Compare it with excel data files and DB, to make sure that network is configured as intended.
