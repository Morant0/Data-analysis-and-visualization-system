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

defineOptions({ name: '国家尺度' })

// 新增状态管理
const activeTab = ref() // frequency | impact | loss
const selectedCountry = ref('China')
const countryOptions = ref([
  { label: '吉布提', value: 'Djibouti' },
  { label: '苏丹', value: 'Sudan' },
  { label: '索马里', value: 'Somalia' },
  { label: '安哥拉', value: 'Angola' },
  { label: '孟加拉国', value: 'Bangladesh' },
  { label: '危地马拉', value: 'Guatemala' },
  { label: '伊朗', value: 'Iran (Islamic Republic of)' },
  { label: '莫桑比克', value: 'Mozambique' },
  { label: '南非', value: 'South Africa' },
  { label: '巴西', value: 'Brazil' },
  { label: '印度', value: 'India' },
  { label: '美国', value: 'United States of America' },
  { label: '罗马尼亚', value: 'Romania' },
  { label: '保加利亚', value: 'Bulgaria' },
  { label: '中国', value: 'China' },
  { label: '留尼汪', value: 'Réunion' },
  { label: '菲律宾', value: 'Philippines' },
  { label: '博茨瓦纳', value: 'Botswana' },
  { label: '蒙古', value: 'Mongolia' },
  { label: '俄罗斯', value: 'Russian Federation' },
  { label: '刚果', value: 'Congo' },
  { label: '阿富汗', value: 'Afghanistan' },
  { label: '埃塞俄比亚', value: 'Ethiopia' },
  { label: '坦桑尼亚', value: 'United Republic of Tanzania' },
  { label: '莱索托', value: 'Lesotho' },
  { label: '肯尼亚', value: 'Kenya' },
  { label: '波斯尼亚和黑塞哥维那', value: 'Bosnia and Herzegovina' },
  { label: '冰岛', value: 'Iceland' },
  { label: '纳米比亚', value: 'Namibia' },
  { label: '哥伦比亚', value: 'Colombia' },
  { label: '印度尼西亚', value: 'Indonesia' },
  { label: '津巴布韦', value: 'Zimbabwe' },
  { label: '埃及', value: 'Egypt' },
  { label: '以色列', value: 'Israel' },
  { label: '约旦', value: 'Jordan' },
  { label: '斯威士兰', value: 'Eswatini' },
  { label: '澳大利亚', value: 'Australia' },
  { label: '赞比亚', value: 'Zambia' },
  { label: '马达加斯加', value: 'Madagascar' },
  { label: '尼日利亚', value: 'Nigeria' },
  { label: '阿根廷', value: 'Argentina' },
  { label: '马拉维', value: 'Malawi' },
  { label: '巴基斯坦', value: 'Pakistan' },
  { label: '刚果民主共和国', value: 'Democratic Republic of the Congo' },
  { label: '秘鲁', value: 'Peru' },
  { label: '玻利维亚', value: 'Bolivia (Plurinational State of)' },
  { label: '乍得', value: 'Chad' },
  { label: '奥地利', value: 'Austria' },
  { label: '尼日尔', value: 'Niger' },
  { label: '马来西亚', value: 'Malaysia' },
  { label: '喀麦隆', value: 'Cameroon' },
  { label: '捷克', value: 'Czechia' },
  { label: '日本', value: 'Japan' },
  { label: '中非共和国', value: 'Central African Republic' },
  { label: '贝宁', value: 'Benin' },
  { label: '土耳其', value: 'Türkiye' },
  { label: '匈牙利', value: 'Hungary' },
  { label: '韩国', value: 'Republic of Korea' },
  { label: '塞尔维亚和黑山', value: 'Serbia Montenegro' },
  { label: '厄瓜多尔', value: 'Ecuador' },
  { label: '沙特阿拉伯', value: 'Saudi Arabia' },
  { label: '洪都拉斯', value: 'Honduras' },
  { label: '法属圭亚那', value: 'French Guiana' },
  { label: '哈萨克斯坦', value: 'Kazakhstan' },
  { label: '布隆迪', value: 'Burundi' },
  { label: '密克罗尼西亚', value: 'Micronesia (Federated States of)' },
  { label: '英国', value: 'United Kingdom of Great Britain and Northern Ireland' },
  { label: '白俄罗斯', value: 'Belarus' },
  { label: '乌拉圭', value: 'Uruguay' },
  { label: '墨西哥', value: 'Mexico' },
  { label: '希腊', value: 'Greece' },
  { label: '智利', value: 'Chile' },
  { label: '利比里亚', value: 'Liberia' },
  { label: '克罗地亚', value: 'Croatia' },
  { label: '塞浦路斯', value: 'Cyprus' },
  { label: '乌克兰', value: 'Ukraine' },
  { label: '尼加拉瓜', value: 'Nicaragua' },
  { label: '法国', value: 'France' },
  { label: '西班牙', value: 'Spain' },
  { label: '越南', value: 'Viet Nam' },
  { label: '乌干达', value: 'Uganda' },
  { label: '塞拉利昂', value: 'Sierra Leone' },
  { label: '哥斯达黎加', value: 'Costa Rica' },
  { label: '老挝', value: "Lao People's Democratic Republic" },
  { label: '泰国', value: 'Thailand' },
  { label: '加拿大', value: 'Canada' },
  { label: '柬埔寨', value: 'Cambodia' },
  { label: '尼泊尔', value: 'Nepal' },
  { label: '不丹', value: 'Bhutan' },
  { label: '巴拉圭', value: 'Paraguay' },
  { label: '摩洛哥', value: 'Morocco' },
  { label: '爱尔兰', value: 'Ireland' },
  { label: '台湾', value: 'Taiwan (Province of China)' },
  { label: '卢旺达', value: 'Rwanda' },
  { label: '斯洛伐克', value: 'Slovakia' },
  { label: '马里', value: 'Mali' },
  { label: '新西兰', value: 'New Zealand' },
  { label: '拉脱维亚', value: 'Latvia' },
  { label: '朝鲜', value: "Democratic People's Republic of Korea" },
  { label: '意大利', value: 'Italy' },
  { label: '萨尔瓦多', value: 'El Salvador' },
  { label: '斯里兰卡', value: 'Sri Lanka' },
  { label: '也门', value: 'Yemen' },
  { label: '巴拿马', value: 'Panama' },
  { label: '北马其顿', value: 'North Macedonia' },
  { label: '伯利兹', value: 'Belize' },
  { label: '委内瑞拉', value: 'Venezuela (Bolivarian Republic of)' },
  { label: '瑞士', value: 'Switzerland' },
  { label: '新加坡', value: 'Singapore' },
  { label: '吉尔吉斯斯坦', value: 'Kyrgyzstan' },
  { label: '挪威', value: 'Norway' },
  { label: '阿尔及利亚', value: 'Algeria' },
  { label: '几内亚', value: 'Guinea' },
  { label: '塔吉克斯坦', value: 'Tajikistan' },
  { label: '巴布亚新几内亚', value: 'Papua New Guinea' },
  { label: '阿塞拜疆', value: 'Azerbaijan' },
  { label: '海地', value: 'Haiti' },
  { label: '摩尔多瓦', value: 'Republic of Moldova' },
  { label: '土库曼斯坦', value: 'Turkmenistan' },
  { label: '波兰', value: 'Poland' },
  { label: '马绍尔群岛', value: 'Marshall Islands' },
  { label: '古巴', value: 'Cuba' },
  { label: '冈比亚', value: 'Gambia' },
  { label: '牙买加', value: 'Jamaica' },
  { label: '乌兹别克斯坦', value: 'Uzbekistan' },
  { label: '亚美尼亚', value: 'Armenia' },
  { label: '格鲁吉亚', value: 'Georgia' },
  { label: '葡萄牙', value: 'Portugal' },
  { label: '布基纳法索', value: 'Burkina Faso' },
  { label: '瓦努阿图', value: 'Vanuatu' },
  { label: '叙利亚', value: 'Syrian Arab Republic' },
  { label: '多哥', value: 'Togo' },
  { label: '加纳', value: 'Ghana' },
  { label: '萨摩亚', value: 'Samoa' },
  { label: '波多黎各', value: 'Puerto Rico' },
  { label: '东帝汶', value: 'Timor-Leste' },
  { label: '圣赫勒拿', value: 'Saint Helena' },
  { label: '德国', value: 'Germany' },
  { label: '科特迪瓦', value: 'Côte d’Ivoire' },
  { label: '毛里塔尼亚', value: 'Mauritania' },
  { label: '多米尼加共和国', value: 'Dominican Republic' },
  { label: '开曼群岛', value: 'Cayman Islands' },
  { label: '加那利群岛', value: 'Canary Islands' },
  { label: '库克群岛', value: 'Cook Islands' },
  { label: '加蓬', value: 'Gabon' },
  { label: '巴哈马', value: 'Bahamas' },
  { label: '汤加', value: 'Tonga' },
  { label: '立陶宛', value: 'Lithuania' },
  { label: '缅甸', value: 'Myanmar' },
  { label: '阿尔巴尼亚', value: 'Albania' },
  { label: '塞内加尔', value: 'Senegal' },
  { label: '毛里求斯', value: 'Mauritius' },
  { label: '比利时', value: 'Belgium' },
  { label: '瑞典', value: 'Sweden' },
  { label: '关岛', value: 'Guam' },
  { label: '塞舌尔', value: 'Seychelles' },
  { label: '巴巴多斯', value: 'Barbados' },
  { label: '格林纳达', value: 'Grenada' },
  { label: '圣文森特和格林纳丁斯', value: 'Saint Vincent and the Grenadines' },
  { label: '荷兰', value: 'Netherlands (Kingdom of the)' },
  { label: '丹麦', value: 'Denmark' },
  { label: '黎巴嫩', value: 'Lebanon' },
  { label: '所罗门群岛', value: 'Solomon Islands' },
  { label: '北马里亚纳群岛', value: 'Northern Mariana Islands' },
  { label: '几内亚比绍', value: 'Guinea-Bissau' },
  { label: '佛得角', value: 'Cabo Verde' },
  { label: '斐济', value: 'Fiji' },
  { label: '突尼斯', value: 'Tunisia' },
  { label: '新喀里多尼亚', value: 'New Caledonia' },
  { label: '阿曼', value: 'Oman' },
  { label: '伊拉克', value: 'Iraq' },
  { label: '美属萨摩亚', value: 'American Samoa' },
  { label: '中国香港', value: 'China, Hong Kong Special Administrative Region' },
  { label: '厄立特里亚', value: 'Eritrea' },
  { label: '卢森堡', value: 'Luxembourg' },
  { label: '斯洛文尼亚', value: 'Slovenia' },
  { label: '百慕大', value: 'Bermuda' },
  { label: '科摩罗', value: 'Comoros' },
  { label: '纽埃', value: 'Niue' },
  { label: '特克斯和凯科斯群岛', value: 'Turks and Caicos Islands' },
  { label: '圣卢西亚', value: 'Saint Lucia' },
  { label: '特立尼达和多巴哥', value: 'Trinidad and Tobago' },
  { label: '美属维尔京群岛', value: 'United States Virgin Islands' },
  { label: '多米尼加', value: 'Dominica' },
  { label: '法属圣马丁', value: 'Saint Martin (French Part)' },
  { label: '马提尼克', value: 'Martinique' },
  { label: '黑山', value: 'Montenegro' },
  { label: '南苏丹', value: 'South Sudan' },
  { label: '基里巴斯', value: 'Kiribati' },
  { label: '安提瓜和巴布达', value: 'Antigua and Barbuda' },
  { label: '圣基茨和尼维斯', value: 'Saint Kitts and Nevis' },
  { label: '巴勒斯坦', value: 'State of Palestine' },
  { label: '法属波利尼西亚', value: 'French Polynesia' },
  { label: '图瓦卢', value: 'Tuvalu' },
  { label: '瓦利斯和富图纳群岛', value: 'Wallis and Futuna Islands' },
  { label: '帕劳', value: 'Palau' },
  { label: '利比亚', value: 'Libya' },
  { label: '中国澳门', value: 'China, Macao Special Administrative Region' },
  { label: '安圭拉', value: 'Anguilla' },
  { label: '圣巴泰勒米岛', value: 'Saint Barthélemy' },
  { label: '法属圣马丁', value: 'Saint Martin (French Part)' },
  { label: '圣马丁岛（荷兰部分）', value: 'Sint Maarten (Dutch part)' },
  { label: '英属维尔京群岛', value: 'British Virgin Islands' },
  { label: '阿拉伯联合酋长国', value: 'United Arab Emirates' },
  { label: '卡塔尔', value: 'Qatar' },
  { label: '科威特', value: 'Kuwait' },
  { label: '马耳他', value: 'Malta' },
  { label: '列支敦士登', value: 'Liechtenstein' },
  { label: '马约特岛', value: 'Mayotte' }
])

