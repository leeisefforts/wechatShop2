//index.js
//获取应用实例
const app = getApp()
Page({
  data: {
    canIUse: wx.canIUse('button.open-type.getUserInfo'),
    sq_show: false,
    user_info: '',
    height : 0,
    width: 0,
    topshow : false,
    ss_yx : false,
    scroll_top:0,
    ss_text : '',
    ss_input : '',
    list: ''
  },
 
  //事件处理函数
  bindViewTap: function() {
    wx.navigateTo({
      url: '../logs/logs'
    })
  },
  // 点击进入商品详情
  list_click : function(e){
    console.log(e.currentTarget.dataset.id)
    wx.navigateTo({
      url: '../info/info?id=' + e.currentTarget.dataset.id
    })
  },
  // 点击搜索框
  ss_input:function(){
    this.setData({
      ss_yc : true,
      ss_text: 1
    })
  },
  //当搜索框输入时事件
  bind_ss_input: function (e) {
    var _this = this;
  },
  // 搜索确实时
  bind_ss_confirm : function(e){
    var _this = this;
    console.log(e.detail.value)
  },
  //搜索框点击X取消事件
  ss_x: function () {
    this.setData({
      ss_yc: false,
      ss_text: '',
      ss_input : ''
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
  handletap :function(){
    this.setData({
      scroll_top : 0
    })
  },

  // 用户点击授权登录
  bindGetUserInfo: function (e) {
    app.login(this)
    if(e.detail && e.detail.rawData){
      this.setData({ sq_show: false })
    }
  },

  //滚动到底部加载数据
  lower_load : function(){
    console.log('底部')
  },
  
  // 页面加载
  onLoad: function () {
    var _this = this;


    // 获取首页数据
    wx.request({
      url: app.http +'api/shoplist',
      method: 'GET',
      data: {
        p: 1,
        mix_kw : ''
      },
      header: { "Content-Type": "application/x-www-form-urlencoded" },
      dataType: 'json',
      success: function (r) {
        if(r.data.code == 200){
          _this.setData({
            list: r.data.data.list
          })
        }
      }
    });

     //取出用户微信信息
      wx.getStorage({
        key: 'user_info',
        success: function(res) {

          _this.setData({
            user_info : res
          })
        },
        // 获取失败说明没授权 打开授权提示框
        fail: function () {
          _this.setData({
            sq_show: true
          })
        }
    })

    var _this = this;
    // 获取屏幕可见区域
    wx.getSystemInfo({
      success: function (res) {
        _this.setData({
          height: res.windowHeight+'px',
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
    } else if (this.data.canIUse){
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
  getUserInfo: function(e) {
    app.globalData.userInfo = e.detail.userInfo
    this.setData({
      userInfo: e.detail.userInfo,
      hasUserInfo: true
    })
  },
})
