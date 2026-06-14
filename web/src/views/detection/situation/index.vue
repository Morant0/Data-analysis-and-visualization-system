<script setup>
import { ref, computed, watch, onMounted, onUnmounted } from 'vue'
import * as echarts from 'echarts'
import {
  NSelect,
  NDatePicker,
  NLayout,
  NLayoutSider,
  NLayoutContent,
  NCard,
  NSpace,
  NTag
} from 'naive-ui'
import CommonPage from '@/components/page/CommonPage.vue'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'
import continentGeoJSON from '@/geojson/continent.json'
import api from '@/api'

// 配置数据
const continentMapping = {
  'Afghanistan': 'Asia',
  'Albania': 'Europe',
  'Algeria': 'Africa',
  'Angola': 'Africa',
  'Argentina': 'South America',
  'Australia': 'Oceania',
  'Austria': 'Europe',
  'Azerbaijan': 'Asia',
  'Bahamas': 'North America',
  'Bahrain': 'Asia',
  'Bangladesh': 'Asia',
  'Barbados': 'North America',
  'Belarus': 'Europe',
  'Belgium': 'Europe',
  'Belize': 'North America',
  'Benin': 'Africa',
  'Bhutan': 'Asia',
  'Bolivia (Plurinational State of)': 'South America',
  'Bosnia and Herzegovina': 'Europe',
  'Botswana': 'Africa',
  'Brazil': 'South America',
  'Brunei Darussalam': 'Asia',
  'Bulgaria': 'Europe',
  'Burkina Faso': 'Africa',
  'Burundi': 'Africa',
  'Cabo Verde': 'Africa',
  'Cambodia': 'Asia',
  'Cameroon': 'Africa',
  'Canada': 'North America',
  'Central African Republic': 'Africa',
  'Chad': 'Africa',
  'Chile': 'South America',
  'China': 'Asia',
  'China, Hong Kong Special Administrative Region': 'Asia',
  'China, Macao Special Administrative Region': 'Asia',
  'Colombia': 'South America',
  'Comoros': 'Africa',
  'Congo': 'Africa',
  'Cook Islands': 'Oceania',
  'Costa Rica': 'North America',
  'Côte d’Ivoire': 'Africa',
  'Croatia': 'Europe',
  'Cuba': 'North America',
  'Cyprus': 'Asia',
  'Czechia': 'Europe',
  'Democratic People\'s Republic of Korea': 'Asia',
  'Democratic Republic of the Congo': 'Africa',
  'Denmark': 'Europe',
  'Djibouti': 'Africa',
  'Dominica': 'North America',
  'Dominican Republic': 'North America',
  'Ecuador': 'South America',
  'Egypt': 'Africa',
  'El Salvador': 'North America',
  'Equatorial Guinea': 'Africa',
  'Eritrea': 'Africa',
  'Estonia': 'Europe',
  'Eswatini': 'Africa',
  'Ethiopia': 'Africa',
  'Fiji': 'Oceania',
  'Finland': 'Europe',
  'France': 'Europe',
  'Gabon': 'Africa',
  'Gambia': 'Africa',
  'Georgia': 'Asia',
  'Germany': 'Europe',
  'Ghana': 'Africa',
  'Greece': 'Europe',
  'Grenada': 'North America',
  'Guatemala': 'North America',
  'Guinea': 'Africa',
  'Guinea-Bissau': 'Africa',
  'Guyana': 'South America',
  'Haiti': 'North America',
  'Honduras': 'North America',
  'Hungary': 'Europe',
  'Iceland': 'Europe',
  'India': 'Asia',
  'Indonesia': 'Asia',
  'Iran (Islamic Republic of)': 'Asia',
  'Iraq': 'Asia',
  'Ireland': 'Europe',
  'Israel': 'Asia',
  'Italy': 'Europe',
  'Jamaica': 'North America',
  'Japan': 'Asia',
  'Jordan': 'Asia',
  'Kazakhstan': 'Asia',
  'Kenya': 'Africa',
  'Kiribati': 'Oceania',
  'Kuwait': 'Asia',
  'Kyrgyzstan': 'Asia',
  'Laos': 'Asia',
  'Latvia': 'Europe',
  'Lebanon': 'Asia',
  'Lesotho': 'Africa',
  'Liberia': 'Africa',
  'Libya': 'Africa',
  'Liechtenstein': 'Europe',
  'Lithuania': 'Europe',
  'Luxembourg': 'Europe',
  'Madagascar': 'Africa',
  'Malawi': 'Africa',
  'Malaysia': 'Asia',
  'Maldives': 'Asia',
  'Mali': 'Africa',
  'Malta': 'Europe',
  'Marshall Islands': 'Oceania',
  'Mauritania': 'Africa',
  'Mauritius': 'Africa',
  'Mexico': 'North America',
  'Micronesia (Federated States of)': 'Oceania',
  'Moldova': 'Europe',
  'Monaco': 'Europe',
  'Mongolia': 'Asia',
  'Montenegro': 'Europe',
  'Morocco': 'Africa',
  'Mozambique': 'Africa',
  'Myanmar': 'Asia',
  'Namibia': 'Africa',
  'Nepal': 'Asia',
  'Netherlands': 'Europe',
  'New Caledonia': 'Oceania',
  'New Zealand': 'Oceania',
  'Nicaragua': 'North America',
  'Niger': 'Africa',
  'Nigeria': 'Africa',
  'Niue': 'Oceania',
  'North Macedonia': 'Europe',
  'Norway': 'Europe',
  'Oman': 'Asia',
  'Pakistan': 'Asia',
  'Palau': 'Oceania',
  'Panama': 'North America',
  'Papua New Guinea': 'Oceania',
  'Paraguay': 'South America',
  'Peru': 'South America',
  'Philippines': 'Asia',
  'Poland': 'Europe',
  'Portugal': 'Europe',
  'Qatar': 'Asia',
  'Réunion': 'Africa',
  'Romania': 'Europe',
  'Russian Federation': 'Europe',
  'Rwanda': 'Africa',
  'Saint Helena': 'Africa',
  'Saint Kitts and Nevis': 'North America',
  'Saint Lucia': 'North America',
  'Saint Vincent and the Grenadines': 'North America',
  'Samoa': 'Oceania',
  'San Marino': 'Europe',
  'Saudi Arabia': 'Asia',
  'Senegal': 'Africa',
  'Serbia': 'Europe',
  'Seychelles': 'Africa',
  'Sierra Leone': 'Africa',
  'Singapore': 'Asia',
  'Slovakia': 'Europe',
  'Slovenia': 'Europe',
  'Solomon Islands': 'Oceania',
  'Somalia': 'Africa',
  'South Africa': 'Africa',
  'South Sudan': 'Africa',
  'Spain': 'Europe',
  'Sri Lanka': 'Asia',
  'Sudan': 'Africa',
  'Suriname': 'South America',
  'Swaziland': 'Africa',
  'Sweden': 'Europe',
  'Switzerland': 'Europe',
  'Syrian Arab Republic': 'Asia',
  'Tajikistan': 'Asia',
  'Tanzania': 'Africa',
  'Thailand': 'Asia',
  'Timor-Leste': 'Asia',
  'Togo': 'Africa',
  'Tonga': 'Oceania',
  'Trinidad and Tobago': 'North America',
  'Tunisia': 'Africa',
  'Turkey': 'Asia',
  'Turkmenistan': 'Asia',
  'Tuvalu': 'Oceania',
  'Uganda': 'Africa',
  'Ukraine': 'Europe',
  'United Arab Emirates': 'Asia',
  'United Kingdom of Great Britain and Northern Ireland': 'Europe',
  'United Republic of Tanzania': 'Africa',
  'United States of America': 'North America',
  'Uruguay': 'South America',
  'Uzbekistan': 'Asia',
  'Vanuatu': 'Oceania',
  'Venezuela (Bolivarian Republic of)': 'South America',
  'Viet Nam': 'Asia',
  'Wallis and Futuna Islands': 'Oceania',
  'Yemen': 'Asia',
  'Zambia': 'Africa',
  'Zimbabwe': 'Africa'
}