const yearOptions = [
  { label: '近10年', value: 10 },
  { label: '近20年', value: 20 },
  { label: '近25年', value: 25 }
]
const selectedYears = ref(10)

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

// 图表容器统一管理
const chartContainers = {
  frequency: { left: ref(null), right: ref(null) },
  impact: { left: ref(null), right: ref(null) },
  loss: { left: ref(null), right: ref(null) }
}

// 图表实例统一管理
let charts = {
  frequency: { left: null, right: null },
  impact: { left: null, right: null },
  loss: { left: null, right: null }
}

// 新增状态管理
const loading = ref(false)
const prevTab = ref(null)


// 获取图表数据（参数化）
async function fetchChartData(type) {
  try {
    const params = { 
      n: selectedYears.value,
      country: selectedCountry.value
    }
    
    const apis = {
      frequency: [api.getYearCount(params), api.getYearCountByType(params)],
      impact: [api.getRecentStats(params), api.getRecentStatsByType(params)],
      loss: [api.getRecentLoss(params), api.getRecentLossByType(params)]
    }
    
    const [res1, res2] = await Promise.all(apis[type])
    initChart(type, res1.data, res2.data)
  } catch (error) {
    console.error('获取图表数据失败:', error)
  }
}

// 修改初始化逻辑
function initChart(type, lineData, pieData) {
  return new Promise((resolve) => {
    nextTick(() => {
      // 确保容器存在
      if (!chartContainers[type].left.value || 
          !chartContainers[type].right.value) {
        return
      }
      
      // 清理可能存在的子元素
      chartContainers[type].left.value.innerHTML = ''
      chartContainers[type].right.value.innerHTML = ''

      // 创建新canvas元素
      const leftCanvas = document.createElement('div')
      const rightCanvas = document.createElement('div')
      leftCanvas.style.width = '100%'
      leftCanvas.style.height = '100%'
      rightCanvas.style.width = '100%'
      rightCanvas.style.height = '100%'

      chartContainers[type].left.value.appendChild(leftCanvas)
      chartContainers[type].right.value.appendChild(rightCanvas)

      // 初始化实例
      charts[type].left = echarts.init(leftCanvas)
      charts[type].right = echarts.init(rightCanvas)

      // 生成配置
      const options = generateChartOptions(type, lineData, pieData)
      charts[type].left.setOption(options.left)
      charts[type].right.setOption(options.right)
      
      resolve()
    })
  })
}

