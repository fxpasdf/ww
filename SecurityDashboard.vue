<template>
  <div class="flex h-screen bg-gray-50">
    <!-- 侧边栏 -->
    <div class="w-64 bg-white border-r shadow-sm h-screen overflow-y-auto">
      <div class="p-4 border-b">
        <h1 class="text-xl font-bold flex items-center gap-2">
          <shield-icon class="h-6 w-6 text-emerald-600" />
          <span>Linux基线检测系统</span>
        </h1>
      </div>
      <nav class="p-2">
        <button
          v-for="item in menuItems"
          :key="item.id"
          @click="activeTab = item.id"
          :class="[
            'w-full flex items-center gap-3 px-3 py-2 text-sm rounded-md transition-colors',
            'hover:bg-gray-100',
            activeTab === item.id ? 'bg-emerald-50 text-emerald-600 font-medium' : 'text-gray-500'
          ]"
        >
          <component :is="item.icon" class="h-5 w-5" />
          <span>{{ item.label }}</span>
          <chevron-right-icon v-if="activeTab === item.id" class="h-4 w-4 ml-auto" />
        </button>
      </nav>
    </div>

    <!-- 主内容区 -->
    <div class="flex flex-col flex-1 overflow-hidden">
      <!-- 头部 -->
      <header class="border-b bg-white p-4">
        <div class="flex items-center gap-3">
          <div class="p-2 rounded-md bg-emerald-50 text-emerald-600">
            <component :is="getTabInfo(activeTab).icon" class="h-5 w-5" />
          </div>
          <div>
            <h1 class="text-xl font-semibold">{{ getTabInfo(activeTab).title }}</h1>
            <p class="text-sm text-gray-500">{{ getTabInfo(activeTab).description }}</p>
          </div>
        </div>
      </header>

      <!-- 主内容 -->
      <main class="flex-1 overflow-auto p-6">
        <!-- 错误提示 -->
        <div v-if="error" class="mb-6 bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-md flex items-start">
          <alert-circle-icon class="h-5 w-5 mr-2 mt-0.5" />
          <span>{{ error }}</span>
        </div>

        <!-- 配置功能检查 -->
        <div v-if="activeTab === 'config'" class="bg-white rounded-lg border shadow-sm">
          <div class="p-6">
            <div class="mb-6">
              <button 
                @click="configScan" 
                :disabled="aLoading" 
                class="px-4 py-2 bg-emerald-600 text-white rounded-md hover:bg-emerald-700 flex items-center"
              >
                <loader-2-icon v-if="aLoading" class="mr-2 h-4 w-4 animate-spin" />
                配置功能检查
              </button>
            </div>

            <h2 class="text-xl font-semibold mb-4">配置功能检查结果</h2>

            <table class="w-full border-collapse">
              <thead>
                <tr class="border-b">
                  <th class="text-left py-3 px-4 w-[200px]">类型</th>
                  <th class="text-left py-3 px-4">检测结果</th>
                </tr>
              </thead>
              <tbody>
                <tr v-if="configTableData.length === 0" class="border-b">
                  <td colspan="2" class="text-center text-gray-500 py-6">
                    {{ aLoading ? "加载中..." : "暂无数据，请点击按钮开始检查" }}
                  </td>
                </tr>
                <tr v-for="(item, index) in configTableData" :key="index" class="border-b">
                  <td class="py-3 px-4 font-medium">{{ item.name }}</td>
                  <td class="py-3 px-4">{{ item.value }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- 安全漏洞检测 -->
        <div v-if="activeTab === 'vulnerability'" class="bg-white rounded-lg border shadow-sm">
          <div class="p-6">
            <div class="mb-6">
              <button 
                @click="vulnerabilityScan" 
                :disabled="aLoading" 
                class="px-4 py-2 bg-emerald-600 text-white rounded-md hover:bg-emerald-700 flex items-center"
              >
                <loader-2-icon v-if="aLoading" class="mr-2 h-4 w-4 animate-spin" />
                安全漏洞检测
              </button>
            </div>

            <h2 class="text-xl font-semibold mb-4">安全漏洞检测结果</h2>

            <table class="w-full border-collapse">
              <thead>
                <tr class="border-b">
                  <th class="text-left py-3 px-4 w-[200px]">类型</th>
                  <th class="text-left py-3 px-4">检测结果</th>
                </tr>
              </thead>
              <tbody>
                <tr v-if="vulnerabilityTableData.length === 0" class="border-b">
                  <td colspan="2" class="text-center text-gray-500 py-6">
                    {{ aLoading ? "加载中..." : "暂无数据，请点击按钮开始检测" }}
                  </td>
                </tr>
                <tr v-for="(item, index) in vulnerabilityTableData" :key="index" class="border-b">
                  <td class="py-3 px-4 font-medium">{{ item.name }}</td>
                  <td class="py-3 px-4">{{ item.value }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- 渗透测试 -->
        <div v-if="activeTab === 'penetration'" class="bg-white rounded-lg border shadow-sm">
          <div class="p-6">
            <div class="mb-6">
              <button 
                @click="penetrationScan" 
                :disabled="bLoading" 
                class="px-4 py-2 bg-emerald-600 text-white rounded-md hover:bg-emerald-700 flex items-center"
              >
                <loader-2-icon v-if="bLoading" class="mr-2 h-4 w-4 animate-spin" />
                开始渗透测试
              </button>
            </div>

            <h2 class="text-xl font-semibold mb-4">渗透测试报告</h2>

            <div class="bg-white rounded-lg border mb-6">
              <div class="p-4 border-b">
                <h3 class="text-lg font-medium">渗透测试结果</h3>
              </div>
              <div class="p-4">
                <table class="w-full border-collapse">
                  <thead>
                    <tr class="border-b">
                      <th class="text-left py-3 px-4 w-[200px]">检测项</th>
                      <th class="text-left py-3 px-4 w-[200px]">结果</th>
                      <th class="text-center py-3 px-4 w-[80px]">风险等级</th>
                      <th class="text-left py-3 px-4">修复建议</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-if="penetrationTableData.length === 0" class="border-b">
                      <td colspan="4" class="text-center text-gray-500 py-6">
                        {{ bLoading ? "加载中..." : "暂无数据，请点击按钮开始测试" }}
                      </td>
                    </tr>
                    <tr v-for="(item, index) in penetrationTableData" :key="index" class="border-b">
                      <td class="py-3 px-4 font-medium">{{ item.检测项 }}</td>
                      <td class="py-3 px-4">{{ item.结果 }}</td>
                      <td class="py-3 px-4 text-center">
                        <span 
                          :class="[
                            'px-2 py-1 text-xs font-medium rounded-full',
                            item.风险等级 === '高' ? 'bg-red-100 text-red-800' : 
                            item.风险等级 === '中' ? 'bg-amber-100 text-amber-800' : 
                            'bg-green-100 text-green-800'
                          ]"
                        >
                          {{ item.风险等级 }}
                        </span>
                      </td>
                      <td class="py-3 px-4">{{ item.修复建议 }}</td>
                    </tr>
                  </tbody>
                </table>

                <div v-if="penetrationResult && penetrationResult.总体评估" class="mt-6 p-4 border rounded-lg bg-gray-50">
                  <h3 class="text-lg font-medium mb-2">总体评估</h3>
                  <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div>
                      <p class="text-sm font-medium text-gray-500 mb-1">风险等级</p>
                      <span 
                        :class="[
                          'px-2 py-1 text-xs font-medium rounded-full',
                          penetrationResult.总体评估.风险等级 === '高' ? 'bg-red-100 text-red-800' : 
                          penetrationResult.总体评估.风险等级 === '中' ? 'bg-amber-100 text-amber-800' : 
                          'bg-green-100 text-green-800'
                        ]"
                      >
                        {{ penetrationResult.总体评估.风险等级 }}
                      </span>
                    </div>
                    <div>
                      <p class="text-sm font-medium text-gray-500 mb-1">修复建议</p>
                      <p>{{ penetrationResult.总体评估.修复建议 }}</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 代码审计 -->
        <div v-if="activeTab === 'codeAudit'" class="bg-white rounded-lg border shadow-sm">
          <div class="p-6">
            <div class="mb-6">
              <button 
                @click="codeAuditScan" 
                :disabled="cLoading" 
                class="px-4 py-2 bg-emerald-600 text-white rounded-md hover:bg-emerald-700 flex items-center"
              >
                <loader-2-icon v-if="cLoading" class="mr-2 h-4 w-4 animate-spin" />
                开始代码审计
              </button>
            </div>

            <h2 class="text-xl font-semibold mb-4">代码审计报告</h2>

            <div class="bg-white rounded-lg border mb-6">
              <div class="p-4 border-b">
                <h3 class="text-lg font-medium">代码审计结果</h3>
              </div>
              <div class="p-4">
                <table class="w-full border-collapse">
                  <thead>
                    <tr class="border-b">
                      <th class="text-left py-3 px-4 w-[180px]">文件</th>
                      <th class="text-left py-3 px-4 w-[100px]">检测项</th>
                      <th class="text-left py-3 px-4 w-[200px]">结果</th>
                      <th class="text-center py-3 px-4 w-[80px]">风险等级</th>
                      <th class="text-left py-3 px-4">修复建议</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-if="codeAuditTableData.length === 0" class="border-b">
                      <td colspan="5" class="text-center text-gray-500 py-6">
                        {{ cLoading ? "加载中..." : "暂无数据，请点击按钮开始审计" }}
                      </td>
                    </tr>
                    <tr v-for="(item, index) in codeAuditTableData" :key="index" class="border-b">
                      <td class="py-3 px-4 font-medium">{{ item.文件 }}</td>
                      <td class="py-3 px-4">{{ item.检测项 }}</td>
                      <td class="py-3 px-4">{{ item.结果 }}</td>
                      <td class="py-3 px-4 text-center">
                        <span 
                          :class="[
                            'px-2 py-1 text-xs font-medium rounded-full',
                            item.风险等级 === '高' ? 'bg-red-100 text-red-800' : 
                            item.风险等级 === '中' ? 'bg-amber-100 text-amber-800' : 
                            'bg-green-100 text-green-800'
                          ]"
                        >
                          {{ item.风险等级 }}
                        </span>
                      </td>
                      <td class="py-3 px-4">{{ item.修复建议 }}</td>
                    </tr>
                  </tbody>
                </table>

                <div v-if="codeAuditResult && codeAuditResult.总体评估" class="mt-6 p-4 border rounded-lg bg-gray-50">
                  <h3 class="text-lg font-medium mb-2">总体评估</h3>
                  <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div>
                      <p class="text-sm font-medium text-gray-500 mb-1">风险等级</p>
                      <span 
                        :class="[
                          'px-2 py-1 text-xs font-medium rounded-full',
                          codeAuditResult.总体评估.风险等级 === '高' ? 'bg-red-100 text-red-800' : 
                          codeAuditResult.总体评估.风险等级 === '中' ? 'bg-amber-100 text-amber-800' : 
                          'bg-green-100 text-green-800'
                        ]"
                      >
                        {{ codeAuditResult.总体评估.风险等级 }}
                      </span>
                    </div>
                    <div>
                      <p class="text-sm font-medium text-gray-500 mb-1">修复建议</p>
                      <p>{{ codeAuditResult.总体评估.修复建议 }}</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 系统性能检测 -->
        <div v-if="activeTab === 'performance'" class="bg-white rounded-lg border shadow-sm">
          <div class="p-6">
            <div class="mb-6">
              <button 
                @click="performanceScan" 
                :disabled="dLoading" 
                class="px-4 py-2 bg-emerald-600 text-white rounded-md hover:bg-emerald-700 flex items-center"
              >
                <loader-2-icon v-if="dLoading" class="mr-2 h-4 w-4 animate-spin" />
                获取性能数据
              </button>
            </div>

            <h2 class="text-xl font-semibold mb-4">系统性能检测结果</h2>

            <table class="w-full border-collapse">
              <thead>
                <tr class="border-b">
                  <th class="text-left py-3 px-4 w-[200px]">性能指标</th>
                  <th class="text-left py-3 px-4">当前值</th>
                </tr>
              </thead>
              <tbody>
                <tr v-if="performanceTableData.length === 0" class="border-b">
                  <td colspan="2" class="text-center text-gray-500 py-6">
                    {{ dLoading ? "加载中..." : "暂无数据，请点击按钮获取性能数据" }}
                  </td>
                </tr>
                <tr v-for="(item, index) in performanceTableData" :key="index" class="border-b">
                  <td class="py-3 px-4 font-medium">{{ item.name }}</td>
                  <td class="py-3 px-4">{{ item.value }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- 系统脆弱性评估 -->
        <div v-if="activeTab === 'system-assessment'" class="bg-white rounded-lg border shadow-sm">
          <div class="p-6">
            <div class="mb-6">
              <button 
                @click="reporterScan" 
                :disabled="dLoading" 
                class="px-4 py-2 bg-emerald-600 text-white rounded-md hover:bg-emerald-700 flex items-center"
              >
                <loader-2-icon v-if="dLoading" class="mr-2 h-4 w-4 animate-spin" />
                开始评估
              </button>
            </div>

            <h2 class="text-xl font-semibold mb-4">系统脆弱性评估</h2>

            <div v-if="reporterResult" class="mb-6">
              <div class="flex space-x-2 border-b mb-6">
                <button 
                  v-for="tab in assessmentTabs" 
                  :key="tab.id"
                  @click="activeAssessmentTab = tab.id"
                  :class="[
                    'px-4 py-2 text-sm font-medium',
                    activeAssessmentTab === tab.id ? 'border-b-2 border-emerald-600 text-emerald-600' : 'text-gray-500'
                  ]"
                >
                  {{ tab.label }}
                </button>
              </div>

              <!-- 总体评估 -->
              <div v-if="activeAssessmentTab === 'overview'" class="bg-white rounded-lg border">
                <div class="p-6">
                  <h3 class="text-lg font-medium mb-4">总体评估</h3>
                  <table class="w-full border-collapse">
                    <thead>
                      <tr class="border-b">
                        <th class="text-left py-3 px-4 w-[120px]">风险等级</th>
                        <th class="text-left py-3 px-4">修复建议</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr v-for="(item, index) in reporterTableData" :key="index" class="border-b">
                        <td class="py-3 px-4">
                          <span 
                            :class="[
                              'px-2 py-1 text-xs font-medium rounded-full',
                              item.风险等级 === '高' ? 'bg-red-100 text-red-800' : 
                              item.风险等级 === '中' ? 'bg-amber-100 text-amber-800' : 
                              'bg-green-100 text-green-800'
                            ]"
                          >
                            {{ item.风险等级 }}
                          </span>
                        </td>
                        <td class="py-3 px-4">{{ item.修复建议 }}</td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </div>

              <!-- 配置功能 -->
              <div v-if="activeAssessmentTab === 'config'" class="bg-white rounded-lg border">
                <div class="p-6">
                  <h3 class="text-lg font-medium mb-4">配置功能检查</h3>
                  <table class="w-full border-collapse">
                    <thead>
                      <tr class="border-b">
                        <th class="text-left py-3 px-4 w-[200px]">类型</th>
                        <th class="text-left py-3 px-4">检测结果</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr v-for="(item, index) in configTableData" :key="index" class="border-b">
                        <td class="py-3 px-4 font-medium">{{ item.name }}</td>
                        <td class="py-3 px-4">{{ item.value }}</td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </div>

              <!-- 其他标签页内容类似，根据需要添加 -->
            </div>
            <div v-else class="text-center text-gray-500 py-12">
              {{ dLoading ? "加载中..." : "暂无数据，请点击按钮开始评估" }}
            </div>
          </div>
        </div>
      </main>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { 
  Shield, 
  AlertTriangle, 
  Terminal, 
  Code, 
  BarChart3, 
  FileWarning, 
  ChevronRight,
  AlertCircle,
  Loader2
} from 'lucide-vue-next';