const disasterOptions = [
  { label: '干旱', value: 'Drought' },
  { label: '洪涝', value: 'Flood' },
  { label: '极端温度', value: 'Extreme temperature' },
  { label: '火山活动', value: 'Volcanic activity' },
  { label: '风暴', value: 'Storm' },
  { label: '野火', value: 'Wildfire' },
  { label: '地震', value: 'Earthquake' },
  { label: '疫情', value: 'Epidemic' },
  { label: '湿物质运动', value: 'Mass movement (wet)' },
  { label: '虫害', value: 'Infestation' },
  { label: '干物质运动', value: 'Mass movement (dry)' },
  { label: '撞击事件', value: 'Impact' },
  { label: '动物事件', value: 'Animal incident' },
  { label: '冰川湖溃决洪水', value: 'Glacial lake outburst flood' }
]

// 地图配置
const mapConfig = {
  '总频次': {
    api: api.getCountryCount,
    colorRange: ['#e7f0fd', '#cfe2fc', '#a6c4fa', '#6ea1f7', '#3b82f6'],
    field: 'count'
  },
  '影响人数': {
    api: api.getCountryAffected,
    colorRange: ['#e6f6ec', '#c3ead4', '#95d9b4', '#5dc38d', '#22c55e'],
    field: 'total_affected'
  },
  '伤亡人口': {
    api: api.getCoutry_casualties,
    colorRange: ['#fee2e2', '#fecaca', '#fca5a5', '#f87171', '#ef4444'],
    field: 'total_casualties'
  },
  '经济损失': {
    api: api.getCountry_Loss,
    colorRange: ['#fef3c7', '#fde68a', '#fcd34d', '#fbbf24', '#f59e0b'],
    field: 'total_loss'
  }
}

