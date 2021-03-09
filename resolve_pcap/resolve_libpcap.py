import pcap
import datetime
import dpkt
import socket
from dpkt.compat import compat_ord
def inet_to_str(inet):
    """Convert inet object to a string

        Args:
            inet (inet struct): inet network address
        Returns:
            str: Printable/readable IP address
    """
    # First try ipv4 and then ipv6
    try:
        return socket.inet_ntop(socket.AF_INET, inet)
    except ValueError:
        return socket.inet_ntop(socket.AF_INET6, inet)
def mac_addr(address):
    """Convert a MAC address to a readable/printable string

       Args:
           address (str): a MAC address in hex form (e.g. '\x01\x02\x03\x04\x05\x06')
       Returns:
           str: Printable/readable MAC address
    """
    return ':'.join('%02x' % compat_ord(b) for b in address)
def resolve_pcap(f):
    if 1:
        nodes={}
        links={}
        pcapf = dpkt.pcap.Reader(f)

        for timestamp, buf in pcapf:
            #print('Timestamp: ', str(datetime.datetime.utcfromtimestamp(timestamp)))
            try:
                eth = dpkt.ethernet.Ethernet(buf)
                if not isinstance(eth.data, dpkt.ip.IP):
                    continue
                ip = eth.data
                src=inet_to_str(ip.src)
                dst=inet_to_str(ip.dst)
                if src not in nodes:
                    nodes[src]={'name':src,'value': mac_addr(eth.src)}
                if dst not in nodes:
                    nodes[dst]={'name':dst,'value': mac_addr(eth.dst)}
                if (f'{src},{dst}' not in links) and (f'{dst},{src}' not in links): # and (f'{dst},{src}' not in links)
                    links[f'{src},{dst}']={
                        'source': src,
                        'target': dst,
                        #'value':'hello',
                       #'name': 'hello',
                       # 'des': f'{src}-{dst}'

                    }
            except Exception as e:
                print(e)

        return list(nodes.values()),list(links.values())
            # Pull out fragment information (flags and offset all packed into off field, so use bitmasks)
            #do_not_fragment = bool(ip.off & dpkt.ip.IP_DF)
            #more_fragments = bool(ip.off & dpkt.ip.IP_MF)
            #fragment_offset = ip.off & dpkt.ip.IP_OFFMASK
