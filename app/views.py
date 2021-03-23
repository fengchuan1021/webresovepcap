from django.http import JsonResponse
from io import BytesIO
#import pcap
import datetime
import pyshark,os
from django.conf import settings
from django.db import connections
from app.models import Capfile,Data
application_level=['bgp','http','https','ssh','dns','icmp','dhcp','dns']
categories=application_level+['tcp','udp','ip']
def getprotocal(cap):
    for name in categories:
        if hasattr(cap,name):
            return name
    return ''
def getlayer_level(proto):
    if proto in application_level:
        return '应用层'
    if proto in ['tcp','udp']:
        return '传输层'
    if proto in ['ip']:
        return '网络层'
    if proto in ['eth']:
        return '链路层'
    return ''

def storemysql(f,caps):
    file=Capfile(filename=f)
    file.save()
    arr=[]
    for ind,cap in enumerate(caps):
        data=Data()
        data.fileid=file
        data.sniff_time=cap.sniff_time
        data.length=cap.length
        data.ind=ind
        if hasattr(cap,'ip'):
            data.srcip=cap.ip.src
            data.dstip=cap.ip.dst
            data.ttl=cap.ip.ttl
            data.version=int(cap.ip.version)
            ttl=int(data.ttl)
            if ttl<=32:
                data.hop=32-ttl
            elif ttl<=64:
                data.hop=64-ttl
            elif ttl<=128:
                data.hop=128-ttl
            elif ttl<=255:
                data.hop=255-ttl

        if hasattr(cap,'eth'):
            data.srcmac=cap.eth.src
            data.dstmac=cap.eth.dst
        data.proto_name=getprotocal(cap)
        data.layer_level=getlayer_level(data.proto_name)
        data.content=''
        arr.append(data)
    if arr:
        Data.objects.bulk_create(arr)

    return file.id
def getdetail(request,fileid,ind):
    f=Capfile.objects.get(id=fileid)
    caps = pyshark.FileCapture(f.filename)

    def getlayer(obj):

        if hasattr(obj,'layers'):
            tmparr = []
            for layer in obj.layers:
                obj={'label':layer.layer_name.upper()+' Layer'}
                t=getlayer(layer)
                if t:
                    obj['children']=t
                tmparr.append(obj)
            return tmparr
        else:
            s=''
            if obj.layer_name == obj.DATA_LAYER:
                s='DATA'
            for field_line in obj._get_all_field_lines():
                s += field_line
            return [{'label':'<pre>'+s.replace('\t','')+'</pre>'}]

    tmpdata=getlayer(caps[ind])
    retarr={'data':tmpdata}
    return JsonResponse(retarr)
def getpackagesbaseonsrc(request,fileid,source):
    cursor = connections['default'].cursor()
    colocums = ['srcip', 'dstip', 'srcmac', 'dstmac', 'proto_name', 'sniff_time','length','fileid_id','ind']
    sql = f"select {','.join(colocums)} from app_data where fileid_id={fileid}  and ((srcip='{source}' or dstip='{source}') or (srcmac='{source}' or dstmac='{source}'))"
    cursor.execute(sql)

    result = cursor.fetchall()
    arr = [dict(zip(colocums, row)) for row in result]
    return JsonResponse(arr,safe=False)
def getpackages(request,fileid,proto,source,target):
    proto=proto.replace("protocol: ",'')
    cursor = connections['default'].cursor()
    colocums = ['srcip', 'dstip', 'srcmac', 'dstmac', 'proto_name', 'sniff_time','length','fileid_id','ind']
    if 'arp' not in proto:

        sql=f"select {','.join(colocums)} from app_data where fileid_id={fileid} and proto_name='{proto}' and ((srcip='{source}' and dstip='{target}') or (srcip='{target}' and dstip='{source}'))"
    else:
        colocums2 = ['srcmac', 'dstmac', 'srcmac', 'dstmac', 'proto_name', 'sniff_time','length','fileid_id','ind']
        sql=f"select {','.join(colocums2)} from app_data where fileid_id={fileid} and proto_name='{proto}' and ((srcmac='{source}' and dstmac='{target}') or (srcmac='{target}' and dstmac='{source}'))"

    print(sql)
    cursor.execute(sql)
    result=cursor.fetchall()
    arr=[dict(zip(colocums,row)) for row in result]
    return JsonResponse(arr,safe=False)

def getdata(fileid,proto):
    nodes = {}
    links = {}
    cursor = connections['default'].cursor()
    sql = "SET SESSION sql_mode=(SELECT REPLACE(@@sql_mode,'ONLY_FULL_GROUP_BY,',''))"
    cursor.execute(sql)
    proto_name=''
    if proto !='all':
        proto_name=f' and proto_name="{proto}" '
    sql=f"select proto_name from app_data where fileid_id={fileid} group by proto_name"
    cursor.execute(sql)
    cat=cursor.fetchall()
    tmp_categories=[{'name':row[0]} for row in cat if row[0]]
    if proto not in ['arp']:
        sql = f"select srcip,dstip,ttl,hop,srcmac,proto_name from app_data where fileid_id={fileid} {proto_name}  GROUP BY srcip,dstip order by hop asc "
    else:
        sql = f"select srcmac,dstmac,ttl,hop,srcmac,proto_name from app_data where fileid_id={fileid} {proto_name}  GROUP BY srcmac,dstmac order by hop asc "

    cursor.execute(sql)
    result = cursor.fetchall()
    for row in result:
        if row[0] not in nodes:
            nodes[row[0]] = {'name': row[0], 'value': row[4], "category": row[5]}
        if (f'{row[0]},{row[1]}' not in links) and (f'{row[1]},{row[0]}' not in links):  # and (f'{dst},{src}' not in links)
            links[f'{row[0]},{row[1]}'] = {
                'source': row[0],
                'target': row[1],
                'value': f'protocol: {row[5]}',
                # 'name': 'hello',
                # 'des': f'{src}-{dst}'

            }
    return list(nodes.values()), list(links.values()),tmp_categories
def getdataview(request,fileid,proto):
    status=0
    err_msg='success'
    nodes,links,tmp_categories=getdata(fileid,proto)
    return JsonResponse({'status':status,'data':err_msg,'id':str(fileid),'nodes': nodes,'links':links,
                         'categories':tmp_categories


                         })
def resolve_pcap(f):
    if 1:

        caps = pyshark.FileCapture(f)
        fileid=storemysql(f,caps)
        return fileid
import time
def resove_pcapfile(request):
    status=0
    err_msg='success'
    nodes=links=[]
    try:
        if request.method == 'POST':
            obj = request.FILES.get('file')
            filename=os.path.join(settings.BASE_DIR,'data',str(obj)+str(time.time()))
            with open(filename,'wb') as f:
                for chunk in obj.chunks():
                    f.write(chunk)
            fileid=resolve_pcap(filename)
            nodes,links,tmp_categories=getdata(fileid)
            status=1
    except Exception as e:
        print(e)
        status = 0
        err_msg = 'error'

    return JsonResponse({'status':status,'data':err_msg,'id':fileid,'nodes': nodes,'links':links,
                         'categories':tmp_categories


                         })