const selectedMap = ref('总频次')
const timeRange = ref('1y')
const disasterType = ref('')
const customDateRange = ref(null)
const mapInstance = ref(null)
const geoJsonLayer = ref(null)
const legend = ref(null)

// 修改时间范围计算逻辑
const dateRange = computed(() => {
  if (timeRange.value === 'custom') {
    return [
      new Date(customDateRange.value[0]),
      new Date(customDateRange.value[1])
    ]
  }

  const now = new Date()
  const ranges = {
    '1y': [new Date(new Date().setFullYear(new Date().getFullYear() - 1)), new Date()],
    '6m': [new Date(new Date().setMonth(new Date().getMonth() - 6)), new Date()],
    '3m': [new Date(new Date().setMonth(new Date().getMonth() - 3)), new Date()],
    '1m': [new Date(new Date().setMonth(new Date().getMonth() - 1)), new Date()]
  }
  return ranges[timeRange.value] || null
})

// 修改获取数据逻辑
async function fetchData() {
  if (!dateRange.value || !dateRange.value[0] || !dateRange.value[1]) return
  const config = mapConfig[selectedMap.value]
  const start = dateRange.value[0]
  const end = dateRange.value[1]
  
  // 确保日期格式正确
  const formatDate = d => d.toISOString().split('T')[0]
  
  const res = await config.api({
    start_date: formatDate(start),
    end_date: formatDate(end),
    disaster_type: disasterType.value
  })
  
  // 保持原有聚合逻辑不变
  const continentData = res.data.reduce((acc, item) => {
    const continent = continentMapping[item.country] || '其他'
    acc[continent] = (acc[continent] || 0) + item[config.field]
    return acc
  }, {})

  updateMap(continentData)
}

// 更新地图样式
function updateMap(data) {
  if (geoJsonLayer.value) {
    mapInstance.value.removeLayer(geoJsonLayer.value)
  }

  const config = mapConfig[selectedMap.value]
  const values = Object.values(data).filter(v => v > 0)
  const max = Math.max(...values)
  const intervals = createIntervals(max, 5)

  geoJsonLayer.value = L.geoJSON(continentGeoJSON, {
    style: feature => {
      const value = data[feature.properties.name] || 0
      return {
        fillColor: getColor(value, intervals, config.colorRange),
        weight: 1,
        color: '#666',
        fillOpacity: 0.8
      }
    }
  }).addTo(mapInstance.value)

  updateLegend(intervals, config.colorRange)
}

// 创建颜色区间
function createIntervals(max, steps) {
  if (max === 0) return [0]
  const step = max / steps
  return Array.from({ length: steps }, (_, i) => Math.ceil(step * (i + 1)))
}

// 获取颜色
function getColor(value, intervals, colors) {
  if (value === 0) return '#f3f4f6'
  for (let i = 0; i < intervals.length; i++) {
    if (value <= intervals[i]) return colors[i]
  }
  return colors[colors.length - 1]
}

// 更新图例
function updateLegend(intervals, colors) {
  if (legend.value) {
    legend.value.remove()
  }

  legend.value = L.control({ position: 'bottomright' })
  legend.value.onAdd = () => {
    const div = L.DomUtil.create('div', 'legend')
    div.innerHTML = `
      <h4>${selectedMap.value}图例</h4>
      ${intervals.map((max, i) => `
        <div class="legend-item">
          <i style="background:${colors[i]}"></i>
          ${i === 0 ? `0-${max}` : `${intervals[i-1]+1}-${max}`}
        </div>
      `).join('')}
    `
    return div
  }
  legend.value.addTo(mapInstance.value)
}

// 新增图表相关逻辑
const chart1 = ref(null)
const chart2 = ref(null)
const chart3 = ref(null)
const chart4 = ref(null)
const chart1Ref = ref(null)
const chart2Ref = ref(null)
const chart3Ref = ref(null)
const chart4Ref = ref(null)

