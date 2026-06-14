<script setup>
import { h, onMounted, ref, resolveDirective, withDirectives } from 'vue'
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
  NPopconfirm,
  NLayout,
  NLayoutSider,
  NLayoutContent,
  NTreeSelect,
  NLayoutFooter
} from 'naive-ui'
import CommonPage from '@/components/page/CommonPage.vue'
import QueryBarItem from '@/components/query-bar/QueryBarItem.vue'
import CrudModal from '@/components/table/CrudModal.vue'
import CrudTable from '@/components/table/CrudTable.vue'
import TheIcon from '@/components/icon/TheIcon.vue'
import { useRoute } from 'vue-router'
import { renderIcon } from '@/utils'
import { useCRUD } from '@/composables'
import api from '@/api'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'

const $table = ref(null)
const queryItems = ref({})
const vPermission = resolveDirective('permission')
const detailVisible = ref(false)
const detailData = ref({})


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

const countryOptions = [
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
]

// 时间范围选项
const timeOptions = [
  { label: '近一个月', value: 'month' },
  { label: '近三个月', value: '3month' },
  { label: '近六个月', value: '6month' },
  { label: '近一年', value: 'year' }
]
const timeRangeType = ref('month')
const customDateRange = ref(null)

// 计算时间范围
const calcDateRange = (type) => {
  const end = new Date()
  const start = new Date()
  switch (type) {
    case 'month':
      start.setMonth(end.getMonth() - 1)
      break
    case '3month':
      start.setMonth(end.getMonth() - 3)
      break
    case '6month':
      start.setMonth(end.getMonth() - 6)
      break
    case 'year':
      start.setFullYear(end.getFullYear() - 1)
      break
  }
  return [start, end]
}

// 处理时间范围变化
const handleTimeRangeChange = (type) => {
  if (type === 'custom') return
  const [start, end] = calcDateRange(type)
  queryItems.value.start_time = start.toISOString().split('T')[0]
  queryItems.value.end_time = end.toISOString().split('T')[0]
  customDateRange.value = null
}

// 处理自定义日期
const handleCustomDate = (value) => {
  if (!value) return
  timeRangeType.value = 'custom'
  queryItems.value.start_time = new Date(value[0]).toISOString().split('T')[0]
  queryItems.value.end_time = new Date(value[1]).toISOString().split('T')[0]
}

// 查看详情
const handleViewDetail = async (row) => {
    // 调用获取详情的API接口
    const res = await api.getDisaster({ dis_no: row.dis_no }) 
    const human = await api.getHumanImpact({ dis_no: row.dis_no})
    const economic = await api.getEconomicLoss({ dis_no: row.dis_no})
    const mergedData = Object.assign({}, res.data, human.data, economic.data);
    detailData.value = mergedData
    detailVisible.value = true
}

// 表格列配置
const columns = [
  {
    title: '灾害编号',
    key: 'dis_no',
    align: 'center',
    width: 'auto',
    ellipsis: { tooltip: true },
  },
  {
    title: '类型',
    key: 'disaster_type',
    width: 'auto',
    align: 'center',
    ellipsis: { tooltip: true },
  },
  {
    title: '国家',
    key: 'country',
    align: 'center',
    width: 'auto',
    ellipsis: { tooltip: true },
  },
  {
    title: '开始时间',
    key: 'start_date',
    width: 'auto',
    align: 'center',
    ellipsis: { tooltip: true },
  },
  {
    title: '结束时间',
    key: 'end_date',
    width: 'auto',
    align: 'center',
    ellipsis: { tooltip: true },
  },
  {
    title: '操作',
    key: 'actions',
    width: 'auto',
    align: 'center',
    fixed: 'right',
    render(row) {
      return [
        withDirectives(
          h(
            NButton,
            {
              size: 'small',
              type: 'primary',
              style: 'margin-right: 8px;',
              onClick: () => {
                handleViewDetail(row)
              },
            },
            {
              default: () => '查看详情',
              icon: renderIcon('material-symbols:visibility-outline', { size: 16 }),
            }
          ),
          [[vPermission, 'get:/api/v1/disaster/get']]
        ),
      ]
    },
  },
]

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

