<template>
	<div :id="item.id" class='chartcontainer'>
		<div  v-show="showchart" style="width: 79%;float: left;display: inline-block;min-height: 800px;height: 100%;">
			<div :id="'chart'+item.id"  style="width: 100%;min-height: 800px;height: 100%;"></div>
		</div>
		
		
		<div style='width:1%;float:left;height: 100%;min-height: 800px;'>
			<i :class="showchart ? 'el-icon-caret-left' : 'el-icon-caret-right'" style="z-index: 999;" @click="toggle" id='togglei'></i>
		</div>
		
		<div id='tablediv' :style="showchart ? 'width:20%' : 'width:90%'">
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
</template>

<script>
	import * as echarts from 'echarts';
	export default{
		 props: ['item','domain'],
		data(){
			return {tableData:[],showchart:true,detaildata:[]}
		},
		methods:{
			toggle(){
				this.showchart=!this.showchart;
				console.log(this.showchart);
			},
			getdetail(row,c,e){
				this.axios.get(`${this.domain}/api/getdetail/${row.fileid_id}/${row.ind}/`).then(ret=>{
					console.log('detail');
					this.detaildata=ret.data.data;
				});
			},
			  // renderContent(h, { node, data, store }) {
			  //       return (
			  //         <span class="el-tree-node__label">
			  //           <pre>{node.label}</pre>
			  //         </span>);
			  //     },
		},
		mounted(){

			var myChart = echarts.init(document.getElementById('chart'+this.item.id));
			
			myChart.setOption({
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
			myChart.on('click',params=>{
				console.log(params);
				if(params.dataType=='edge'){
					this.axios.get(`${this.domain}/api/getpackages/${this.item.id}/${params.data.value}/${params.data.source}/${params.data.target}/`).then(ret=>{
							if(ret.data){
								this.tableData=ret.data;
							}
					});
				}
				
			});
			
		},
	}
</script>

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
