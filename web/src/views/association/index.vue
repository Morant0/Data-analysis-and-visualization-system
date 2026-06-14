<script setup>
import { ref, onMounted } from 'vue'
import {
    NTreeSelect, 
    NTag, 
    NLayout, 
    NLayoutSider, 
    NLayoutContent, 
    NSpace, 
    NDataTable, 
    NAlert,
    NText,
    NModal, 
    NCard, 
    NSpin, 
    NScrollbar,
} from 'naive-ui'
import CommonPage from '@/components/page/CommonPage.vue'
import api from '@/api'

// 添加AI分析相关状态
const aiAnalysis = ref('')
const isAnalyzing = ref(false)
const showAnalysis = ref(false)

// AI分析请求方法
const generateAIAnalysis = async () => {
  if (associations.value.length === 0) {
    aiAnalysis.value = "无有效数据可供分析"
    return
  }
  try {
    isAnalyzing.value = true
    showAnalysis.value = true
    
    // 构造提示词
    const prompt = currentDisaster.value 
      ? `请用中文分析${currentDisaster.value}灾害的主要关联规则，包含以下关键点：
         1. 主要次生灾害类型及概率
         2. 需要重点关注的指标（置信度/提升度）
         3. 应急准备建议
         基于以下数据：${JSON.stringify(associations.value)}`
      : `请用中文总结全局灾害关联规律，包含：
         1. 前3组最强关联规则
         2. 需要警惕的次生灾害链
         3. 整体应对策略建议
         基于以下数据：${JSON.stringify(associations.value)}`

    const res = await fetch("https://api.chatanywhere.tech/v1/chat/completions", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": "sk-eDp6NpKMPFVxTbg4CbEoLoeYMYIPypv2xhpaOCLQQ2IoC0Wi"
      },
      body: JSON.stringify({
        model: "gpt-4o",
        messages: [
          {
            role: "system",
            content: "你是一个专业的应急管理分析师，需要根据关联规则数据生成简明专业的分析报告"
          },
          {
            role: "user",
            content: prompt
          }
        ],
        temperature: 0.2
      })
    })

    const data = await res.json()
    aiAnalysis.value = data.choices[0].message.content
  } catch (error) {
    console.error("AI分析失败:", error)
    aiAnalysis.value = "分析生成失败，请稍后再试"
  } finally {
    isAnalyzing.value = false
  }
}

const associations = ref([])
const currentDisaster = ref(null)
const isLoading = ref(false)
const disasterOptions = ref([])

// 获取所有灾害类型选项
const loadDisasterOptions = async () => {
  const res = await api.gatAssociateList()
  const disasters = new Set()
  res.data.forEach(rule => {
    rule.antecedents.forEach(d => disasters.add(d))
    rule.consequents.forEach(d => disasters.add(d))
  })
  disasterOptions.value = Array.from(disasters).map(d => ({
    label: d,
    value: d,
    key: d
  }))
}

// 加载关联规则
const loadAssociations = async (type = null) => {
  try {
    isLoading.value = true
    const params = typeof type === 'string' ? { disaster_type: type } : {}
    const res = type 
      ? await api.getAssociateByType(params)
      : await api.gatAssociateList()
    
    associations.value = res.data
      .filter(rule => 
        !rule.antecedents.includes('None') && 
        !rule.consequents.includes('None')
      )
      .sort((a, b) => b.confidence - a.confidence)

    // 移除这里的 generateAIAnalysis() 调用
    aiAnalysis.value = '' // 清空之前的分析结果
  } catch (error) {
    console.error('加载数据失败:', error)
  } finally {
    isLoading.value = false
  }
}

// 初始化
onMounted(async () => {
  await loadDisasterOptions()
  await loadAssociations()
})

// 表格列配置
const columns = [
  {
    title: '前因灾害',
    key: 'antecedents',
    render: row => h(NSpace, row.antecedents.map(d => 
      h(NTag, { type: 'info', size: 'medium' }, { default: () => d })
    ))
  },
  {
    title: '可能引发的次生灾害',
    key: 'consequents',
    render: row => h(NSpace, row.consequents.map(d => 
      h(NTag, { type: 'error', size: 'medium' }, { default: () => d })
    ))
  },
  {
    title: '置信度',
    key: 'confidence',
    render: row => `${(row.confidence * 100).toFixed(1)}%`,
    sorter: (a, b) => a.confidence - b.confidence
  },
  {
    title: '支持度',
    key: 'support',
    render: row => `${(row.support * 100).toFixed(1)}%`
  },
  {
    title: '提升度',
    key: 'lift',
    render: row => row.lift.toFixed(2)
  }
]
</script>

<template>
  <CommonPage show-footer title="次生灾害分析">
    <NLayout has-sider>
      <!-- 左侧筛选栏 -->
      <NLayoutSider
        :width="280"
        collapse-mode="transform"
        content-style="padding:20px;"
        bordered
      >
        <NSpace vertical>
            <NText strong >灾害类型筛选</NText>
          <NTreeSelect
            v-model:value="currentDisaster"
            :options="disasterOptions"
            clearable
            filterable
            placeholder="选择或输入灾害类型"
            @update:value="val => loadAssociations(val)"
          />
          <NButton
            type="primary"
            block
            @click="currentDisaster = null; loadAssociations()"
          >
            显示全部关联关系
          </NButton>
          
          <NAlert title="指标说明" type="info">
            <p>✅ 置信度：前因发生时后果发生的概率</p>
            <p>📊 支持度：规则在数据中的出现频率</p>
            <p>📈 提升度：规则的有效性(>1表示正相关)</p>
          </NAlert>
        </NSpace>
      </NLayoutSider>

      <!-- 右侧内容区 -->
      <NLayoutContent content-style="padding:24px;">
        <NDataTable
          :columns="columns"
          :data="associations"
          :loading="isLoading"
          :bordered="false"
          :pagination="{ pageSize: 10 }"
          class="shadow-sm"
        >
          <template #empty>
            <div class="py-8 text-center text-gray-400">
              未找到相关灾害关联规则
            </div>
          </template>
        </NDataTable>

        <!-- 新增AI分析模块 -->
        <div class="mt-6">
        <NCard title="智能分析报告" :bordered="false" size="small">
            <template #header-extra>
              <NButton 
                size="small" 
                type="primary"
                @click="generateAIAnalysis"
                :loading="isAnalyzing"
                :disabled="associations.length === 0"
              >
                {{ aiAnalysis ? '重新分析' : '智能分析' }}
              </NButton>
            </template>
            
            <NScrollbar style="max-height: 500px" trigger="none">
            <NSpin :show="isAnalyzing">
                <div class="p-15 whitespace-pre-wrap text-gray-700">
                {{ aiAnalysis || "点击上方按钮生成分析报告" }}
                </div>
            </NSpin>
            </NScrollbar>
        </NCard>
        </div>
      </NLayoutContent>
    </NLayout>
  </CommonPage>
</template>