// 图表配置生成器
function generateChartOptions(type, lineData, pieData) {
  const optionsMap = {
    frequency: {
      left: {
        tooltip: { trigger: 'axis' },
        xAxis: {
          type: 'category',
          data: lineData.map(d => d.start_year),
          name: '年份'
        },
        yAxis: { type: 'value', name: '总频次(次)' },
        series: [
          {
            name: '灾害次数',
            type: 'bar',
            data: lineData.map(d => d.count),
            itemStyle: { color: '#5470C6' }
          }
        ]
      },
      right: {
        tooltip: { trigger: 'item',
        formatter: ({ seriesName, name, value, percent }) => `
            ${name}<br/>
            ${seriesName}: ${value.toLocaleString()}次<br/>
            占比: ${percent}%
          `
        },
        legend: {
          orient: 'horizontal',
          bottom: 50,
          itemGap: 8,
          right: 50,
          textStyle: {
            color: '#666',
          }
        },
        series: [{
          name: '灾害次数',
          type: 'pie',
          radius: ['35%', '60%'],
          center: ['50%', '30%'],
          data: pieData.map(d => ({
            name: d.disaster_type,
            value: d.total_count,
            itemStyle: {
              color: disasterColors[d.disaster_type]
            }
          })),
          label: {
            show: false
          },
        }]
      }
    },
    impact: {
      left: {
        tooltip: { trigger: 'axis' },
        legend: { data: ['影响人数', '伤亡人数'] },
        xAxis: {
          type: 'category',
          data: lineData.map(d => d.start_year),
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
            data: lineData.map(d => d.total_affected_sum),
            itemStyle: { color: '#FF0000' }
          },
          {
            name: '伤亡人数',
            type: 'line',
            yAxisIndex: 1,
            data: lineData.map(d => d.death_injured_sum),
            smooth: true,
            itemStyle: { color: '#B22222' }
          }
        ]
      },
      right: {
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
          bottom: 50,
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
            center: ['50%', '30%'],
            label: { show: false }, // 关闭标签
            data: pieData.map(d => ({
              name: d.disaster_type,
              value: d.total_affected_sum,
              itemStyle: {
                color: disasterColors[d.disaster_type]
              }
            })),
          },
          { // 外圈-伤亡人数
            type: 'pie',
            name: '伤亡人数',
            radius: ['45%', '60%'],
            center: ['50%', '30%'],
            label: { show: false }, // 关闭标签
            data: pieData.map(d => ({
              name: d.disaster_type,
              value: d.death_injured_sum,
              itemStyle: {
                color: disasterColors[d.disaster_type]
              }
            })),
          }
        ]
      }
    },
    loss: {
      left: {
        tooltip: { trigger: 'axis' },
        xAxis: {
          type: 'category',
          data: lineData.map(d => d.start_year),
          name: '年份'
        },
        yAxis: { type: 'value', name: '直接经济损失(千美元)' },
        series: [
          {
            name: '直接经济损失',
            type: 'bar',
            data: lineData.map(d => d.total_loss),
            itemStyle: { color: '#7FFF00' }
          },
        ]
      },
      right: {
        tooltip: { trigger: 'item',
        formatter: ({ seriesName, name, value, percent }) => `
            ${name}<br/>
            ${seriesName}: ${value.toLocaleString()}美元<br/>
            占比: ${percent}%
          `
        },
        legend: {
          orient: 'horizontal',
          bottom: 50,
          itemGap: 8,
          right: 50,
          textStyle: {
            color: '#666',
          }
        },
        series: [{
          type: 'pie',
          name: '直接经济损失',
          radius: ['35%', '60%'],
          center: ['50%', '30%'],
          data: pieData.map(d => ({
            name: d.disaster_type,
            value: d.total_loss,
            itemStyle: {
              color: disasterColors[d.disaster_type]
            }
          })),
          label: {
            show: false
          },
        }]
      }
    }
  }
  console.log({
    left: optionsMap[type].left,
    right: optionsMap[type].right
  })
  // 合并基础配置
  return {
    left: optionsMap[type].left,
    right: optionsMap[type].right
  }
}

