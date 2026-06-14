<script setup>
// 逻辑代码
import { h, onMounted, ref, resolveDirective, withDirectives, nextTick } from 'vue'
import {
  NButton,
  NCheckbox,
  NCheckboxGroup,
  NForm,
  NFormItem,
  NImage,
  NInput,
  NSpace,
  NSwitch,
  NTag,
  NSelect,
  NPopconfirm,
  NLayout,
  NRadioGroup, 
  NRadioButton,
  NLayoutSider,
  NLayoutContent,
  NTreeSelect,
} from 'naive-ui'
import CommonPage from '@/components/page/CommonPage.vue'
import QueryBarItem from '@/components/query-bar/QueryBarItem.vue'
import CrudModal from '@/components/table/CrudModal.vue'
import CrudTable from '@/components/table/CrudTable.vue'
import TheIcon from '@/components/icon/TheIcon.vue'
import * as echarts from 'echarts'
import { renderIcon } from '@/utils'
import { useCRUD } from '@/composables'
import api from '@/api'

defineOptions({ name: '全球尺度' })

// 灾害类型颜色映射
const disasterColors = {
  // 基础灾害类型
  'Drought': '#FFD700',          // 金色代表干旱
  'Flood': '#4169E1',            // 皇家蓝代表洪水
  'Extreme temperature': '#DC143C', // 深红代表极端温度
  'Volcanic activity': '#800080',  // 紫色代表火山活动
  'Storm': '#00BFFF',             // 深天蓝代表风暴
  'Wildfire': '#FF4500',          // 橙红代表野火
  'Earthquake': '#FFA500',        // 橙色代表地震
  // 生物相关灾害
  'Epidemic': '#32CD32',          // 酸橙绿代表疫情
  'Infestation': '#9ACD32',       // 黄绿代表虫害
  'Animal incident': '#8B4513',   // 鞍棕色代表动物事件
  // 地质运动类
  'Mass movement (wet)': '#A0522D', // 土色代表湿物质运动
  'Mass movement (dry)': '#D2691E', // 巧克力色代表干物质运动
  // 特殊灾害
  'Impact': '#696969',            // 暗灰代表撞击事件
  'Glacial lake outburst flood': '#87CEEB', // 冰蓝色代表冰川湖溃决洪水
}

const yearOptions = [
  { label: '近10年', value: 10 },
  { label: '近20年', value: 20 },
  { label: '近25年', value: 25 }
]

const selectedYears = ref(10)
const chartLeft = ref(null)
const chartRight = ref(null)
let leftChart = null
let rightChart = null

const chartLeft2 = ref(null)
const chartRight2 = ref(null)
let leftChart2 = null
let rightChart2 = null

const chartLeft3 = ref(null)
const chartRight3 = ref(null)
let leftChart3 = null
let rightChart3 = null

// 获取图表数据
async function fetchChartData() {
  try {
    const [res1, res2, res3, res4, res5, res6] = await Promise.all([
      api.getYearCount({ n: selectedYears.value }),
      api.getYearCountByType({ n: selectedYears.value }),
      api.getRecentStats({ n: selectedYears.value }),
      api.getRecentStatsByType({ n: selectedYears.value }),
      api.getRecentLoss({ n: selectedYears.value }),
      api.getRecentLossByType({ n: selectedYears.value }),
    ])
    
    initCharts(res1.data, res2.data, res3.data, res4.data, res5.data, res6.data)
  } catch (error) {
    console.error('获取图表数据失败:', error)
  }
}

