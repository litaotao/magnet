model_1 = '''
option = {
    title : {
        text: 'Magnet Human Relation',
        subtext: 'You are just one node in the boundless human relation net',
        x:'right',
        y:'bottom'
    },
    tooltip : {
        trigger: 'item',
        formatter: '{a} : {b}',
        borderWidth: 1,
        axisPointer: {
                        type : 'line',
                        lineStyle : {
                          color: '#48b',
                          width: 2,
                          type: 'solid'
                        }
                    }
    },
    toolbox: {
        show : true,
        feature : {
            restore : {show: true, title: 'reset'},
            saveAsImage : {show: true, title: 'save as image'},
            dataZoom : {show : true}
        }
    },
    legend: {
        x: 'left',
        data:[]
    },
    series : [
    {
        type:'force',
        name : "People",
        categories : [
            {
                name: 'level 1'
            },
            {
                name: 'level 2'
            },
            {
                name: 'level 3'
            },
            {
                name: 'level 4'
            },
            {
                name: 'level 5'
            }
        ],
        itemStyle: {
            normal: {
                label: {
                    show: true,
                    textStyle: {
                        color: '#800080'
                    }
                },
                nodeStyle : {
                    brushType : 'both',
                    strokeColor : 'rgba(255,215,0,0.4)',
                    lineWidth : 1
                }
            },
            emphasis: {
                label: {
                    show: true
                },
                nodeStyle : {
                },
                linkStyle : {}
            }
        },
        minRadius : 15,
        maxRadius : 25,
        density : 0.1,
        attractiveness: 1,
        linkSymbol: 'arrow',
        draggable: true,
        nodes:
            {{nodes|safe}}
        ,
        links:
            {{links|safe}}
    }
    ]
};
'''