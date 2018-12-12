//index.js
//获取应用实例
const app = getApp()
Page({
  data: {
    canIUse: wx.canIUse('button.open-type.getUserInfo'),
    height: 0,
    sq_show: app.sq_show,
    user_info: '',
    width: 0,
    topshow: false,
    ss_yx: false,
    scroll_top: 0,
    ss_text: '',
    ss_input: '',
    list: [{ title: '这里是标题11111', num: 1236, money: 689.99 }, { title: '这里是标题22222222222222222222222222', num: 3298, money: 495.56 }, { title: '这里是标题11111', num: 1236, money: 689.99 }, { title: '这里是标题22222222222222222222222222', num: 3298, money: 495.56 }, { title: '这里是标题11111', num: 1236, money: 689.99 }, { title: '这里是标题22222222222222222222222222', num: 3298, money: 495.56 }]
  },

  //事件处理函数
  bindViewTap: function () {
    wx.navigateTo({
      url: '../logs/logs'
    })
  },
  // 点击进入商品详情
  list_click: function () {
    wx.navigateTo({
      url: '../info/info'
    })
  },
  // 点击搜索框
  ss_input: function () {
    this.setData({
      ss_yc: true,
      ss_text: 1
    })
  },
  //当搜索框输入时事件
  bind_ss_input: function (e) {
    var _this = this;
  },
  // 搜索确实时
  bind_ss_confirm: function (e) {
    var _this = this;
    console.log(e.detail.value)
  },
  //搜索框点击X取消事件
  ss_x: function () {
    this.setData({
      ss_yc: false,
      ss_text: '',
      ss_input: ''
    })
  },

  //滚动出现返回顶部
  scroll: function (e) {
    if (e.detail.scrollTop > parseInt(this.data.height)) {
      this.setData({
        topshow: true
      })
    }

    if (e.detail.scrollTop < parseInt(this.data.height)) {
      this.setData({
        topshow: false
      })
    }
  },

  //点击返回顶部
  handletap: function () {
    this.setData({
      scroll_top: 0
    })
  },
  // 用户点击授权登录
  bindGetUserInfo: function (e) {
    console.log(e)
    app.login(this)
  },

  // 页面加载
  onLoad: function () {
    console.log(this.data.sq_show)
    var _this = this;
    //取出用户微信信息
    wx.getStorage({
      key: 'user_info',
      success: function (res) {
        _this.setData({
          user_info: res
        })
        // console.log(_this.data.user_info)
      },
    })

    // 获取首页数据
    wx.request({
      url: app.http,
      method: 'GET',
      data: {

      },
      header: { "Content-Type": "application/x-www-form-urlencoded" },
      dataType: 'json',
      success: function (r) {
        // console.log(r)
      }
    });

    var _this = this;
    // 获取屏幕可见区域
    wx.getSystemInfo({
      success: function (res) {
        _this.setData({
          height: res.windowHeight + 'px',
          width: res.windowWidth + 'px'
        })
      },
    })
    if (app.globalData.userInfo) {
      this.setData({
        userInfo: app.globalData.userInfo,
        hasUserInfo: true,
        // bbb: app.aa
      })
    } else if (this.data.canIUse) {
      // 由于 getUserInfo 是网络请求，可能会在 Page.onLoad 之后才返回
      // 所以此处加入 callback 以防止这种情况
      app.userInfoReadyCallback = res => {
        this.setData({
          userInfo: res.userInfo,
          hasUserInfo: true
        })
      }
    } else {
      // 在没有 open-type=getUserInfo 版本的兼容处理
      wx.getUserInfo({
        success: res => {
          app.globalData.userInfo = res.userInfo
          this.setData({
            userInfo: res.userInfo,
            hasUserInfo: true
          })
        }
      })
    }
  },
  getUserInfo: function (e) {
    app.globalData.userInfo = e.detail.userInfo
    this.setData({
      userInfo: e.detail.userInfo,
      hasUserInfo: true
    })
  },
})
