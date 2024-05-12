 $(window).load(function(){  
             $(".loading").fadeOut()
            })  
			
/****/
$(document).ready(function(){
	var whei=$(window).width()
	$("html").css({fontSize:whei/20})
	$(window).resize(function(){
		var whei=$(window).width()
	 $("html").css({fontSize:whei/20})
});
	});


 $(window).load(function(){$(".loading").fadeOut()})  
$(function () {
    echarts_1()
    echarts_2()
    echarts_3()
    echarts_4()
    echarts_5()
    echarts_6()
    pe01()
    pe02()
    pe03()

function echarts_1() {
 var myChart = echarts.init(document.getElementById('echarts1'));

 option = {
  tooltip: {
 trigger: 'axis',
 axisPointer: {type: 'shadow'},
},"grid": {
  "top": "20%",
"right":"50",
"bottom":"20",
"left":"30",
},
legend: {
  data: ['产量（万吨）','产量增速'],
  right: 'center', width:'100%',
  textStyle: {
      color: "#fff"
  },
  itemWidth: 12,
  itemHeight: 10,
},



 "xAxis": [
   {
     "type": "category",
     data: ['2012','2013', '2014', '2015', '2016','2017','2018','2019','2020','2021','2022'],
     axisLine: { lineStyle: {color: "rgba(255,255,255,.1)"}},
     axisLabel:  { textStyle: {color: "rgba(255,255,255,.7)", fontSize: '14', },
         },
 
     },
],
 "yAxis": [
   {
     "type": "value",
     "name": "万吨",
     axisTick: {show: false},
     splitLine: {
      show: false,
     
  },
     "axisLabel": {
       "show": true,
       fontSize:14,
       color: "rgba(255,255,255,.6)"
      
     },
     axisLine: {
      min:0,
      max:10,
       lineStyle: {color: 'rgba(255,255,255,.1)'}
      },//左线色
     
   },
   {
     "type": "value",
     "name": "百分比",
     "show": true,
     "axisLabel": {
       "show": true,
       fontSize:14,
       formatter: "{value} %",
       color: "rgba(255,255,255,.6)"
     },
     axisTick: {show: false},
   axisLine: {lineStyle: {color: 'rgba(255,255,255,.1)'}},//右线色
    splitLine: {show:true,lineStyle: {color:'rgba(255,255,255,.1)'}},//x轴线
   },
 ],
 "series": [
  
   {
     "name": "产量（万吨）",
     "type": "bar",
     "data": [22091.5,22748.1,23302.63,24524.62,24405.24,25241.9,25688.35,27400.84,28692.36,29970.2,31296.24],
     "barWidth": "15%",
     "itemStyle": {
       "normal": {
        barBorderRadius: 15,
        color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [{
          offset: 0,
          color: '#8bd46e'
      }, {
          offset: 1,
          color: '#09bcb7'
      }]),
       }
     },
     "barGap": "0.2"
   },
   
   {
     "name": "产量增速",
     "type": "line",
        smooth: true,
     "yAxisIndex": 1,
     "data": [5.10,2.97,2.44,5.24,-0.49,3.43,1.77,6.67,4.71,4.45,4.42],
   lineStyle: {
        normal: {
          width: 2
        },
      },
     "itemStyle": {
       "normal": {
         "color": "#86d370",
    
       }
     }, 
   } 
  
 ]
};

        myChart.setOption(option);
        window.addEventListener("resize",function(){
            myChart.resize();
        });

	
    }
function echarts_2() {
        // 基于准备好的dom，初始化echarts实例
        var myChart = echarts.init(document.getElementById('echarts2'));

       option = {
	    tooltip: {
        trigger: 'axis',
        axisPointer: {type: 'shadow'},
       // formatter:'{c}' ,
    },
    grid: {
        left: '0',
	  	top: '30',
        right: '10',
        bottom: '-20',
        containLabel: true
    },
    legend: {
        data: ['进口金额（万美元）', '出口金额（千万美元）'],
        right: 'center',
        top:0,
        textStyle: {
            color: "#fff"
        },
        itemWidth: 12,
        itemHeight: 10,
        // itemGap: 35
    },

    xAxis: [{
        type: 'category',
        boundaryGap: false,
        axisLabel:  {
          rotate: -90,
                textStyle: {
 					color: "rgba(255,255,255,.6)",
          fontSize:14,
         
                },
            },
        axisLine: {
			lineStyle: { 
				color: 'rgba(255,255,255,.1)'
			}

        },

   data: ['2017','2018','2019','2020','2021','2022','2023年1~5月']

    }, {

        axisPointer: {show: false},
        axisLine: {  show: false},
        position: 'bottom',
        offset: 20,

       

    }],

    "yAxis": [
      {
        "type": "value",
        "name": "万美元",
        "show": true,
        axisTick: {show: false},
        splitLine: {
         show: false,
        },
        "axisLabel": {
          "show": true,
          fontSize:14,
          formatter: "{value} 万美元",
          color: "rgba(255,255,255,.6)"
         
        },
        axisLine: {
         min:0,
         max:10,
          lineStyle: {color: 'rgba(255,255,255,.1)'}
         },//左线色
        
      },
      {
        "type": "value",
        "name": "千万美元",
        "show": true,
        "axisLabel": {
          "show": true,
          fontSize:14,
          formatter: "{value} 千万美元",
          color: "rgba(255,255,255,.6)"
        },
        axisTick: {show: false},
      axisLine: {lineStyle: {color: 'rgba(255,255,255,.1)'}},//右线色
       splitLine: {show:true,lineStyle: {color:'rgba(255,255,255,.1)'}},//x轴线
      },
    ],
    "series": [
     
      {
        "name": "进口金额（万美元）",
        "type": "line",
        "data": [1266.44,1312.29,2130.33,1809.31,1761.45,2692.76,1765.64],
        "barWidth": "15%",
        "itemStyle": {
          "normal": {
           barBorderRadius: 15,
           color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [{
             offset: 0,
             color: '#FFF68F'
         }, {
             offset: 1,
             color: '#FFF68F'
         }]),
          }
        },
        "barGap": "0.2"
      },
      
      {
        "name": "出口金额（千万美元）",
        "type": "line",
           smooth: true,
        "yAxisIndex": 1,
        "data": [63.62,63.05,64.99,75.49,69.34,59.17,22.58],
      lineStyle: {
           normal: {
             width: 2
           },
         },
        "itemStyle": {
          "normal": {
            "color": "#8B864E",
       
          }
        }, 
      } 
     
    ]
};
        // 使用刚指定的配置项和数据显示图表。
        myChart.setOption(option);
        window.addEventListener("resize",function(){
            myChart.resize();
        });
    }
    function echarts_3() {
        // 基于准备好的dom，初始化echarts实例
        var myChart = echarts.init(document.getElementById('echarts3'));

        option = {

          tooltip: {
            trigger: 'axis',
            axisPointer: { // 坐标轴指示器，坐标轴触发有效
              type: 'shadow' // 默认为直线，可选为：'line' | 'shadow'
            }
          },
          legend: {
            data: ['进口量（吨）', '出口量（万吨）'],
            right: 'center',
            top:0,
            textStyle: {
                color: "#fff"
            },
            itemWidth: 12,
            itemHeight: 10,
            // itemGap: 35
        },
          grid: {
            left: '0',
            right: '20',
            bottom: '0',
            top:'15%',
            containLabel: true
          },
          xAxis: {
            type: 'category',
            data: ['2017','2018','2019','2020','2021','2022','2023年1~5月'],
            axisLine: {
              lineStyle: {
                color: 'white'
   
              }
            },
            axisLabel: {
              //rotate:-90,
              formatter:function(value){return value.split("").join("\n");},
         textStyle: {
              color: "rgba(255,255,255,.6)",
             fontSize:14,
                   }
        },
            axisLine: {
               lineStyle: {
                   color: 'rgba(255,255,255,0.3)'
               }
           },
          },
   
          "yAxis": [
            {
              "type": "value",
              "name": "吨",
              splitLine: {show: false},
              axisTick: {show: false},
              "axisLabel": {
                "show": true,
                color: "rgba(255,255,255,.6)"
               
              },
              axisLine: {lineStyle: {color: 'rgba(255,255,255,.1)'}},//左线色
              
            },
            {
              "type": "value",
              "name": "万吨",
              "show": true,
              axisTick: {show: false},
              "axisLabel": {
                "show": true,
                formatter: "{value} ",
                color: "rgba(255,255,255,.6)"
              },
            axisLine: {lineStyle: {color: 'rgba(255,255,255,.1)'}},//右线色
             splitLine: {show:true,lineStyle: {color:'rgba(255,255,255,.1)'}},//x轴线
            },
          ],
          "series": [
           
            {
              "name": "进口量（吨）",
              "type": "bar",
              "data": [7808.18,7712.25,12909.13,10502.24,9477.77,12292.28,9312.73],
              "barWidth": "20%",
   
              "itemStyle": {
                "normal": {
                 barBorderRadius: 15,
                 color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [{
                   offset: 0,
                   color: '#9932CC'
               }, {
                   offset: 1,
                   color: '#9932CC'
               }]),
                }
              },
              "barGap": "0"
            },
            {
              "name": "出口量（万吨）",
              "type": "bar",
              "yAxisIndex": 1,
          
              "data": [61.71,59.15,54.85,63.39,60.06,53.12,17.21],
              "barWidth": "20%",
   
              "itemStyle": {
                "normal": {
                  barBorderRadius: 15,
                  color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [{
                    offset: 0,
                    color: '#EE82EE'
                }, {
                    offset: 1,
                    color: '#EE82EE'
                }]),
                 }
              },
              "smooth": true
            }
          ]
        //   series: [{
        //     name: '进口量（吨）',
        //     type: 'bar',
        //     stack: 'a',
        //     barWidth: '30',barGap: 0,
        //     itemStyle: {
        //        normal: {
        //         color: '#8bd46e', }
        //     },
        //     data: [7808.18,7712.25,12909.13,10502.24,9477.77,12292.28,9312.73]
        //   },
        //   {
        //     name: '出口量（吨）',
        //     type: 'bar',
        //     stack: 'a',
        //     barWidth: '30',barGap: 0,
        //     itemStyle: {
        //        normal: {
        //         color: '#f5804d',
        //        barBorderRadius:0, }
        //     },
        //     data: [-61.71,-59.15,-54.85,-63.39,-60.06,-53.12,-17.21]
        //   },
          
        // ]
        };

        // 使用刚指定的配置项和数据显示图表。
        myChart.setOption(option);
        window.addEventListener("resize",function(){
            myChart.resize();
        });
    }
    function echarts_5() {
      // 基于准备好的dom，初始化echarts实例
      var myChart = echarts.init(document.getElementById('echarts5'));

      option = {
        tooltip: {
       trigger: 'axis',
       axisPointer: {type: 'shadow'},
      },"grid": {
        "top": "15%",
      "right":"10%",
      "bottom":"20",
      "left":"10%",
      },
       legend: {
        data: ['表观消费量（万吨）', '增长率（%）'],
        right: 'center',
        top:0,
        textStyle: {
            color: "#fff"
        },
        itemWidth: 12,
        itemHeight: 10,
      },
       "xAxis": [
         {
           "type": "category",
       
           data: ['2012', '2013', '2014', '2015','2016','2017','2018','2019','2020','2021','2022'],
        axisLine: { lineStyle: {color: "rgba(255,255,255,.1)"}},
           axisLabel:  { textStyle: {color: "rgba(255,255,255,.7)", fontSize: '14', },
               },
       
           },
     ],
       "yAxis": [
         {
           "type": "value",
           "name": "万吨",
           splitLine: {show: false},
           axisTick: {show: false},
           "axisLabel": {
             "show": true,
             color: "rgba(255,255,255,.6)"
            
           },
           axisLine: {lineStyle: {color: 'rgba(255,255,255,.1)'}},//左线色
           
         },
         {
           "type": "value",
           "name": "%",
           "show": true,
           axisTick: {show: false},
           "axisLabel": {
             "show": true,
             formatter: "{value} %",
             color: "rgba(255,255,255,.6)"
           },
         axisLine: {lineStyle: {color: 'rgba(255,255,255,.1)'}},//右线色
          splitLine: {show:true,lineStyle: {color:'rgba(255,255,255,.1)'}},//x轴线
         },
       ],
       "series": [
        
         {
           "name": "表观消费量（万吨）",
           "type": "bar",
           "data": [
            1503.74,1506.58,1552.92,1616.22,1551.88,1589.81,1559.44,1685.62,1728.63,1837.51,1870
           ],
           "barWidth": "20%",

           "itemStyle": {
             "normal": {
              barBorderRadius: 15,
              color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [{
                offset: 0,
                color: '#fccb05'
            }, {
                offset: 1,
                color: '#f5804d'
            }]),
             }
           },
           "barGap": "0"
         },
         {
           "name": "增长率（%）",
           "type": "line",
           "yAxisIndex": 1,
       
           "data": [ , -0.21,3.08,4.08,-3.98,2.44,-1.91,8.09,2.55,6.30,2],
         lineStyle: {
         normal: {
           width: 2
         },
       },
           "itemStyle": {
             "normal": {
               "color": "#ff3300",
          
             }
           },
           "smooth": true
         }
       ]
   };
      // 使用刚指定的配置项和数据显示图表。
      myChart.setOption(option);
      window.addEventListener("resize",function(){
          myChart.resize();
      });
  }
    function echarts_4() {
      // 基于准备好的dom，初始化echarts实例
      var myChart = echarts.init(document.getElementById('echarts4'));
      var myColor=['#eb2100','#eb3600','#d0570e','#d0a00e','#34da62','#00e9db','#00c0e9','#0096f3'];
      option = {
           
              grid: {
                  left: '2%',
                  top:'1%',
                  right: '5%',
                  bottom: '0%',
                  containLabel: true
              },
              xAxis: [{
                  show: false,
              }],
              yAxis: [{
                      axisTick:'none',
                      axisLine:'none',
                      offset:'7',
                      axisLabel: {
                              textStyle: {
                                  color: 'rgba(255,255,255,.6)',
                                  fontSize:'14',
                              }
                          },
                      data: ['四川省','安徽省','辽宁省','山西省','河南省','贵州省','云南省','山东省','河北省','吉林省']

                  }, {
                      axisTick:'none',
                      axisLine:'none',
                      axisLabel: {
                              textStyle: {
                                color: 'rgba(255,255,255,.6)',
                                  fontSize:'14',
                              }
                          },
                      data: [385,392,469,694,715,740,859,889,1539,3898]

                       },{
                      name:'单位：件',
                          nameGap:'50',
                          nameTextStyle:{
                            color: 'rgba(255,255,255,.6)',
                              fontSize:'16',
                          },
                      axisLine:{
                        lineStyle:{
                          color:'rgba(0,0,0,0)'
                        }
                      },
                      data: [],
              }],
              series: [{
                  name: '条',
                  type: 'bar',
                  yAxisIndex: 0,
                  data: [2,2,3,5,5,5,6,6,11,28],
                  label:{
                        normal:{
                          show:true,
                          position:'right',
                          formatter:function(param){
                            return param.value + '%';
                          },
                          textStyle:{
                            color: 'rgba(255,255,255,.8)',
                             fontSize:'12',
                          }
                        }
                  },
                  barWidth: 15,
                  itemStyle: {
                      normal: {
                          color: new echarts.graphic.LinearGradient(1, 0, 0, 0, [{
                                  offset: 0,
                                  color: '#03c893'
                              },
                              {
                                  offset: 1,
                                  color: '#0091ff'
                              }
                          ]),
                          barBorderRadius: 15,
                      }
                  },
                  z: 2
              }, {
                  name: '白框',
                  type: 'bar',
                  yAxisIndex: 1,
                  barGap: '-100%',
                  data: [99.5,99.5,99.5,99.5,99.5,99.5,99.5,99.5,99.5,99.5],
                  barWidth: 15,
                  itemStyle: {
                      normal: {
                        color:'rgba(0,0,0,.2)',
                          barBorderRadius:15,
                      }
                  },
                  z: 1
              }]
          };
   

      // 使用刚指定的配置项和数据显示图表。
      myChart.setOption(option);
      window.addEventListener("resize",function(){
          myChart.resize();
      });
  }
  function echarts_6() {
    // 基于准备好的dom，初始化echarts实例
    var myChart = echarts.init(document.getElementById('echarts6'));
   

  option = {
    title:{
      text:'25万吨',
      subtext:'总出口量',
      x:'center',
      y:'40%',
      textStyle:{
          color:'#fff',
          fontSize:22,
          lineHeight:10,
      },
      subtextStyle: {
          color:'#90979c',
          fontSize:16,
          lineHeight:10,

      },
  },
    tooltip: {
        trigger: 'item',
        formatter: "{b} : {c} ({d}%)"
    },

    visualMap: {
        show: false,
        min: 500,
        max: 600,
        inRange: {
            //colorLightness: [0, 1]
        }
    },
    series: [{
        name: '访问来源',
        type: 'pie',
        radius: ['50%', '70%'],
        center: ['50%', '50%'],
        color: ['rgb(131,249,103)', '#FBFE27', '#FE5050', '#1DB7E5'], //'#FBFE27','rgb(11,228,96)','#FE5050'
        data: [{
          "value": 36.27,
          "name": "印度尼西亚"
      }, {
        "value": 20.82,
        "name": "越南"
      }, {
        "value": 10.25,
        "name": "泰国"
      }, {
        "value": 6.68,
        "name": "中国香港"
      }, {
        "value": 5.95,
        "name": "马来西亚"
      }, {
        "value": 4,
        "name": "菲律宾"
      }, {
        "value": 2,
        "name": "美国"
      }, {
        "value": 2,
        "name": "新加坡"
      }, {
        "value": 2,
        "name": "加拿大"
      } ,{
        "value": 10,
        "name": "其他"
      }  
        ].sort(function(a, b) {
            return a.value - b.value
        }),
        roseType: 'radius',

        label: {
            normal: {
                formatter: ['{c|{c}%}', '{b|{b}}'].join('\n'),
                rich: {
                    c: {
                        color: 'rgb(241,246,104)',
                        fontSize: 20,
                        fontWeight:'bold',
                        lineHeight: 5
                    },
                    b: {
                        color: 'rgb(98,137,169)',
                        fontSize: 14,
                        height: 44
                    },
                },
            }
        },
        labelLine: {
            normal: {
                lineStyle: {
                    color: 'rgb(98,137,169)',
                },
                smooth: 0.2,
                length: 10,
                length2: 20,

            }
        }
    }]
};
 

    // 使用刚指定的配置项和数据显示图表。
    myChart.setOption(option);
    window.addEventListener("resize",function(){
        myChart.resize();
    });
}


    function pe01() {
        // 基于准备好的dom，初始化echarts实例
        var myChart = echarts.init(document.getElementById('pe01'));
        var txt=81
        option = {
            title: {
              text: txt+'%',
              x: 'center',
             y: 'center',
              textStyle: {
                fontWeight: 'normal',
                color: '#fff',
                fontSize: '18'
              }
            },
            color:'rgba(255,255,255,.3)',
         
            series: [{
              name: 'Line 1',
              type: 'pie',
              clockWise: true,
              radius: ['65%', '80%'],
              itemStyle: {
                normal: {
                  label: {
                    show: false
                  },
                  labelLine: {
                    show: false
                  }
                }
              },
              hoverAnimation: false,
              data: [{
                value: txt,
                name: '已使用',
                itemStyle: {
                  normal: {
                    color:'#eaff00',
                    label: {
                      show: false
                    },
                    labelLine: {
                      show: false
                    }
                  }
                }
              }, {
                name: '未使用',
                value: 100-txt
              }]
            }]
        };

        // 使用刚指定的配置项和数据显示图表。
        myChart.setOption(option);
        window.addEventListener("resize",function(){
            myChart.resize();
        });
    }

    function pe02() {
        // 基于准备好的dom，初始化echarts实例
        var myChart = echarts.init(document.getElementById('pe02'));
        var txt=17
        option = {
            title: {
              text: txt+'%',
              x: 'center',
             y: 'center',
              textStyle: {
                fontWeight: 'normal',
                color: '#fff',
                fontSize: '18'
              }
            },
            color:'rgba(255,255,255,.3)',
         
            series: [{
              name: 'Line 1',
              type: 'pie',
              clockWise: true,
              radius: ['65%', '80%'],
              itemStyle: {
                normal: {
                  label: {
                    show: false
                  },
                  labelLine: {
                    show: false
                  }
                }
              },
              hoverAnimation: false,
              data: [{
                value: txt,
                name: '已使用',
                itemStyle: {
                  normal: {
                    color:'#ea4d4d',
                    label: {
                      show: false
                    },
                    labelLine: {
                      show: false
                    }
                  }
                }
              }, {
                name: '未使用',
                value: 100-txt
              }]
            }]
        };

        // 使用刚指定的配置项和数据显示图表。
        myChart.setOption(option);
        window.addEventListener("resize",function(){
            myChart.resize();
        });
    }
    function pe03() {
        // 基于准备好的dom，初始化echarts实例
        var myChart = echarts.init(document.getElementById('pe03'));
        var txt=2
        option = {
            title: {
              text: txt+'%',
              x: 'center',
             y: 'center',
              textStyle: {
                fontWeight: 'normal',
                color: '#fff',
                fontSize: '18'
              }
            },
            color:'rgba(255,255,255,.3)',
         
            series: [{
              name: 'Line 1',
              type: 'pie',
              clockWise: true,
              radius: ['65%', '80%'],
              itemStyle: {
                normal: {
                  label: {
                    show: false
                  },
                  labelLine: {
                    show: false
                  }
                }
              },
              hoverAnimation: false,
              data: [{
                value: txt,
                name: '已使用',
                itemStyle: {
                  normal: {
                    color:'#395ee6',
                    label: {
                      show: false
                    },
                    labelLine: {
                      show: false
                    }
                  }
                }
              }, {
                name: '未使用',
                value: 100-txt
              }
            ]
            }]
        };

        // 使用刚指定的配置项和数据显示图表。
        myChart.setOption(option);
        window.addEventListener("resize",function(){
            myChart.resize();
        });
    }
})



		
		
		


		



