export default {
  name: "SecurityDashboard",
  components: {
    ShieldIcon: Shield,
    AlertTriangleIcon: AlertTriangle,
    TerminalIcon: Terminal,
    CodeIcon: Code,
    BarChart3Icon: BarChart3,
    FileWarningIcon: FileWarning,
    ChevronRightIcon: ChevronRight,
    AlertCircleIcon: AlertCircle,
    Loader2Icon: Loader2
  },
  data() {
    return {
      activeTab: "config",
      activeAssessmentTab: "overview",
      aLoading: false,
      bLoading: false,
      cLoading: false,
      dLoading: false,
      error: "",
      baseUrl: "http://localhost:5000/",
      configResult: null,
      vulnerabilityResult: null,
      performanceResult: null,
      penetrationResult: {
        总体评估: {
          风险等级: "",
          修复建议: "",
        },
        渗透测试结果: {},
      },
      codeAuditResult: {
        总体评估: {
          风险等级: "",
          修复建议: "",
        },
        代码审计结果: {},
      },
      reporterResult: {
        总体评估: {},
      },
      menuItems: [
        {
          id: "config",
          label: "配置功能检查",
          icon: "ShieldIcon",
        },
        {
          id: "vulnerability",
          label: "安全漏洞检测",
          icon: "AlertTriangleIcon",
        },
        {
          id: "penetration",
          label: "渗透测试",
          icon: "TerminalIcon",
        },
        {
          id: "codeAudit",
          label: "代码审计",
          icon: "CodeIcon",
        },
        {
          id: "performance",
          label: "系统性能检测",
          icon: "BarChart3Icon",
        },
        {
          id: "system-assessment",
          label: "系统脆弱性评估",
          icon: "FileWarningIcon",
        },
      ],
      assessmentTabs: [
        { id: "overview", label: "总体评估" },
        { id: "config", label: "配置功能" },
        { id: "vulnerability", label: "安全漏洞" },
        { id: "penetration", label: "渗透测试" },
        { id: "codeAudit", label: "代码审计" },
        { id: "performance", label: "系统性能" },
      ]
    };
  },
  computed: {
    configTableData() {
      if (!this.configResult) return [];
      return Object.keys(this.configResult).map((key) => ({
        name: key,
        value: Array.isArray(this.configResult[key])
          ? this.configResult[key].join(", ")
          : this.configResult[key],
      }));
    },
    vulnerabilityTableData() {
      if (!this.vulnerabilityResult) return [];
      return Object.keys(this.vulnerabilityResult).map((key) => ({
        name: key,
        value: Array.isArray(this.vulnerabilityResult[key])
          ? this.vulnerabilityResult[key].join(", ")
          : this.vulnerabilityResult[key],
      }));
    },
    performanceTableData() {
      if (!this.performanceResult) return [];
      return Object.keys(this.performanceResult).map((key) => ({
        name: key,
        value: Array.isArray(this.performanceResult[key])
          ? this.performanceResult[key].join(", ")
          : this.performanceResult[key],
      }));
    },
    penetrationTableData() {
      return Object.values(this.penetrationResult.渗透测试结果);
    },
    reporterTableData() {
      var arr = Object.values(this.reporterResult.总体评估);
      var list = [
        {
          修复建议: arr[0],
          风险等级: arr[1],
        },
      ];
      return list;
    },
    codeAuditTableData() {
      const results = [];
      const codeAuditResults = this.codeAuditResult.代码审计结果;
      for (const file in codeAuditResults) {
        codeAuditResults[file].forEach((item) => {
          results.push({
            文件: file,
            ...item,
          });
        });
      }
      return results;
    },
  },
  methods: {
    getTabInfo(tab) {
      switch (tab) {
        case "config":
          return {
            title: "配置功能检查",
            description: "检查系统配置和功能是否正常",
            icon: "ShieldIcon",
          };
        case "vulnerability":
          return {
            title: "安全漏洞检测",
            description: "检测系统中的安全漏洞",
            icon: "AlertTriangleIcon",
          };
        case "penetration":
          return {
            title: "渗透测试",
            description: "模拟攻击者行为进行渗透测试",
            icon: "TerminalIcon",
          };
        case "codeAudit":
          return {
            title: "代码审计",
            description: "审计代码中的安全问题",
            icon: "CodeIcon",
          };
        case "performance":
          return {
            title: "系统性能检测",
            description: "检测系统性能指标",
            icon: "BarChart3Icon",
          };
        case "system-assessment":
          return {
            title: "系统脆弱性评估",
            description: "全面评估系统安全脆弱性",
            icon: "FileWarningIcon",
          };
        default:
          return {
            title: "配置功能检查",
            description: "检查系统配置和功能是否正常",
            icon: "ShieldIcon",
          };
      }
    },
    // 开始配置功能检查
    async configScan() {
      this.aLoading = true;
      this.error = "";
      
      try {
        const response = await axios.get(`${this.baseUrl}/config`);
        this.configResult = response.data;
      } catch (err) {
        this.error = "获取失败: " + (err.response?.data?.error || err.message);
      } finally {
        this.aLoading = false;
      }
    },
    // 漏洞检查
    async vulnerabilityScan() {
      this.aLoading = true;
      this.error = "";
      
      try {
        const response = await axios.get(`${this.baseUrl}/vuln`);
        this.vulnerabilityResult = response.data;
      } catch (err) {
        this.error = "获取失败: " + (err.response?.data?.error || err.message);
      } finally {
        this.aLoading = false;
      }
    },
    // 渗透检查
    async penetrationScan() {
      this.bLoading = true;
      this.error = "";
      
      try {
        const response = await axios.get(`${this.baseUrl}/penetration_test`);
        this.penetrationResult = response.data;
      } catch (err) {
        this.error = "获取失败: " + (err.response?.data?.error || err.message);
      } finally {
        this.bLoading = false;
      }
    },
    // 开始代码审计
    async codeAuditScan() {
      this.cLoading = true;
      this.error = "";
      
      try {
        const response = await axios.get(`${this.baseUrl}/code_audit`);
        this.codeAuditResult = response.data;
      } catch (err) {
        this.error = "代码审计失败: " + (err.response?.data?.error || err.message);
      } finally {
        this.cLoading = false;
      }
    },
    // 获取性能数据
    async performanceScan() {
      this.dLoading = true;
      this.error = "";
      
      try {
        const response = await axios.get(`${this.baseUrl}/performance`);
        this.performanceResult = response.data;
      } catch (err) {
        this.error = "获取性能数据失败: " + (err.response?.data?.error || err.message);
      } finally {
        this.dLoading = false;
      }
    },
    // 系统脆弱性评估
    async reporterScan() {
      this.dLoading = true;
      this.error = "";
      
      try {
        const response = await axios.get(`${this.baseUrl}/vulnerability_report`);
        this.reporterResult = response.data;
        
        // 获取其他数据以生成综合报告
        try {
          const configResponse = await axios.get(`${this.baseUrl}/config`);
          this.configResult = configResponse.data;
        } catch (err) {
          console.error("Failed to fetch config data", err);
        }

        try {
          const vulnResponse = await axios.get(`${this.baseUrl}/vuln`);
          this.vulnerabilityResult = vulnResponse.data;
        } catch (err) {
          console.error("Failed to fetch vulnerability data", err);
        }

        try {
          const penetrationResponse = await axios.get(`${this.baseUrl}/penetration_test`);
          this.penetrationResult = penetrationResponse.data;
        } catch (err) {
          console.error("Failed to fetch penetration test data", err);
        }

        try {
          const codeAuditResponse = await axios.get(`${this.baseUrl}/code_audit`);
          this.codeAuditResult = codeAuditResponse.data;
        } catch (err) {
          console.error("Failed to fetch code audit data", err);
        }

        try {
          const performanceResponse = await axios.get(`${this.baseUrl}/performance`);
          this.performanceResult = performanceResponse.data;
        } catch (err) {
          console.error("Failed to fetch performance data", err);
        }
      } catch (err) {
        this.error = "评估失败: " + (err.response?.data?.error || err.message);
      } finally {
        this.dLoading = false;
      }
    }
  }
};
</script>

<style>
/* 添加一些基本样式 */
body {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
  line-height: 1.5;
  color: #374151;
}

/* 添加 Tailwind 的基础样式 */
@tailwind base;
@tailwind components;
@tailwind utilities;
</style>