// 地图实例
const map = shallowRef(null)
const markers = ref([])

// 图例实例
const legend = shallowRef(null)

// 初始化图例
const initLegend = () => {
  // 创建图例容器
  legend.value = L.control({ position: 'bottomright' })

  legend.value.onAdd = () => {
    const div = L.DomUtil.create('div', 'disaster-legend')
    // 初始空内容，由updateLegend填充
    return div
  }

  legend.value.addTo(map.value)
}

// 更新图例内容
const updateLegend = () => {
  const legendContainer = legend.value?.getContainer()
  if (!legendContainer) return

  // 生成图例项
  const items = Object.entries(disasterColors)
    .map(([type, color]) => `
      <div class="legend-item">
        <i style="background:${color}"></i>
        <span>${type}</span>
      </div>
    `).join('')

  legendContainer.innerHTML = `
    <div class="legend-header">灾害类型</div>
    <div class="legend-scroll">${items}</div>
  `
}

// 初始化地图
const initMap = () => {
  nextTick(() => {
    if (!map.value) {
      map.value = L.map('map-container', {
        attributionControl: false
      }).setView([30, 120], 4)
      
      L.tileLayer('https://webrd0{s}.is.autonavi.com/appmaptile?lang=zh_cn&size=1&scale=1&style=8&x={x}&y={y}&z={z}', {
        subdomains: ['1', '2', '3', '4'],
        attribution: '高德地图'
      }).addTo(map.value)
      initLegend()
    }
  })
}

// 更新地图标记
const updateMapMarkers = async () => {
  // 清除旧标记
  markers.value.forEach(marker => marker.remove())
  markers.value = []

  // 获取当前页数据
  const currentPageData = await api.getDisasterList({
        ...queryItems.value,
        page: $table.value?.pagination?.page,
        page_size: $table.value?.pagination?.page_size
  }).then(res => res.data)

  // 添加新标记
  currentPageData?.forEach(item => {
    if (!item.latitude || !item.longitude) return
    
    const marker = L.circleMarker([item.latitude, item.longitude], {
      radius: 6,
      fillColor: disasterColors[item.disaster_type],
      color: '#333',
      weight: 1,
      opacity: 0,
      fillOpacity: 0.8
    }).on('click', () => handleViewDetail(item))

    marker.addTo(map.value)
    markers.value.push(marker)
  })

  // 更新图例
  nextTick(() => updateLegend())
}

// 监听表格搜索/分页变化
watch(() => $table.value?.pagination, () => {
  updateMapMarkers()
}, { deep: true })

// 初始化默认时间范围
onMounted(() => {
  handleTimeRangeChange('month')
  $table.value?.handleSearch()
  initMap()
  updateMapMarkers()
})

</script>

