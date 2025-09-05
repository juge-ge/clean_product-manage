<template>
  <div class="pcb-basic-info">
    <h2>企业基本信息</h2>
    <form @submit.prevent="handleSubmit" class="basic-info-form">
      <!-- 地区信息 -->
      <div class="form-group">
        <label for="city">所属地市：</label>
        <input 
          type="text" 
          id="city" 
          v-model="formData.city" 
          required
          class="form-input"
        >
      </div>

      <div class="form-group">
        <label for="county">所属县：</label>
        <input 
          type="text" 
          id="county" 
          v-model="formData.county" 
          required
          class="form-input"
        >
      </div>

      <!-- 企业基本信息 -->
      <div class="form-group">
        <label for="name">企业名称：</label>
        <input 
          type="text" 
          id="name" 
          v-model="formData.name" 
          required
          class="form-input"
        >
      </div>

      <div class="form-group">
        <label for="scale">企业规模：</label>
        <select 
          id="scale" 
          v-model="formData.scale" 
          required
          class="form-input"
        >
          <option value="">请选择</option>
          <option value="large">大型</option>
          <option value="medium">中型</option>
          <option value="small">小型</option>
          <option value="micro">微型</option>
        </select>
      </div>

      <!-- 财务信息 -->
      <div class="form-group">
        <label for="registeredCapital">注册资本（万元）：</label>
        <input 
          type="number" 
          id="registeredCapital" 
          v-model="formData.registeredCapital" 
          required
          min="0"
          class="form-input"
        >
      </div>

      <div class="form-group">
        <label for="annualOutput">年产值（万元）：</label>
        <input 
          type="number" 
          id="annualOutput" 
          v-model="formData.annualOutput" 
          required
          min="0"
          class="form-input"
        >
      </div>

      <div class="form-group">
        <label for="annualSales">年销售额（万元）：</label>
        <input 
          type="number" 
          id="annualSales" 
          v-model="formData.annualSales" 
          required
          min="0"
          class="form-input"
        >
      </div>

      <!-- 法人信息 -->
      <div class="form-group">
        <label for="legalRepresentative">法人代表：</label>
        <input 
          type="text" 
          id="legalRepresentative" 
          v-model="formData.legalRepresentative" 
          required
          class="form-input"
        >
      </div>

      <!-- 地址信息 -->
      <div class="form-group">
        <label for="registeredAddress">注册地址：</label>
        <input 
          type="text" 
          id="registeredAddress" 
          v-model="formData.registeredAddress" 
          required
          class="form-input"
        >
      </div>

      <div class="form-group">
        <label for="productionAddress">生产地址：</label>
        <input 
          type="text" 
          id="productionAddress" 
          v-model="formData.productionAddress" 
          required
          class="form-input"
        >
      </div>

      <div class="form-group">
        <label for="postalCode">邮编：</label>
        <input 
          type="text" 
          id="postalCode" 
          v-model="formData.postalCode" 
          required
          pattern="[0-9]{6}"
          class="form-input"
        >
      </div>

      <!-- 联系信息 -->
      <div class="form-group">
        <label for="contactPerson">联系人：</label>
        <input 
          type="text" 
          id="contactPerson" 
          v-model="formData.contactPerson" 
          required
          class="form-input"
        >
      </div>

      <div class="form-group">
        <label for="contactPhone">联系电话：</label>
        <input 
          type="tel" 
          id="contactPhone" 
          v-model="formData.contactPhone" 
          required
          pattern="[0-9-]{7,13}"
          class="form-input"
        >
      </div>

      <!-- 其他信息 -->
      <div class="form-group">
        <label for="establishmentDate">建厂时间：</label>
        <input 
          type="date" 
          id="establishmentDate" 
          v-model="formData.establishmentDate" 
          required
          class="form-input"
        >
      </div>

      <div class="form-group">
        <label for="industry">所属行业：</label>
        <input 
          type="text" 
          id="industry" 
          v-model="formData.industry" 
          required
          class="form-input"
        >
      </div>

      <!-- 提交按钮 -->
      <div class="form-actions">
        <button type="submit" class="submit-btn">保存信息</button>
        <button type="button" @click="resetForm" class="reset-btn">重置</button>
      </div>
    </form>
  </div>
</template>

<script>
export default {
  name: 'PCBBasicInfo',
  data() {
    return {
      formData: {
        city: '',
        county: '',
        name: '',
        scale: '',
        registeredCapital: '',
        annualOutput: '',
        annualSales: '',
        legalRepresentative: '',
        registeredAddress: '',
        productionAddress: '',
        postalCode: '',
        contactPerson: '',
        contactPhone: '',
        establishmentDate: '',
        industry: ''
      }
    }
  },
  methods: {
    handleSubmit() {
      // TODO: 实现表单提交逻辑
      console.log('提交的表单数据：', this.formData)
    },
    resetForm() {
      Object.keys(this.formData).forEach(key => {
        this.formData[key] = ''
      })
    }
  }
}
</script>

<style scoped>
.pcb-basic-info {
  padding: 20px;
  max-width: 800px;
  margin: 0 auto;
}

h2 {
  color: #333;
  margin-bottom: 30px;
  text-align: center;
}

.basic-info-form {
  background: #fff;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.form-group {
  margin-bottom: 20px;
  display: flex;
  align-items: center;
}

label {
  width: 150px;
  text-align: right;
  margin-right: 15px;
  color: #606266;
}

.form-input {
  flex: 1;
  height: 36px;
  line-height: 36px;
  padding: 0 12px;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  transition: border-color 0.2s;
}

.form-input:focus {
  border-color: #409eff;
  outline: none;
}

.form-input:hover {
  border-color: #c0c4cc;
}

.form-actions {
  margin-top: 30px;
  text-align: center;
}

.submit-btn,
.reset-btn {
  padding: 10px 20px;
  font-size: 14px;
  border-radius: 4px;
  cursor: pointer;
  margin: 0 10px;
  border: none;
}

.submit-btn {
  background-color: #409eff;
  color: white;
}

.submit-btn:hover {
  background-color: #66b1ff;
}

.reset-btn {
  background-color: #909399;
  color: white;
}

.reset-btn:hover {
  background-color: #a6a9ad;
}
</style>
