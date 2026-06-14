<script setup>
import { onMounted, ref } from 'vue'
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
  NMessageProvider,
  useMessage, 
  NDataTable, 
  NStatistic, 
  NCarousel, 
  NCarouselItem,
} from 'naive-ui'
import { useRouter } from 'vue-router'
import api from '@/api'

const router = useRouter()
const message = useMessage()
const searchKeyword = ref('')

const handleSearch = async () => {
  const keyword = searchKeyword.value.trim()
  if (!keyword) {
    message.error('请输入搜索关键词')
    return
  }

  try {
    // 调用存在性校验接口
    const res = await api.IsExist( { keyword: keyword } )
    if (res.data[0].exists) {
      router.push({
        path: '/data-search',
        query: { keyword: searchKeyword.value.trim() }
      })
    } else {
      message.error('未检测到关键字数据，请重新输入！')
    }
  } catch (error) {
    message.error('校验服务异常，请稍后重试')
    console.error('校验关键字存在性失败:', error)
  }
}

// 新增响应式数据
const disasterCount = ref(0)
const affectedCount = ref(0)
const lossTotal = ref(0)
const disasterTypes = ref([])
const countryCounts = ref([])
const nYears = 5

// 获取数据的方法
const fetchData = async () => {
  try {
    // 获取统计数据
    const [countRes, affectedRes, lossRes, typeRes, countryRes] = await Promise.all([
      api.getRecentDisasterCount({n: nYears}),
      api.getRecentAffected({n: nYears}),
      api.getRecentLossTotal({n: nYears}),
      api.getYearCountByType({n: nYears}),
      api.getCountryDisasterCount({n: nYears})
    ])
    
    disasterCount.value = countRes.data.total_disaster_count
    affectedCount.value = affectedRes.data.total_affected / 10000
    lossTotal.value = (lossRes.data.total_loss / 10000).toFixed(1)
    
    // 处理灾害类型数据（取前8）
    disasterTypes.value = typeRes.data
      .sort((a,b) => b.total_count - a.total_count)
      .slice(0,8)
      .map(item => ({
        type: item.disaster_type,
        count: item.total_count
      }))
    
    // 处理国家数据（取前8）
    countryCounts.value = countryRes.data
      .sort((a,b) => b.count - a.count)
      .slice(0,8)
      .map(item => ({
        country: item.country,
        count: item.count
      }))
    
  } catch (error) {
    message.error('数据加载失败')
    console.error('获取数据失败:', error)
  }
}

// 生成时间范围字符串
const getDateRange = () => {
  const end = new Date()
  const start = new Date()
  start.setFullYear(end.getFullYear() - nYears)
  return `${start.toLocaleDateString()} - ${end.toLocaleDateString()}`
}

onMounted(() => {
  fetchData()
})

// 新增轮播图片数据
const carouselImages = ref([
  'src/picture/p1.png',
  'src/picture/p2.png',
  'src/picture/p3.png',
  'src/picture/p4.png',
  'src/picture/p5.png'
])

// 在原有代码基础上添加effect和duration配置
const carouselSettings = ref({
  effect: 'slide', // 使用滑动效果
  duration: 300,    // 动画时长调整为300ms
  interval: 4000    // 自动播放间隔保持5秒
})

</script>

