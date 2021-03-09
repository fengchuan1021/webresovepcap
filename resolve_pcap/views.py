from django.http import JsonResponse
from io import BytesIO
from resolve_pcap.resolve_libpcap import resolve_pcap
def resove_pcapfile(request):
    status=0
    err_msg='success'
    nodes=links=[]
    try:
        if request.method == 'POST':
            obj = request.FILES.get('file')
            print(obj)
            f = BytesIO()
            for chunk in obj.chunks():
                f.write(chunk)
            f.seek(0)
            nodes,links=resolve_pcap(f)
            print(nodes)
            print(links)
            status=1
    except Exception as e:
        status = 0
        err_msg = 'error'
    print('111111111111111')
    print(len(links))
    return JsonResponse({'status':status,'data':err_msg,'id':str(obj),'nodes': nodes,'links':links})