// 初始化图表
function initCharts(data1, data2, data3, data4, data5, data6) {
  nextTick(() => {
    // 销毁旧图表
    if (leftChart) leftChart.dispose()
    if (rightChart) rightChart.dispose()
    if (leftChart2) leftChart2.dispose()
    if (rightChart2) rightChart2.dispose()
    if (leftChart3) leftChart3.dispose()
    if (rightChart3) rightChart3.dispose()
    
    // 初始化新图表
    leftChart = echarts.init(chartLeft.value)
    rightChart = echarts.init(chartRight.value)
    leftChart2 = echarts.init(chartLeft2.value)
    rightChart2 = echarts.init(chartRight2.value)
    leftChart3 = echarts.init(chartLeft3.value)
    rightChart3 = echarts.init(chartRight3.value)

    // 处理数据
    const years = data1.map(d => d.start_year)
    const counts = data1.map(d => d.count)

    const total_count = data2.map(d => d.total_count)
    const total = total_count.reduce((sum, cur) => sum + cur, 0)

    // 左图配置（柱状+折线）
    const leftOption = {
      tooltip: { trigger: 'axis' },
      xAxis: {
        type: 'category',
        data: years,
        name: '年份'
      },
      yAxis: { type: 'value', name: '总频次(次)' },
      series: [
        {
          name: '灾害次数',
          type: 'bar',
          data: counts,
          itemStyle: { color: '#5470C6' }
        },
        {
          name: '趋势线',
          type: 'line',
          data: counts,
          smooth: true,
          itemStyle: { color: '#91CC75' }
        }
      ]
    }

    // 右图配置（饼图）
    const rightOption = {
      tooltip: { trigger: 'item' },
      legend: {
        orient: 'horizontal',
        top: 10,
        itemGap: 8,
        right: 50,
        textStyle: {
          color: '#666',
        }
      },
      series: [{
        type: 'pie',
        radius: ['35%', '55%'],
        center: ['50%', '57%'],
        data: data2.map(d => ({
          name: d.disaster_type,
          value: d.total_count,
          percent: ((d.total_count / total) * 100).toFixed(2) + '%',
          itemStyle: {
            color: disasterColors[d.disaster_type]
          }
        })),
        label: {
          formatter: '{b}: {c}次 ({d}%)'
        },
        itemStyle: {
          borderWidth: 1,
          borderColor: '#fff',
          shadowBlur: 5,
          shadowColor: 'rgba(0, 0, 0, 0.2)'
        },
      }]
    }

    // 左图2配置（双Y轴）
    const leftOption2 = {
      tooltip: { trigger: 'axis' },
      legend: { data: ['影响人数', '伤亡人数'] },
      xAxis: {
        type: 'category',
        data: data3.map(d => d.start_year),
        name: '年份'
      },
      yAxis: [
        {
          type: 'value',
          name: '影响人数(万人)',
          axisLabel: { formatter: value => (value / 10000).toFixed(0) }
        },
        {
          type: 'value',
          name: '伤亡人数(千人)',
          axisLabel: { formatter: value => (value / 1000).toFixed(0) }
        }
      ],
      series: [
        {
          name: '影响人数',
          type: 'bar',
          data: data3.map(d => d.total_affected_sum),
          itemStyle: { color: '#FF0000' }
        },
        {
          name: '伤亡人数',
          type: 'line',
          yAxisIndex: 1,
          data: data3.map(d => d.death_injured_sum),
          smooth: true,
          itemStyle: { color: '#B22222' }
        }
      ]
    }

    // 右图2配置（嵌套饼图）
    const totalAffected = data4.reduce((sum, d) => sum + d.total_affected_sum, 0)
    const totalDeath = data4.reduce((sum, d) => sum + d.death_injured_sum, 0)
    
    // 右图2配置（嵌套饼图-无标签版）
    const rightOption2 = {
      tooltip: {
        trigger: 'item',
        formatter: ({ seriesName, name, value, percent }) => `
          ${name}<br/>
          ${seriesName}: ${value.toLocaleString()}人<br/>
          占比: ${percent}%
        `
      },
      legend: {
        orient: 'horizontal',
        right: 20,
        bottom: 55,
        itemGap: 8,
        right: 50,
        textStyle: {
          color: '#666',
        }
      },
      series: [
        { // 内圈-影响人数
          type: 'pie',
          name: '影响人数',
          radius: ['20%', '35%'],
          center: ['50%', '40%'],
          label: { show: false }, // 关闭标签
          data: data4.map(d => ({
            name: d.disaster_type,
            value: d.total_affected_sum,
            itemStyle: {
              color: disasterColors[d.disaster_type]
            }
          })),
          itemStyle: {
            borderWidth: 1,
            borderColor: '#fff',
            shadowBlur: 5,
            shadowColor: 'rgba(0, 0, 0, 0.2)'
          },
        },
        { // 外圈-伤亡人数
          type: 'pie',
          name: '伤亡人数',
          radius: ['40%', '55%'],
          center: ['50%', '40%'],
          label: { show: false }, // 关闭标签
          data: data4.map(d => ({
            name: d.disaster_type,
            value: d.death_injured_sum,
            itemStyle: {
              color: disasterColors[d.disaster_type]
            }
          })),
          itemStyle: {
            borderWidth: 1,
            borderColor: '#fff',
            shadowBlur: 5,
            shadowColor: 'rgba(0, 0, 0, 0.2)'
          },
        }
      ]
    }

    // 左图3配置（柱状+折线）
    const leftOption3 = {
      tooltip: { trigger: 'axis' },
      xAxis: {
        type: 'category',
        data: data5.map(d => d.start_year),
        name: '年份'
      },
      yAxis: { type: 'value', name: '直接经济损失(千美元)' },
      series: [
        {
          name: '直接经济损失',
          type: 'bar',
          data: data5.map(d => d.total_loss),
          itemStyle: { color: '#7FFF00' }
        },
        {
          name: '趋势线',
          type: 'line',
          data: data5.map(d => d.total_loss),
          smooth: true,
          itemStyle: { color: '#006400' }
        }
      ]
    }

    const totalLoss = data6.reduce((sum, d) => sum + d.total_loss, 0)
    // 右图3配置（饼图）
    const rightOption3 = {
      tooltip: { trigger: 'item' },
      legend: {
        orient: 'horizontal',
        top: 10,
        itemGap: 8,
        right: 50,
        textStyle: {
          color: '#666',
        }
      },
      series: [{
        type: 'pie',
        radius: ['35%', '55%'],
        center: ['50%', '57%'],
        data: data6.map(d => ({
          name: d.disaster_type,
          value: d.total_loss,
          percent: ((d.total_loss / totalLoss) * 100).toFixed(2) + '%',
          itemStyle: {
            color: disasterColors[d.disaster_type]
          }
        })),
        label: {
          formatter: '{b}: ({d}%)'
        },
        itemStyle: {
          borderWidth: 1,
          borderColor: '#fff',
          shadowBlur: 5,
          shadowColor: 'rgba(0, 0, 0, 0.2)'
        },
      }]
    }

    leftChart.setOption(leftOption)
    rightChart.setOption(rightOption)
    leftChart2.setOption(leftOption2)
    rightChart2.setOption(rightOption2) 
    leftChart3.setOption(leftOption3)
    rightChart3.setOption(rightOption3) 
    
    // 窗口自适应
    window.addEventListener('resize', () => {
      leftChart.resize()
      rightChart.resize()
      leftChart2.resize()
      rightChart2.resize()
      leftChart3.resize()
      rightChart3.resize()
    })
  })
}

