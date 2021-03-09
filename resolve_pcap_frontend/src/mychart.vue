<template>
	<div :id="item.id" class='chartcontainer'></div>
</template>

<script>
	import * as echarts from 'echarts';
	export default{
		 props: ['item'],

		mounted(){

			var myChart = echarts.init(document.getElementById(this.item.id));
			myChart.setOption({
			    title: {
			        text: this.item.id+'拓扑图',
					left: 'center'
			    },
			    tooltip: {},
			    series: [{
			       
			        type: 'graph',
					layout: 'force',
					roam: true,
					data: this.item.nodes,
					links: this.item.links,
			        force: {
			                            repulsion: 100,layoutAnimation : true
			                        }
			    }]
			});
		},
	}
</script>

<style>
</style>