// 专用销毁方法
function destroyChart(type) {
  const chartInstances = charts[type]
  if (chartInstances) {
    chartInstances.left?.dispose()
    chartInstances.right?.dispose()
    charts[type] = { left: null, right: null }
  }
  
  // 清除残留DOM（关键！）
  const containers = chartContainers[type]
  containers.left.value?.removeChild(containers.left.value.firstChild)
  containers.right.value?.removeChild(containers.right.value.firstChild)
}

// 优化后的切换逻辑
async function changeTab(tab) {
  if (activeTab.value === tab) return
  
  // 1. 立即销毁旧图表
  if (prevTab.value) {
    destroyChart(prevTab.value)
  }
  
  // 2. 显示加载状态
  loading.value = true
  activeTab.value = tab
  
  try {
    // 3. 等待DOM更新完成
    await nextTick()
    
    // 4. 初始化新图表
    await fetchChartData(tab)
  } finally {
    loading.value = false
    prevTab.value = tab
  }
}

// 新增散点图容器和实例
chartContainers.scatter = { 
  loss: ref(null),    // 经济损失散点图
  impact: ref(null)   // 新增影响人数散点图
}
let scatterCharts = {
  loss: null,
  impact: null
}

// 修改后的数据获取方法
async function fetchScatterData() {
  try {
    const params = { n: selectedYears.value }
    const [resCount, resLoss, resCasualties] = await Promise.all([
      api.getCountryDisasterCount(params),
      api.getCountryLoss(params),
      api.getCountryCasualties(params)
    ])
    
    // 处理经济损失数据
    const lossData = processScatterData(resCount.data, resLoss.data, 'total_loss')
    initScatterChart('loss', lossData, '直接经济损失（千美元）', value => `$${value.toLocaleString()}`)
    
    // 处理影响/伤亡数据
    const impactData = processScatterData(resCount.data, resCasualties.data, 'total_casualties')
    initScatterChart('impact', impactData, '影响/伤亡人数（人）', value => value.toLocaleString())
    
  } catch (error) {
    console.error('获取散点图数据失败:', error)
  }
}


