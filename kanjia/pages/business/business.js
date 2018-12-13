// pages/business/business.js
//获取应用实例
const app = getApp()
Page({

  /**
   * 页面的初始数据
   */
  data: {
    canIUse: wx.canIUse('button.open-type.getUserInfo'),
    sq_show: false,
    user_info: '',
    iphone_length : 0,
    name_length:0,
    add_length: 0,
    height: 0,
    width: 0,
  },
  // 记录姓名长度
  name_length: function (e) {
    this.setData({
      name_length: e.detail.value.length
    })
  },
  // 记录手机号长度
  iphone_length : function(e){
    this.setData({
      iphone_length: e.detail.value.length
    })
  },
  // 记录地址长度
  add_length: function (e) {
    this.setData({
      add_length: e.detail.value.length
    })
  },
  // 点击提交
  button : function(){
    if (this.data.name_length < 1) {
      wx.showToast({
        title: '请输入姓名',
        image: '../../img/x.png',
        duration: 2000
      })
      return false;
    } else if (this.data.iphone_length !== 11 || this.data.iphone_length < 1){
      wx.showToast({
        title: '手机格式不正常',
        image: '../../img/x.png',
        duration: 2000
      })
      return false;
    } else if (this.data.add_length < 1) {
      wx.showToast({
        title: '请输入地址',
        image: '../../img/x.png',
        duration: 2000
      })
      return false;
    }else{
      wx.showToast({
        title: '已提交',
        icon: 'success',
        duration: 2000
      })
    }
    
  },


  // 用户点击授权登录
  bindGetUserInfo: function (e) {
    app.login(this)
    if (e.detail && e.detail.rawData) {
      this.setData({ sq_show: false })
    }
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    var _this = this;
    //取出用户微信信息
    wx.getStorage({
      key: 'user_info',
      success: function (res) {
        _this.setData({
          user_info: res
        })
        console.log(_this.data.user_info)
      },
      // 获取失败说明没授权 打开授权提示框
      fail: function () {
        _this.setData({
          sq_show: true
        })
      }
    })
    // 获取屏幕可见区域
    wx.getSystemInfo({
      success: function (res) {
        _this.setData({
          height: res.windowHeight + 'px',
          width: res.windowWidth + 'px'
        })
      },
    })
  },

  /**
   * 生命周期函数--监听页面初次渲染完成
   */
  onReady: function () {

  },

  /**
   * 生命周期函数--监听页面显示
   */
  onShow: function () {

  },

  /**
   * 生命周期函数--监听页面隐藏
   */
  onHide: function () {

  },

  /**
   * 生命周期函数--监听页面卸载
   */
  onUnload: function () {

  },

  /**
   * 页面相关事件处理函数--监听用户下拉动作
   */
  onPullDownRefresh: function () {

  },

  /**
   * 页面上拉触底事件的处理函数
   */
  onReachBottom: function () {

  },

  /**
   * 用户点击右上角分享
   */
  onShareAppMessage: function () {

  }
})