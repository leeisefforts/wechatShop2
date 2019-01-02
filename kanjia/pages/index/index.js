//index.js
//获取应用实例
const app = getApp()
Page({
  data: {
    canIUse: wx.canIUse('button.open-type.getUserInfo'),
    sq_show: false,
    user_info: '',
    openid : '',
    token : '',
    height : 0,
    w_width : 0,
    width: 0,
    topshow : false,
    ss_yx : false,
    scroll_top:0,
    ss_text : '',
    ss_input : '',
    list: '',
    page : 1,
    p_page :2,
    ss_page : 1,
    con_show : true
  },
 
  //事件处理函数
  bindViewTap: function() {
    wx.navigateTo({
      url: '../logs/logs'
    })
  },
  // 点击进入商品详情
  list_click : function(e){
    wx.navigateTo({
      url: '../info/info?id=' + e.currentTarget.dataset.id
    })
  },
  // 点击搜索框
  ss_input:function(){
    this.setData({
      ss_yc : true,
      ss_text: 1,
      con_show : false
    })
  },
  //当搜索框输入时事件
  bind_ss_input: function (e) {
    var _this = this;
  },
  // 搜索确实时
  bind_ss_confirm : function(e){

    var _this = this;

    // 获取数据
    wx.request({
      url: app.http + 'api/shoplist',
      method: 'GET',
      data: {
        p: _this.data.ss_page,
        mix_kw: e.detail.value
      },
      header: app.getRequestHeader(),
      dataType: 'json',
      success: function (r) {
        if (r.data.code == 200) {
          if (r.data.data.list.length > 0){
            
            _this.setData({
              list: r.data.data.list,
              ss_yc: false,
              con_show: true
            })
          }else{
            wx.showToast({
              title: '没有数据',
              icon: 'none',
              duration: 2000
            })
          }
        }

      }
    });
  },
  //搜索框点击X取消事件
  ss_x: function () {
    var _this = this;
    _this.setData({
      ss_yc: false,
      ss_text: '',
      ss_input : '',
      con_show: true
    })

    // 获取首页数据
    wx.request({
      url: app.http + 'api/shoplist',
      method: 'GET',
      data: {
        p: _this.data.page,
        mix_kw: ''
      },
      header: app.getRequestHeader(),
      dataType: 'json',
      success: function (r) {
        if (r.data.code == 200) {
          _this.setData({
            list: r.data.data.list,
          })
        }

      }
    });
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

  //滚动到底部加载数据
  lower_load: function () {
    var _this = this;
    // 获取首页数据
    wx.request({
      url: app.http + 'api/shoplist',
      method: 'GET',
      data: {
        p: _this.data.p_page,
        mix_kw: ''
      },
      header: app.getRequestHeader(),
      dataType: 'json',
      success: function (r) {
        if (r.data.code == 200) {
          _this.setData({
            list: _this.data.list.concat(r.data.data.list)
          })
          if (r.data.data.list.length > 0){
            _this.setData({
              p_page: _this.data.p_page + 1
            })
          }
        }

      }
    });
  },

  // 用户点击授权登录
  bindGetUserInfo: function (e) {
    app.login(this)
    if(e.detail && e.detail.rawData){
      this.setData({ sq_show: false })
    }
  },


  
  // 页面加载
  onLoad: function () {
    var _this = this;
    _this.setData({
      openid: app.getCache('openid'),
      token: app.getCache('token'),
      user_info: app.getCache('user_info')
    })

    // 判断是否授权登陆过
    if (_this.data.token == '') {
      _this.setData({
        sq_show: true
      })
    } else {
      _this.setData({
        sq_show: false
      })
    }

    // 获取首页数据
    wx.request({
      url: app.http +'api/shoplist',
      method: 'GET',
      data: {
        p: _this.data.page,
        mix_kw : ''
      },
      header: app.getRequestHeader(),
      dataType: 'json',
      success: function (r) {
        if(r.data.code == 200){
          _this.setData({
            list: r.data.data.list,
          })
        }

      }
    });

    var _this = this;
    // 获取屏幕可见区域
    wx.getSystemInfo({
      success: function (res) {
        _this.setData({
          height: res.windowHeight+'px',
          width: res.windowWidth + 'px',
          w_width: (res.windowWidth - 40) + 'px',
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

  //转发
  onShareAppMessage: function () {
   
  },


  getUserInfo: function(e) {
    app.globalData.userInfo = e.detail.userInfo
    this.setData({
      userInfo: e.detail.userInfo,
      hasUserInfo: true
    })
  },

})
