import { request } from '@/utils'

export default {
  login: (data) => request.post('/base/access_token', data, { noNeedToken: true }),
  getUserInfo: () => request.get('/base/userinfo'),
  getUserMenu: () => request.get('/base/usermenu'),
  getUserApi: () => request.get('/base/userapi'),
  // profile
  updatePassword: (data = {}) => request.post('/base/update_password', data),
  // users
  getUserList: (params = {}) => request.get('/user/list', { params }),
  getUserById: (params = {}) => request.get('/user/get', { params }),
  createUser: (data = {}) => request.post('/user/create', data),
  updateUser: (data = {}) => request.post('/user/update', data),
  deleteUser: (params = {}) => request.delete(`/user/delete`, { params }),
  resetPassword: (data = {}) => request.post(`/user/reset_password`, data),
  // role
  getRoleList: (params = {}) => request.get('/role/list', { params }),
  createRole: (data = {}) => request.post('/role/create', data),
  updateRole: (data = {}) => request.post('/role/update', data),
  deleteRole: (params = {}) => request.delete('/role/delete', { params }),
  updateRoleAuthorized: (data = {}) => request.post('/role/authorized', data),
  getRoleAuthorized: (params = {}) => request.get('/role/authorized', { params }),
  // menus
  getMenus: (params = {}) => request.get('/menu/list', { params }),
  createMenu: (data = {}) => request.post('/menu/create', data),
  updateMenu: (data = {}) => request.post('/menu/update', data),
  deleteMenu: (params = {}) => request.delete('/menu/delete', { params }),
  // apis
  getApis: (params = {}) => request.get('/api/list', { params }),
  createApi: (data = {}) => request.post('/api/create', data),
  updateApi: (data = {}) => request.post('/api/update', data),
  deleteApi: (params = {}) => request.delete('/api/delete', { params }),
  refreshApi: (data = {}) => request.post('/api/refresh', data),
  // depts
  getDepts: (params = {}) => request.get('/dept/list', { params }),
  createDept: (data = {}) => request.post('/dept/create', data),
  updateDept: (data = {}) => request.post('/dept/update', data),
  deleteDept: (params = {}) => request.delete('/dept/delete', { params }),
  // auditlog
  getAuditLogList: (params = {}) => request.get('/auditlog/list', { params }),
  // disasters
  getDisaster: (params = {}) => request.get('/disaster/get', { params }),
  getDisasterList: (params = {}) => request.get('/disaster/list', { params }),
  createDisaster: (data = {}) => request.post('/disaster/create', data),
  updateDisaster: (data = {}) => request.post('/disaster/update', data),
  deleteDisaster: (params = {}) => request.delete('/disaster/delete', { params }),
  getYearCount: (params = {}) => request.get('/disaster/yearly_count', { params }),
  getYearCountByType: (params = {}) => request.get('/disaster/yearly_count_by_type', { params }),
  getCountryDisasterCount: (params = {}) => request.get('/disaster/country-disaster-count', { params }),
  IsExist: (params = {}) => request.get('/disaster/check-keyword', { params }),
  getRecentDisasterCount: (params = {}) => request.get('/disaster/recent-disaster-count', { params }),
  getCountryCount: (params = {}) => request.get('/disaster/country-count', { params }),
  // human_impact
  getHumanImpact: (params = {}) => request.get('/human_impact/get', { params }),
  getRecentStats: (params = {}) => request.get('/human_impact/recent-stats', { params }),
  getRecentStatsByType: (params = {}) => request.get('/human_impact/recent-type-stats', { params }),
  getCountryCasualties: (params = {}) => request.get('/human_impact/recent-country-casualties', { params }),
  getRecentAffected: (params = {}) => request.get('/human_impact/recent-affected-total', { params }),
  getCountryAffected: (params = {}) => request.get('/human_impact/country-affected-people', { params }),
  getCoutry_casualties: (params = {}) => request.get('/human_impact/country-casualties', { params }),
  // economic_loss
  getEconomicLoss: (params = {}) => request.get('/economic_loss/get', { params }),
  getRecentLoss: (params = {}) => request.get('/economic_loss/recent-loss', { params }),
  getRecentLossByType: (params = {}) => request.get('/economic_loss/recent-type-loss', { params }),
  getCountryLoss: (params = {}) => request.get('/economic_loss/recent-country-loss', { params }),
  getRecentLossTotal: (params = {}) => request.get('/economic_loss/recent-loss-total', { params }),
  getCountry_Loss: (params = {}) => request.get('/economic_loss/country-economic-loss', { params }),
  // association
  gatAssociateList: (params = {}) => request.get('/association/list', { params }),
  getAssociateByType: (params = {}) => request.get('/association/get', { params }),

}