onMounted(() => {
  fetchChartData()
})

const {
  modalVisible,
  modalTitle,
  modalLoading,
  handleSave,
  modalForm,
  modalFormRef,
  handleEdit,
  handleDelete,
  handleAdd,
} = useCRUD({
  name: '灾害',
  initForm: {}, // 根据业务字段调整
  doCreate: api.createDisaster,
  doUpdate: api.updateDisaster,
  doDelete: api.deleteDisaster,
  refresh: () => $table.value?.handleSearch(),
})
</script>

<template>
  <CommonPage show-footer title="全球尺度">
    <template #action>
      <NSpace>
        <NSelect 
          v-model:value="selectedYears" 
          :options="yearOptions" 
          style="width: 150px"
          @update:value="fetchChartData"
        />
      </NSpace>
    </template>

    <NSpace vertical :size="12" style="margin-bottom: 20px">
      <n-card embedded size="medium" hoverable>
        <NSpace justify="space-between" align="center" style="width: 100%">
          <NSpace>
            <TheIcon icon="ion:stats-chart" color="#2d8cf0" :size="24" />
            <NText depth="5" style="font-size: 17px">总频次统计</NText>
          </NSpace>
          <NSpace :size="12">
            <NTag type="info" round size="medium">单位：次</NTag>
            <NTag type="success" round size="medium">时间范围：近{{ selectedYears }}年</NTag>
          </NSpace>
        </NSpace>
      </n-card>
    </NSpace>

    <!-- 总频次统计 -->
    <NLayout has-sider style="height: 500px; margin-top: 20px">
      <NLayoutContent content-style="padding: 0 10px 0 0">
        <div 
          ref="chartLeft" 
          style="width: 100%; height: 500px; background: white; padding: 0px; border-radius: 8px;"
        ></div>
      </NLayoutContent>
      
      <NLayoutSider
        content-style="padding: 0 0 0 10px"
        :width="600"
        collapse-mode="transform"
      >
        <div 
          ref="chartRight" 
          style="width: 100%; height: 500px; background: white; padding: 0px; border-radius: 8px;"
        ></div>
      </NLayoutSider>
    </NLayout>

    <NSpace vertical :size="12" style="margin-bottom: 20px">
      <n-card embedded size="medium" hoverable>
        <NSpace justify="space-between" align="center" style="width: 100%">
          <NSpace>
            <TheIcon icon="ion:stats-chart" color="#2d8cf0" :size="24" />
            <NText depth="5" style="font-size: 17px">影响人数/伤亡人数</NText>
          </NSpace>
          <NSpace :size="12">
            <NTag type="info" round size="medium">单位：人</NTag>
            <NTag type="success" round size="medium">时间范围：近{{ selectedYears }}年</NTag>
          </NSpace>
        </NSpace>
      </n-card>
    </NSpace>

    <!-- 影响人数/死亡受伤人数 -->
    <NLayout has-sider embedded style="height: 500px; margin-top: 20px">
      <NLayoutContent content-style="padding: 0 10px 0 0">
        <div 
          ref="chartLeft2" 
          style="width: 100%; height: 500px; background: white; border-radius: 8px;"
        ></div>
      </NLayoutContent>
      
      <NLayoutSider
        content-style="padding: 0 0 0 10px"
        :width="600"
        collapse-mode="transform"
      >
        <div 
          ref="chartRight2" 
          style="width: 100%; height: 500px; background: white; border-radius: 8px;"
        ></div>
      </NLayoutSider>
    </NLayout>

    <NSpace vertical :size="12" style="margin-bottom: 20px">
      <n-card embedded size="medium" hoverable>
        <NSpace justify="space-between" align="center" style="width: 100%">
          <NSpace>
            <TheIcon icon="ion:stats-chart" color="#2d8cf0" :size="24" />
            <NText depth="5" style="font-size: 17px">直接经济损失</NText>
          </NSpace>
          <NSpace :size="12">
            <NTag type="info" round size="medium">单位：千美元</NTag>
            <NTag type="success" round size="medium">时间范围：近{{ selectedYears }}年</NTag>
          </NSpace>
        </NSpace>
      </n-card>
    </NSpace>

    <!-- 直接经济损失 -->
    <NLayout has-sider style="height: 500px; margin-top: 20px">
      <NLayoutContent content-style="padding: 0 10px 0 0">
        <div 
          ref="chartLeft3" 
          style="width: 100%; height: 500px; background: white; padding: 0px; border-radius: 8px;"
        ></div>
      </NLayoutContent>
      
      <NLayoutSider
        content-style="padding: 0 0 0 10px"
        :width="600"
        collapse-mode="transform"
      >
        <div 
          ref="chartRight3" 
          style="width: 100%; height: 500px; background: white; padding: 0px; border-radius: 8px;"
        ></div>
      </NLayoutSider>
    </NLayout>
  </CommonPage>
</template>