// 通用数据处理方法
function processScatterData(countData, targetData, dataKey) {
  const countryMap = new Map()
  countData.forEach(item => {
    countryMap.set(item.country, { count: item.count })
  })
  targetData.forEach(item => {
    const country = countryMap.get(item.country) || { count: 0 }
    country[dataKey] = item[dataKey] || 0
    countryMap.set(item.country, country)
  })
  return Array.from(countryMap).map(([country, data]) => ({
    name: country,
    value: [data.count, data[dataKey]],
    itemStyle: {
      color: country === selectedCountry.value ? '#ff0000' : '#5470C6'
    }
  }))
}

// 通用图表初始化方法
function initScatterChart(type, data, yAxisName, formatter) {
  nextTick(() => {
    const container = chartContainers.scatter[type].value
    if (!container) return
    
    // 清理容器
    container.innerHTML = ''
    const canvas = document.createElement('div')
    canvas.style.width = '100%'
    canvas.style.height = '100%'
    container.appendChild(canvas)
    
    // 初始化图表
    scatterCharts[type] = echarts.init(canvas)
    scatterCharts[type].setOption({
      tooltip: {
        trigger: 'item',
        formatter: params => `
          <b>${params.name}</b><br/>
          总频次: ${params.value[0]}次<br/>
          ${yAxisName}: ${formatter(params.value[1])}
        `
      },
      xAxis: {
        name: '灾害总次数',
        nameLocation: 'center',
        nameGap: 25
      },
      yAxis: {
        name: yAxisName,
        nameGap: 30,
        axisLabel: { formatter }
      },
      series: [{
        type: 'scatter',
        data: data,
        symbolSize: 16,
        emphasis: {
          itemStyle: {
            shadowBlur: 10,
            shadowColor: 'rgba(0, 0, 0, 0.5)'
          }
        }
      }]
    })
  })
}

