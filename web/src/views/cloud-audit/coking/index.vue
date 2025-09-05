<template>
  <div class="coking-audit">
    <div class="page-header">
      <h1>焦化行业审核</h1>
      <p>焦化企业清洁生产审核全流程管理</p>
    </div>
    
    <div class="audit-steps">
      <div class="step-card" @click="navigateTo('basic-info')">
        <div class="step-icon">
          <i class="carbon:information"></i>
        </div>
        <h3>企业基本信息</h3>
        <p>录入企业基础信息和资质材料</p>
      </div>
      
      <div class="step-card" @click="navigateTo('planning')">
        <div class="step-icon">
          <i class="carbon:plan"></i>
        </div>
        <h3>筹划与组织</h3>
        <p>制定审核计划和组织架构</p>
      </div>
      
      <div class="step-card" @click="navigateTo('pre-audit')">
        <div class="step-icon">
          <i class="mdi:check-circle"></i>
        </div>
        <h3>预审核</h3>
        <p>预审核阶段资料准备和评估</p>
      </div>
      
      <div class="step-card" @click="navigateTo('audit')">
        <div class="step-icon">
          <i class="mdi:clipboard-check"></i>
        </div>
        <h3>审核</h3>
        <p>正式审核流程和现场检查</p>
      </div>
      
      <div class="step-card" @click="navigateTo('scheme-library')">
        <div class="step-icon">
          <i class="mdi:library"></i>
        </div>
        <h3>清洁生产方案库</h3>
        <p>清洁生产技术改造方案管理</p>
      </div>
      
      <div class="step-card" @click="navigateTo('report')">
        <div class="step-icon">
          <i class="carbon:report"></i>
        </div>
        <h3>审核评估报告</h3>
        <p>生成清洁生产审核评估报告</p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'CokingAudit',
  methods: {
    navigateTo(step) {
      this.$router.push(`/cloud-audit/coking/${step}`)
    }
  }
}
</script>

<style scoped>
.coking-audit {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.page-header {
  text-align: center;
  margin-bottom: 40px;
}

.page-header h1 {
  color: #333;
  font-size: 28px;
  margin-bottom: 10px;
}

.page-header p {
  color: #666;
  font-size: 16px;
}

.audit-steps {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 20px;
}

.step-card {
  background: #fff;
  border-radius: 8px;
  padding: 30px 20px;
  text-align: center;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  cursor: pointer;
  transition: all 0.3s ease;
  border: 2px solid transparent;
}

.step-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
  border-color: #409eff;
}

.step-icon {
  font-size: 48px;
  color: #409eff;
  margin-bottom: 20px;
}

.step-card h3 {
  color: #333;
  font-size: 18px;
  margin-bottom: 10px;
}

.step-card p {
  color: #666;
  font-size: 14px;
  line-height: 1.5;
}
</style>