<template>
  <NMessageProvider>
    <div class="home-container">
      <NSpace vertical align="center" :size="48">
        <!-- 标题部分 -->
        <NSpace vertical align="center" :size="12">
          <NText tag="h1" depth="1" class="main-title">
            自然灾害数据平台
          </NText>
          <NText tag="h2" depth="3" class="sub-title">
            综合性自然灾害数据查询发布门户
          </NText>
        </NSpace>

        <!-- 搜索区域 -->
        <NSpace
          vertical
          align="center"
          :size="24"
          class="search-wrapper"
        >
          <NSpace :size="16" align="center">
            <NInput
              v-model:value="searchKeyword"
              clearable
              placeholder="可以根据关键字查询，例如：国家、灾害编号、类型"
              style="width: 900px"
              @keyup.enter="handleSearch"
            >
            </NInput>
            <NButton
              type="primary"
              size="large"
              @click="handleSearch"
            >
              查询
            </NButton>
          </NSpace>
        </NSpace>
      </NSpace>

      <NLayout has-sider class="content-section">
        <NLayoutSider
          :width="650"
          :collapsed-width="0"
          :native-scrollbar="false"
        >
          <NSpace vertical :size="24">
            <!-- 标题和时间 -->
            <NSpace justify="space-between" align="center">
              <NText tag="div" depth="5" class="right-title">
                全球灾害实况
              </NText>
              <NText depth="3" style="font-size: 14px">
                {{ getDateRange() }}
              </NText>
            </NSpace>

            <!-- 统计数字 -->
            <NGrid :cols="3" :x-gap="10">
              <!-- 原有统计卡片保持不变 -->
              <NGridItem>
                <NCard>
                  <NStatistic
                    label="总频次"
                    :value="disasterCount"
                  />
                </NCard>
              </NGridItem>
              <NGridItem>
                <NCard>
                  <NStatistic
                    label="受影响人数（万人）"
                    :value="affectedCount.toLocaleString()"
                  />
                </NCard>
              </NGridItem>
              <NGridItem>
                <NCard>
                  <NStatistic
                    label="经济损失（亿美元）"
                    :value="`$${lossTotal.toLocaleString()}`"
                  />
                </NCard>
              </NGridItem>
            </NGrid>

            <!-- 双列表格布局 -->
            <NGrid :cols="2" :x-gap="12">
              <NGridItem>
                <NCard style="height: 100%" class="table-card">
                  <NDataTable
                    :columns="[{ title: '灾害类型', key: 'type' }, { title: '次数', key: 'count' }]"
                    :data="disasterTypes"
                    :bordered="false"
                  />
                </NCard>
              </NGridItem>
              <NGridItem>
                <NCard style="height: 100%" class="table-card">
                  <NDataTable
                    :columns="[{ title: '国家/地区', key: 'country' }, { title: '次数', key: 'count' }]"
                    :data="countryCounts"
                    :bordered="false"
                  />
                </NCard>
              </NGridItem>
            </NGrid>
          </NSpace>
        </NLayoutSider>

        <!-- 右侧布局保留 -->
        <NLayoutContent content-style="padding:24px; height: 100%;">
          <NCard content-style="height: 100%; padding: 0;" class="carousel-card">
            <NCarousel
              :show-dots="true"
              :effect="carouselSettings.effect"
              :duration="carouselSettings.duration"
              :interval="carouselSettings.interval"
              autoplay
              draggable
              dot-type="dot"
              dot-placement="bottom"
              style="height: 100%;"
            >
              <img
                v-for="(img, index) in carouselImages"
                :key="index"
                :src="img"
                class="carousel-image"
              />
              <template #dots="{ total, currentIndex, to }">
                <div class="custom-dots">
                  <button
                    v-for="index in total"
                    :key="index"
                    :class="['dot', currentIndex === index - 1 && 'active']"
                    @click="to(index - 1)"
                  />
                </div>
              </template>
            </NCarousel>
          </NCard>
        </NLayoutContent>
      </NLayout>
    </div>
  </NMessageProvider>
  
</template>

<style scoped>
.n-carousel--slide-left-enter-active,
.n-carousel--slide-right-enter-active,
.n-carousel--slide-left-leave-active,
.n-carousel--slide-right-leave-active {
  transition: transform v-bind('carouselSettings.duration + "ms"') cubic-bezier(0.4, 0, 0.2, 1);
}

/* 新增轮播相关样式 */
.carousel-card {
  height: calc(100%); /* 减去padding */
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.carousel-image {
  width: 100%;
  height: 100%;
}

.custom-dots {
  position: absolute;
  bottom: 20px;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  gap: 8px;
}

.dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  border: none;
  background-color: rgba(255, 255, 255, 0.5);
  cursor: pointer;
  transition: all 0.3s;
}

.dot.active {
  background-color: #2d8cf0;
  transform: scale(1.2);
}

.home-container {
  min-height: 100vh;
  /* 新增以下两行 */
  overflow-y: auto;
  height: 100vh;
  padding: 30px 4%;
  background: linear-gradient(135deg, #ffffff 0%, #ffffff 100%);
}

.n-card {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}
.content-section {
  flex: 1;
  margin-top: 48px;
  margin-bottom: 100px;
}

.n-layout-sider {
  height: calc(100vh - 300px);
  min-height: 700px;
  overflow-y: auto;
}

.n-layout-content {
  height: calc(100vh - 300px);
  min-height: 680px;
}


/* 表格卡片背景色 */
.table-card {
  background-color: #f5f5f5 !important; /* 浅灰色背景 */
}

.main-title {
  font-size: 50px;
  font-weight: 700;
  color: #2d8cf0;
  letter-spacing: 2px;
  text-shadow: 2px 2px 4px rgba(45, 140, 240, 0.1);
}

.right-title {
  font-size: 20px;
  font-weight: 600;
  color: #050505;
  letter-spacing: 2px;
  text-shadow: 2px 2px 4px rgba(45, 140, 240, 0.1);
}

.sub-title {
  font-size: 20px;
  color: #808695;
  font-weight: 400;
}

.search-wrapper {
  background: rgba(255, 255, 255, 0.9);
  padding: 32px 48px;
  border-radius: 16px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
}

</style>