// 监听筛选条件变化
watch([selectedYears, selectedCountry], () => {
  if (activeTab.value) 
    fetchChartData(activeTab.value)
  fetchScatterData() // 新增散点图数据更新
})

onMounted(() => {
  changeTab('frequency') // 默认加载第一个视图
  fetchScatterData() // 初始化时加载散点图
})
</script>


<template>
    <CommonPage show-footer title="国家尺度">
      <!-- 统计指标卡 -->
      <n-card embedded style="margin-bottom: 20px" v-if="activeTab">
        <NSpace justify="space-around" size="small">
          <NStatistic label="当前国家" :value="selectedCountry" />
          <NStatistic label="时间范围" :value="`近${selectedYears}年`" />
          <NStatistic 
            label="数据更新时间"
            :value="new Date().toLocaleDateString()"
          />
        </NSpace>
      </n-card>

      <template #action>
        <NSpace>
          <NSelect
            v-model:value="selectedCountry"
            :options="countryOptions"
            style="width: 180px"
          />
          <NSelect
            v-model:value="selectedYears"
            :options="yearOptions"
            style="width: 150px"
          />
        </NSpace>
      </template>

      <NSpace>
        <NButtonGroup>
          <NButton 
            :type="activeTab === 'frequency' ? 'primary' : 'default'"
            @click="changeTab('frequency')"
          >总频次</NButton>
          <NButton
            :type="activeTab === 'impact' ? 'primary' : 'default'"
            @click="changeTab('impact')"
          >影响人数/伤亡人数</NButton>
          <NButton
            :type="activeTab === 'loss' ? 'primary' : 'default'"
            @click="changeTab('loss')"
          >直接经济损失</NButton>
        </NButtonGroup>
      </NSpace>

      <!-- 动态图表容器 -->
      <n-spin :show="loading" description="正在切换视图...">
        <NLayout has-sider style="height: 300px; margin-top: 20px" v-if="activeTab">
          <NLayoutContent content-style="padding: 0 10px 0 0">
            <div 
              :ref="el => chartContainers[activeTab].left.value = el"
              style="width: 100%; height: 300px; background: white; border-radius: 8px;"
            ></div>
          </NLayoutContent>
          <NLayoutSider
            content-style="padding: 0 0 0 10px"
            :width="600"
            collapse-mode="transform"
          >
            <div
              :ref="el => chartContainers[activeTab].right.value = el"
              style="width: 100%; height: 300px; background: white; border-radius: 8px;"
            ></div>
          </NLayoutSider>
        </NLayout>
      </n-spin>

      <NSpace vertical :size="12" style="margin-bottom: 20px">
        <n-card embedded size="medium" hoverable>
          <NSpace justify="space-between" align="center" style="width: 100%">
            <NSpace>
              <TheIcon icon="ion:business" color="#2d8cf0" :size="24" />
              <NText depth="5" style="font-size: 17px">总频次/直接经济损失</NText>
            </NSpace>
            <NSpace :size="12">
              <NTag type="info" round size="medium">当前选择国家：{{ selectedCountry }}</NTag>
              <NTag type="success" round size="medium">时间范围：近{{ selectedYears }}年</NTag>
            </NSpace>
          </NSpace>
        </n-card>
      </NSpace>

      <!-- 总频次/直接经济损失 -->
      <NLayout has-sider style="height: 400px; margin-top: 20px">
        <NLayoutContent>
          <div 
            :ref="el => chartContainers.scatter.loss.value = el"
            style="width: 100%; height: 400px; background: white; border-radius: 8px; padding: 15px;"
          ></div>
        </NLayoutContent>
      </NLayout>

      <NSpace vertical :size="12" style="margin-bottom: 20px">
        <n-card embedded size="medium" hoverable>
          <NSpace justify="space-between" align="center" style="width: 100%">
            <NSpace>
              <TheIcon icon="ion:business" color="#2d8cf0" :size="24" />
              <NText depth="5" style="font-size: 17px">总频次/影响伤亡人数</NText>
            </NSpace>
            <NSpace :size="12">
              <NTag type="info" round size="medium">当前选择国家：{{ selectedCountry }}</NTag>
              <NTag type="success" round size="medium">时间范围：近{{ selectedYears }}年</NTag>
            </NSpace>
          </NSpace>
        </n-card>
      </NSpace>

      <NLayout has-sider style="height: 400px; margin-top: 20px">
        <NLayoutContent>
          <div 
            :ref="el => chartContainers.scatter.impact.value = el"
            style="width: 100%; height: 400px; background: white; border-radius: 8px; padding: 15px;"
          ></div>
        </NLayoutContent>
      </NLayout>
    </CommonPage>
</template>