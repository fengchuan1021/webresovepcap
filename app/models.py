from django.db import models

# Create your models here.
class Capfile(models.Model):
    filename=models.CharField(max_length=255,default='',verbose_name="文件名")

class Data(models.Model):
    fileid=models.ForeignKey(to=Capfile,on_delete=models.DO_NOTHING)
    sniff_time=models.DateTimeField(null=True,verbose_name='嗅探时间')
    srcip=models.CharField(max_length=40,verbose_name="源IP",blank=True,default='')
    ind=models.IntegerField(null=True)
    dstip=models.CharField(max_length=40,verbose_name="目标IP",blank=True,default='')
    layer_level=models.CharField(max_length=16,verbose_name="网络层次",blank=True,default='')
    proto_name=models.CharField(max_length=16,verbose_name="网络协议",blank=True,default='')
    ttl = models.IntegerField(verbose_name="生存时间", blank=True, default=0)
    hop=models.IntegerField(verbose_name="距离抓包机器时的跳数",null=True)
    version=models.IntegerField(verbose_name="版本", blank=True, default=0)
    srcmac=models.CharField(max_length=18,verbose_name="源mac",blank=True,default='')
    dstmac = models.CharField(max_length=18, verbose_name="目的mac", blank=True, default='')
    length=models.IntegerField(null=True)
    content=models.CharField(max_length=1024,verbose_name="协议内容",default='')

