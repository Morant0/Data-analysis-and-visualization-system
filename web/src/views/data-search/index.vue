<script setup>
// 逻辑代码
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
// import { loginTypeMap, loginTypeOptions } from '@/constant/data'
import api from '@/api'

import L from 'leaflet'
import 'leaflet/dist/leaflet.css'


defineOptions({ name: '灾害数据检索' })

const $table = ref(null)
const queryItems = ref({})
const vPermission = resolveDirective('permission')

// 时间
const datetimeRange = ref(null) // 初始设为null
queryItems.value.start_time = null
queryItems.value.end_time = null

function formatTimestamp(timestamp) {
  const date = new Date(timestamp)

  const pad = (num) => num.toString().padStart(2, '0')

  const year = date.getFullYear()
  const month = pad(date.getMonth() + 1) // 月份从0开始，所以需要+1
  const day = pad(date.getDate())

  return `${year}-${month}-${day}`
}   

const handleDateRangeChange = (value) => {
  if (value == null) {
    queryItems.value.start_time = null
    queryItems.value.end_time = null
  } else {
    queryItems.value.start_time = formatTimestamp(value[0])
    queryItems.value.end_time = formatTimestamp(value[1])
  }
}

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

// 新增详情数据引用
const detailVisible = ref(false)
const detailData = ref({})

const handleViewDetail = async (row) => {
    // 调用获取详情的API接口
    const res = await api.getDisaster({ dis_no: row.dis_no }) 
    const human = await api.getHumanImpact({ dis_no: row.dis_no})
    const economic = await api.getEconomicLoss({ dis_no: row.dis_no})
    const mergedData = Object.assign({}, res.data, human.data, economic.data);
    detailData.value = mergedData
    detailVisible.value = true
}

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

// 在setup中获取route实例
const route = useRoute()

onMounted(() => {
  // 从路由参数获取keyword
  const keyword = route.query.keyword
  if (keyword) {
    // 根据API要求设置查询字段（假设使用type字段）
    queryItems.value.keyword = keyword
    // 手动触发搜索
    $table.value?.handleSearch()
    queryItems.value.keyword = ''
  }
  else
    $table.value?.handleSearch()
  initMap()
  updateMapMarkers()
})

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
</script>

<template>
  <CommonPage show-footer title="数据检索">
    <!-- 新增地图容器 -->
    <div id="map-container" class="h-500px mb-4 border rounded"></div>

    <!-- 页面内容 -->
    <CrudTable
      ref="$table"
      v-model:query-items="queryItems"
      :columns="columns"
      :get-data="api.getDisasterList"
      @search="updateMapMarkers"
    >
      <template #queryBar>
        <QueryBarItem label="灾害编号" :label-width="80">
          <NInput
            v-model:value="queryItems.dis_no"
            clearable
            type="text"
            placeholder="请输入要查询的灾害编号"
            @keypress.enter="$table?.handleSearch()"
          />
        </QueryBarItem>

        <QueryBarItem label="国家" :label-width="80">
          <NInput
            v-model:value="queryItems.country"
            clearable
            type="text"
            placeholder="请输入要查询的国家"
            @keypress.enter="$table?.handleSearch()"
          />
        </QueryBarItem>

        <QueryBarItem label="灾种" :label-width="80">
          <NInput
            v-model:value="queryItems.type"
            clearable
            type="text"
            placeholder="请输入要查询的灾害类型"
            @keypress.enter="$table?.handleSearch()"
          />
        </QueryBarItem>
        
        <QueryBarItem label="灾害时间" :label-width="80">
          <NDatePicker
            v-model:value="datetimeRange"
            type="datetimerange"
            clearable
            placeholder="请选择时间范围"
            @update:value="handleDateRangeChange"
          />
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

<style>
/* 图例样式 */
.disaster-legend {
  background: rgba(255, 255, 255, 0.4);
  padding: 10px;
  border-radius: 5px;
  box-shadow: 0 1px 5px rgba(0,0,0,0.4);
  min-width: 180px;
  max-height: 60vh;
  overflow: hidden;
  backdrop-filter: blur(2px);
}

.legend-header {
  font-weight: bold;
  margin-bottom: 8px;
  color: #333;
  font-size: 14px;
}

.legend-scroll {
  max-height: 55vh;
  overflow-y: auto;
  padding-right: 5px;
}

.legend-item {
  display: flex;
  align-items: center;
  margin: 5px 0;
  font-size: 12px;
  line-height: 1.4;
}

.legend-item i {
  display: inline-block;
  width: 16px;
  height: 16px;
  margin-right: 8px;
  border-radius: 50%;
  border: 1px solid rgba(0,0,0,0.2);
}

/* 滚动条样式 */
.legend-scroll::-webkit-scrollbar {
  width: 6px;
}

.legend-scroll::-webkit-scrollbar-track {
  background: rgba(0,0,0,0.1);
  border-radius: 3px;
}

.legend-scroll::-webkit-scrollbar-thumb {
  background: rgba(0,0,0,0.2);
  border-radius: 3px;
}
</style>