<template>
  <CommonPage>
    <!-- 新增地图容器 -->
    <div id="map-container" class="h-500px mb-4 border rounded"></div>

    <CrudTable
      ref="$table"
      v-model:query-items="queryItems"
      :columns="columns"
      :get-data="api.getDisasterList"
    >
      <template #queryBar>
        <QueryBarItem label="类型" :label-width="40">
          <NSelect
            v-model:value="queryItems.type"
            clearable
            placeholder="请选择"
            style="width: 120px"
            :options=disasterOptions
          />
        </QueryBarItem>
        
        <QueryBarItem label="国家" :label-width="40">
          <NSelect
            v-model:value="queryItems.country"
            clearable
            placeholder="请选择"
            style="width: 120px"
            :options=countryOptions
          />
        </QueryBarItem>

        <QueryBarItem label="时间范围" :label-width="80">
          <NSpace>
            <NRadioGroup
              v-model:value="timeRangeType"
              @update:value="handleTimeRangeChange"
            >
              <NSpace>
                <NRadioButton
                  v-for="opt in timeOptions"
                  :key="opt.value"
                  :value="opt.value"
                  :label="opt.label"
                />
                <NRadioButton value="custom" label="时间选择" />
              </NSpace>
            </NRadioGroup>
            
            <NDatePicker
              v-if="timeRangeType === 'custom'"
              v-model:value="customDateRange"
              type="daterange"
              clearable
              @update:value="handleCustomDate"
            />
          </NSpace>
        </QueryBarItem>
      </template>
    </CrudTable>

    <!-- 查看详情 弹窗 -->
    <CrudModal
      v-model:visible="detailVisible"
      title="灾害详情"
      :show-footer="false"
      bordered
      width="1200px"
    >
      <NLayout embedded class="h-[550px]" :native-scrollbar="false">
        <NLayoutContent>
          <NSpace vertical class="p-4" :size="24">
            <!-- 基础信息卡片 -->
            <NCard
              title="基础信息"
              embedded
              hoverable
              :bordered="true"
              size="small"
              :segmented="{ content: true }"
            >
              <template #header-extra>
                <TheIcon icon="mdi:information-outline" class="mr-1" />
              </template>
              <NGrid :cols="24" :x-gap="24">
                <NFormItemGi :span="12" label="灾害编号">
                  <NText strong type="primary">{{ detailData.dis_no }}</NText>
                </NFormItemGi>
                
                <NFormItemGi :span="12" label="灾害类型">
                  <NTag type="info" round bordered>
                    {{ detailData.disaster_type || '未知类型' }}
                  </NTag>
                </NFormItemGi>

                <NFormItemGi :span="12" label="灾害强度">
                  <NText strong type="primary" v-if="detailData.magnitude">
                        {{ detailData.magnitude }} {{ detailData.magnitude_scale || ""}}
                  </NText>
                  <NText strong type="error" v-else>未知</NText>
                </NFormItemGi>

                <NFormItemGi :span="12" label="灾害起因">
                  <NText strong type="primary" v-if="detailData.origin">
                        {{ detailData.origin }}
                  </NText>
                  <NText strong type="error" v-else>未知</NText>
                </NFormItemGi>

                <NFormItemGi :span="12" label="开始时间">
                  <NText strong type="primary">
                    {{ detailData.start_date ? detailData.start_date : 'Unknown' }}
                  </NText>
                </NFormItemGi>

                <NFormItemGi :span="12" label="结束时间">
                  <NText strong type="primary">
                    {{ detailData.end_date ? detailData.end_date : 'Unknown' }}
                  </NText>
                </NFormItemGi>
              </NGrid>
            </NCard>

            <!-- 地理信息卡片 -->
            <NCard
              title="地理信息"
              embedded
              size="small"
              :segmented="{ content: 'true' }"
            >
              <template #header-extra>
                <TheIcon icon="mdi:earth" class="mr-1" />
              </template>

              <NGrid :cols="24" :x-gap="24">
                <NFormItemGi :span="12" label="国家">
                  <NText strong type="primary">{{ detailData.country }}</NText>
                </NFormItemGi>

                <NFormItemGi :span="12" label="区域">
                  <NText strong type="primary">{{ detailData.region }}</NText>
                </NFormItemGi>

                <NFormItemGi :span="12" label="子区域">
                  <NText strong type="primary">{{ detailData.subregion }}</NText>
                </NFormItemGi>

                <NFormItemGi :span="12" label="流域">
                  <NText strong type="primary" v-if="detailData.river_basin">
                        {{ detailData.river_basin }}
                  </NText>
                  <NText strong type="error" v-else>未知</NText>
                </NFormItemGi>

                <NFormItemGi :span="24" label="详细位置">
                  <NText strong type="primary" v-if="detailData.location">
                        {{ detailData.location }}
                  </NText>
                  <NText strong type="error" v-else>未知</NText>
                </NFormItemGi>

              </NGrid>

              <NSpace :size="16" v-if="detailData.longitude && detailData.latitude">
                <NStatistic label="经度" class="mr-100">
                  <NNumberAnimation
                    :from="0"
                    :to="detailData.longitude"
                    precision="3"
                  />
                </NStatistic>

                <NStatistic label="纬度">
                  <NNumberAnimation
                    :from="0"
                    :to="detailData.latitude"
                    precision="3"
                  />
                </NStatistic>
              </NSpace>
            </NCard>

            <!-- 灾害损失卡片 -->
            <NCard
              v-if="detailData.reconstruction_adjusted || detailData.insured_adjusted || detailData.total_adjusted"
              title="灾害损失"
              embedded
              hoverable
              :bordered="true"
              size="small"
              :segmented="{ content: true }"
            >
              <template #header-extra>
                <TheIcon icon="mdi:chart-box-outline" class="mr-1" />
              </template>
              <NGrid :cols="24" :x-gap="24">
                <NGi :span="12">
                  <NForm label-placement="left" label-align="right">
                    <NFormItem label="灾后重建费用（千美元）:" label-style="font-weight: 500;">
                      <NText strong type="primary" v-if="detailData.reconstruction_adjusted">
                        {{ detailData.reconstruction_adjusted }}
                      </NText>
                      <NText strong type="error" v-else>未知</NText>
                    </NFormItem>

                    <NFormItem label="灾后保险损失（千美元）:">
                      <NText strong type="primary" v-if="detailData.insured_adjusted">
                        {{ detailData.insured_adjusted }}
                      </NText>
                      <NText strong type="error" v-else>未知</NText>
                    </NFormItem>

                    <NFormItem label="灾后总损失（千美元）:">
                      <NText strong type="primary" v-if="detailData.total_adjusted">
                        {{ detailData.total_adjusted }}
                      </NText>
                      <NText strong type="error" v-else>未知</NText>
                    </NFormItem>
                  </NForm>
                </NGi>

                <NGi :span="12">
                  <NSpace>
                    <NStatistic label="灾后重建费用" class="mr-50" v-if="detailData.reconstruction_adjusted">
                      <NNumberAnimation
                        :from="0"
                        :to="detailData.reconstruction_adjusted"
                        precision="2"
                      />
                    </NStatistic>

                    <NStatistic label="灾后保险损失"  class="mr-50" v-if="detailData.insured_adjusted">
                      <NNumberAnimation
                        :from="0"
                        :to="detailData.insured_adjusted"
                        precision="2"
                      />
                    </NStatistic>

                    <NStatistic label="灾后总损失" v-if="detailData.total_adjusted">
                      <NNumberAnimation
                        :from="0"
                        :to="detailData.total_adjusted"
                        precision="2"
                      />
                    </NStatistic>
                  </NSpace>
                </NGi>

              </NGrid>
            </NCard>

            <!-- 人员伤亡信息 -->
            <NCard
              v-if="detailData.total_deaths || detailData.num_injured || detailData.num_homeless || detailData.total_affected"
              title="人员影响"
              embedded
              size="small"
              :segmented="{ content: true }"
            >
              <template #header-extra>
                <TheIcon icon="mdi:alert-octagon" class="text-red-500 mr-1" />
              </template>
              <NSpace>
                <NStatistic label="死亡人数" class="mr-100" v-if="detailData.total_deaths">
                  <NNumberAnimation
                    :from="0"
                    :to="detailData.total_deaths"
                  />
                </NStatistic>

                <NStatistic label="受伤人数" class="mr-100" v-if="detailData.num_injured">
                  <NNumberAnimation
                    :from="0"
                    :to="detailData.num_injured"
                  />
                </NStatistic>

                <NStatistic label="无家可归人数" class="mr-100" v-if="detailData.num_homeless">
                  <NNumberAnimation
                    :from="0"
                    :to="detailData.num_homeless"
                  />
                </NStatistic>

                <NStatistic label="总影响人数" v-if="detailData.total_affected">
                  <NNumberAnimation
                    :from="0"
                    :to="detailData.total_affected"
                  />
                </NStatistic>
              </NSpace>
            </NCard>
          </NSpace>
        </NLayoutContent>
      </NLayout>
    </CrudModal>
  </CommonPage>
</template>
