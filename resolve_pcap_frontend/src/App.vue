<template>
  <div id="app">
    <div style='width: 20%;float:left'>
		<el-upload
		  class="upload-demo"
		  drag
		  multiple
		  :on-success='add_chartdata'
		  :on-remove="remove_file"
		  action="/api/uploadpcapfile/">
		  <i class="el-icon-upload"></i>
		  <div class="el-upload__text">将文件拖到此处，或<em>点击上传</em></div>
		  <div class="el-upload__tip" slot="tip">只能上传pcap文件</div>
		</el-upload>
	</div>
    <div id='main'>
      <mychart v-for='(item,key) of datas' :item='item'></mychart>
    </div>
  </div>
</template>

<script>
	document.body.addEventListener('click',function(e){
		if(e.target.className=='el-upload-list__item-name'){
			let id=e.target.childNodes[1].data.trim();
			console.log(id);
			e.stopPropagation();
			document.getElementById(id).scrollIntoView();
			return false; 
		}
		
	},true);
	import mychart from './mychart.vue'
export default {
	components: {
	           mychart
	        },
	data(){
		return {myhart:null,datas:[]}
	},

  methods: {
	  remove_file(file,FileList){
		  console.log(file);
		  for (let tmpi in this.datas) {
			  console.log(this.datas[tmpi]);
				if(this.datas[tmpi].id==file.name){
					this.datas.splice(tmpi,1);
					return 1;
				}
		  }
	  },
    add_chartdata(response, file, fileList) {

		if(response.status)
		this.datas.push(response)
    }
  }
}
</script>

<style>
	.upload-demo{
		position: fixed;
		top:30px;
	}
html,body,#app,#main{
	width:100%;
	height:100%;
}
#main{
	width: 80%;
	float: right;
}
.chartcontainer{
	min-height: 800px;
	width:100%;
}
#app {
  font-family: Helvetica, sans-serif;
  text-align: center;
}
</style>
