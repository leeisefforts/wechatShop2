// pages/user/user.js
const app = getApp()
Page({

  /**
   * 页面的初始数据
   */
  data: {
    canIUse: wx.canIUse('button.open-type.getUserInfo'),
    sq_show: false,
    user_info: '',
    token:'',
    openid : '',
    avatarUrl : '',
    nickName : ''
  },
  // 用户点击授权登录
  bindGetUserInfo: function (e) {
    app.login(this)
    if (e.detail && e.detail.rawData) {
      this.setData({ sq_show: false })
    }
  },

  //砍价页面
  kanjia : function(){
    wx.navigateTo({
      url: '../kj_list/kj_list',
    })
  },


  //订单页面
  dingdan: function () {
    wx.navigateTo({
      url: '../dd_list/dd_list',
    })
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    var _this = this;
    _this.setData({
      openid: app.getCache('openid'),
      token: app.getCache('token'),
      nickName: app.getCache('user_info').nickName,
      avatarUrl: app.getCache('user_info').avatarUrl
    })
    // 判断是否授权登陆过
    setTimeout(function () {
      console.log(_this.data.token)
      if (_this.data.token == '') {
        _this.setData({
          sq_show: true
        })
      } else {
        _this.setData({
          sq_show: false
        })
      }
    },2000)
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
    var _this = this;
    _this.setData({
      openid: app.getCache('openid'),
      token: app.getCache('token'),
      nickName: app.getCache('user_info').nickName,
      avatarUrl: app.getCache('user_info').avatarUrl
    })
    console.log(app.getCache('user_info').nickName)
    // 判断是否授权登陆过
    setTimeout(function () {
      console.log(_this.data.token)
      if (_this.data.token == '') {
        _this.setData({
          sq_show: true
        })
      } else {
        _this.setData({
          sq_show: false
        })
      }
    }, 2000)
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

})