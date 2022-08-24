# Checking router config vs excel data file

Script to gather data from cisco XR routers:
```
show vrf all
show arp vrf all
show int desc | i "(Fo|Te|Gi|Hu|BE|Lo|BV)[0-9\.]+ "
show ipv4 int bri | i "(Loopback|TenGigE|FortyGigE|GigabitEthernet|HundredGigE|BVI|Bundle-Ether)[0-9\.]+ "
show evpn evi
show l2vpn bridge-domain detail | i "bridge-domain:|evi:|AC:" 
```

Compare it with excel data files and DB, to make sure that network is configured as intended.