// 处理数据响应
async function fetchChartData() {
  if (!dateRange.value || !dateRange.value[0] || !dateRange.value[1]) return
  
  const formatDate = d => d.toISOString().split('T')[0]
  const params = {
    start_date: formatDate(dateRange.value[0]),
    end_date: formatDate(dateRange.value[1]),
    disaster_type: disasterType.value
  }

  try {
    const [countRes, lossRes, casualtiesRes, affectedRes] = await Promise.all([
      api.getCountryCount(params),
      api.getCountry_Loss(params),
      api.getCoutry_casualties(params),
      api.getCountryAffected(params)
    ])

    console.log([countRes, lossRes, casualtiesRes, affectedRes])

    updateChart(chart1.value, processData(countRes.data, 'count'), '频次', '#3b82f6')
    updateChart(chart2.value, processData(lossRes.data, 'total_loss'), '经济损失（千美元）', '#f59e0b')
    updateChart(chart3.value, processData(casualtiesRes.data, 'total_casualties'), '伤亡人口', '#ef4444')
    updateChart(chart4.value, processData(affectedRes.data, 'total_affected'), '影响人数', '#22c55e')

  } catch (error) {
    console.error('图表数据获取失败:', error)
  }
}

function processData(data, field) {
  return data
    .filter(item => item[field] > 0)
    .sort((a, b) => b[field] - a[field])
    .slice(0, 10)
    .map(item => ({
      country: item.country,
      value: item[field]
    }))
}

function updateChart(chartInstance, data, xName, color) {
  if (!chartInstance) return
  
  const option = {
    tooltip: {
      trigger: 'axis',
      axisPointer: { type: 'shadow' }
    },
    xAxis: {
      name: xName,
      type: 'value'
    },
    yAxis: {
      type: 'category',
      data: data.map(d => d.country),
      axisLabel: {
        fontSize: 12
      }
    },
    series: [{
      type: 'bar',
      data: data.map(d => d.value),
      itemStyle: { color }
    }],
    grid: {
      left: '15%',
    }
  }
  chartInstance.setOption(option)
}

// 初始化地图
onMounted(() => {
  mapInstance.value = L.map('map-container', {
    attributionControl: false,
    minZoom: 2,  // 设置最小缩放级别
    maxZoom: 18   // 设置最大缩放级别
  }).setView([35, 105], 3) // 调整初始中心点到中国位置，缩放级别设为4

  L.tileLayer('https://webrd0{s}.is.autonavi.com/appmaptile?lang=zh_cn&size=1&scale=1&style=8&x={x}&y={y}&z={z}', {
    subdomains: ['1', '2', '3', '4'],
    minZoom: 2,  // 设置瓦片最小级别
    maxZoom: 18   // 设置瓦片最大级别
  }).addTo(mapInstance.value)

  fetchData()
  fetchChartData()

  chart1.value = echarts.init(chart1Ref.value)
  chart2.value = echarts.init(chart2Ref.value)
  chart3.value = echarts.init(chart3Ref.value)
  chart4.value = echarts.init(chart4Ref.value)
  window.addEventListener('resize', handleResize)
})

// 销毁图表
onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
  ;[chart1, chart2, chart3, chart4].forEach(c => c.value?.dispose())
})

function handleResize() {
  ;[chart1, chart2, chart3, chart4].forEach(c => c.value?.resize())
}

// 监听参数变化
watch(selectedMap, fetchData)
watch([timeRange, disasterType, customDateRange], () => {
  fetchData()
  fetchChartData()
})
</script>

