<template>
  <div id="app">
    <div style='width: 15%;float:left;height: 100%;' id="uploaddiv" v-show="showchart">
		<el-upload
		  class="upload-demo"
		  drag
		  :on-success='add_chartdata'
		  :action="this.domain +'/api/uploadpcapfile/'">
		  <i class="el-icon-upload"></i>
		  <div class="el-upload__text">将文件拖到此处，或<em>点击上传</em></div>
		  <div class="el-upload__tip" slot="tip">只能上传pcap文件</div>
		</el-upload>
	</div>
    <div id='main' :style="showchart ? 'width:85%' : 'width:100%'">
      <div :id="item.id" class='chartcontainer'>
      	<div  id='chartdiv' :style="showchart ? 'width:79%' : 'width:49%'">
      		<div :id="'chart'+item.id"  style="width: 100%;min-height: 800px;height: 100%;"></div>
      	</div>
      	
      	
      	<div style='width:1%;float:left;height: 100%;min-height: 800px;'>
      		<i :class="showchart ? 'el-icon-caret-left' : 'el-icon-caret-right'" style="z-index: 999;" @click="toggle" id='togglei'></i>
      	</div>
      	
      	<div id='tablediv' :style="showchart ? 'width:20%' : 'width:50%'">
      		<div >
      			<template>
      			    <el-table
      			      :data="tableData"
      				  height="480"
      				  @row-click="getdetail"
      			      style="width: 100%">
      				      <el-table-column
      				        prop='ind'
      						label='序号'
      				       >
      				      </el-table-column>
      					  <el-table-column
      						prop='sniff_time'
      						label='时间'
      						
      					   >
      					  </el-table-column>
      			      <el-table-column
      			        prop="srcip"
      			        label="源地址"
      			        width="180">
      			      </el-table-column>
      			      <el-table-column
      			        prop="dstip"
      			        label="目的地址"
      			        width="180">
      			      </el-table-column>
      			      <el-table-column
      			        prop="proto_name"
      			        label="协议">
      			      </el-table-column>
      				  
      				  <el-table-column
      				    prop="length"
      				    label="包长度">
      				  </el-table-column>
      				  
      			    </el-table>
      			  </template>
      			
      		</div>
      		<div ><el-tree :data="detaildata"  default-expand-all>
      		 <span v-html="node.label" class="el-tree-node__labele" slot-scope="{ node, data }">
      			
      			 </span>
      		</el-tree></div>
      	</div>
      </div>
    </div>
  </div>
</template>

<script>
	import * as echarts from 'echarts';
export default {
	data(){
		return {myhart:null,item:[],domain:"http://127.0.0.1:8000",tableData:[],showchart:true,detaildata:[],myChart:null}
	},
mounted() {
	this.myChart = echarts.init(document.getElementById('chart'+this.item.id));
	this.axios.get(this.domain+'/api/gettestdata/19/').then(ret=>{
		this.item=ret.data;
		console.log(this.item);
		this.myChart.setOption({
		    tooltip: {},
			legend:[{
				data:this.item.categories.map(function(e){return e.name})
			}],
		    series: [{
		       
		        type: 'graph',
				layout: 'force',
				roam: true,
				data: this.item.nodes,
				links: this.item.links,
				categories: this.item.categories,
		        force: {
		                            repulsion: 100,layoutAnimation : true
		                        }
		    }]
		});
		
	});
	
	
	

	this.myChart.on('click',params=>{
		console.log(params);
		if(params.dataType=='edge'){
			this.axios.get(`${this.domain}/api/getpackages/${this.item.id}/${params.data.value}/${params.data.source}/${params.data.target}/`).then(ret=>{
					if(ret.data){
						this.tableData=ret.data;
					}
			});
		}
		else if(params.dataType=='node'){
			this.axios.get(`${this.domain}/api/getpackagesbaseonsrc/${this.item.id}/${params.data.name}/`).then(ret=>{
					if(ret.data){
						this.tableData=ret.data;
					}
			});
		}
		
	});
},
  methods: {
			toggle(){
				this.showchart=!this.showchart;
				
			},
			getdetail(row,c,e){
				this.axios.get(`${this.domain}/api/getdetail/${row.fileid_id}/${row.ind}/`).then(ret=>{
					console.log('detail');
					this.detaildata=ret.data.data;
				});
			},
    add_chartdata(response, file, fileList) {
		//console.log(response);
		if(response.status){
		this.item=response;
		this.myChart.setOption({
		    tooltip: {},
			legend:[{
				data:this.item.categories.map(function(e){return e.name})
			}],
		    series: [{
		       
		        type: 'graph',
				layout: 'force',
				roam: true,
				data: this.item.nodes,
				links: this.item.links,
				categories: this.item.categories,
		        force: {
		                            repulsion: 100,layoutAnimation : true
		                        }
		    }]
		});
		}
    }
  }
}
</script>

<style>
	#chartdiv{width: 79%;float: left;display: inline-block;min-height: 800px;height: 100%;}
	.upload-demo{
		position: fixed;
		top:30px;
	}
html,body,#app,#main{
	width:100%;
	height:100%;
}
#main{
	width: 85%;
	float: right;
}
.chartcontainer{
	min-height: 800px;
	width:100%;
}
.el-upload-dragger{width:230px;}
#app {
  font-family: Helvetica, sans-serif;
  text-align: center;
}
</style>
<style>
	#togglei{
		position: relative;
		top:300px;
		}

		#tablediv{float: left;display: inline-block;}
		.el-tree-node>.el-tree-node__children{
			overflow: none;
			text-align: left;
		}
		.el-tree-node__content{
			height: auto;
		}
</style>