<template>
  <CommonPage show-footer title="态势分析">
    <NLayout has-sider>
      <NLayoutSider
        :width="300"
        :native-scrollbar="false"
        content-style="padding: 20px;"
        bordered
      >
        <NSpace vertical :size="24">
          <NCard title="地图选择" size="small">
            <NSelect
              v-model:value="selectedMap"
              :options="[
                { label: '总频次', value: '总频次' },
                { label: '影响人数', value: '影响人数' },
                { label: '伤亡人口', value: '伤亡人口' },
                { label: '经济损失', value: '经济损失' }
              ]"
            />
          </NCard>

          <NCard title="时间范围" size="small">
            <NSpace vertical>
              <NSelect
                v-model:value="timeRange"
                :options="[
                  { label: '近1年', value: '1y' },
                  { label: '近6个月', value: '6m' },
                  { label: '近3个月', value: '3m' },
                  { label: '近1个月', value: '1m' },
                  { label: '自定义', value: 'custom' }
                ]"
              />
              <NDatePicker
                v-if="timeRange === 'custom'"
                v-model:value="customDateRange"
                type="daterange"
                clearable
              />
            </NSpace>
          </NCard>

          <NCard title="灾害类型" size="small">
            <NSelect
              v-model:value="disasterType"
              placeholder="请选择"
              :options="disasterOptions"
              filterable
              clearable
            />
          </NCard>
        </NSpace>
      </NLayoutSider>

      <NLayoutContent>
        <div id="map-container" class="h-full"></div>
      </NLayoutContent>
    </NLayout>

    <NSpace vertical :size="12" style="margin-top: 20px">
      <n-card embedded size="medium" hoverable>
        <NSpace justify="space-between" align="center" style="width: 100%">
          <NSpace>
            <TheIcon icon="ion:stats-chart" color="#2d8cf0" :size="24" />
            <NText depth="5" style="font-size: 17px">各国家灾害频次排行</NText>
          </NSpace>
          <NSpace :size="12">
            <NTag type="info" size="medium">前10名</NTag>
          </NSpace>
        </NSpace>
      </n-card>
    </NSpace>

    <NLayout has-sider style="height: 400px;">
      <NLayoutContent>
        <div 
          ref="chart1Ref" 
          style="width: 100%; height: 400px; background: white; padding: 0px; border-radius: 8px;"
        ></div>
      </NLayoutContent>
    </NLayout>

    <NSpace vertical :size="12">
      <n-card embedded size="medium" hoverable>
        <NSpace justify="space-between" align="center" style="width: 100%">
          <NSpace>
            <TheIcon icon="ion:stats-chart" color="#2d8cf0" :size="24" />
            <NText depth="5" style="font-size: 17px">各国家灾害影响人数排行</NText>
          </NSpace>
          <NSpace :size="12">
            <NTag type="info" size="medium">前10名</NTag>
          </NSpace>
        </NSpace>
      </n-card>
    </NSpace>

    <NLayout has-sider style="height: 400px;">
      <NLayoutContent>
        <div 
          ref="chart4Ref" 
          style="width: 100%; height: 400px; background: white; padding: 0px; border-radius: 8px;"
        ></div>
      </NLayoutContent>
    </NLayout>

    <NSpace vertical :size="12">
      <n-card embedded size="medium" hoverable>
        <NSpace justify="space-between" align="center" style="width: 100%">
          <NSpace>
            <TheIcon icon="ion:stats-chart" color="#2d8cf0" :size="24" />
            <NText depth="5" style="font-size: 17px">各国家灾害伤亡人数排行</NText>
          </NSpace>
          <NSpace :size="12">
            <NTag type="info" size="medium">前10名</NTag>
          </NSpace>
        </NSpace>
      </n-card>
    </NSpace>

    <NLayout has-sider style="height: 400px;">
      <NLayoutContent>
        <div 
          ref="chart3Ref" 
          style="width: 100%; height: 400px; background: white; padding: 0px; border-radius: 8px;"
        ></div>
      </NLayoutContent>
    </NLayout>

    <NSpace vertical :size="12">
      <n-card embedded size="medium" hoverable>
        <NSpace justify="space-between" align="center" style="width: 100%">
          <NSpace>
            <TheIcon icon="ion:stats-chart" color="#2d8cf0" :size="24" />
            <NText depth="5" style="font-size: 17px">各国家灾害直接经济损失排行</NText>
          </NSpace>
          <NSpace :size="12">
            <NTag type="info" size="medium">前10名</NTag>
          </NSpace>
        </NSpace>
      </n-card>
    </NSpace>

    <NLayout has-sider style="height: 400px;">
      <NLayoutContent>
        <div 
          ref="chart2Ref" 
          style="width: 100%; height: 400px; background: white; padding: 0px; border-radius: 8px;"
        ></div>
      </NLayoutContent>
    </NLayout>
    
  </CommonPage>
</template>

<style>

#map-container {
  background: #f0f2f5;
}

.legend {
  background: rgba(255, 255, 255, 0.9);
  padding: 10px;
  border-radius: 5px;
  box-shadow: 0 1px 5px rgba(0,0,0,0.2);
}

.legend h4 {
  margin: 0 0 10px;
  font-size: 14px;
}

.legend-item {
  display: flex;
  align-items: center;
  margin: 5px 0;
  font-size: 12px;
}

.legend-item i {
  display: inline-block;
  width: 18px;
  height: 18px;
  margin-right: 8px;
  border-radius: 3px;
}
</style>