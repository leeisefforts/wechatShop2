//app.js
App({
  http: 'https://17bctech.com/',
  user_info : '',
  code : '',
  onLaunch: function (option) {
    
    var _this = this
    // 展示本地存储能力
    var logs = wx.getStorageSync('logs') || []
    logs.unshift(Date.now())
    wx.setStorageSync('logs', logs)
  },
  onShow: function (option){
    console.log('小程序进来的参数：', option)
  },
  globalData: {
    userInfo: null
  },


  getRequestHeader: function () {
    return {
      'content-type': 'application/x-www-form-urlencoded',
      'Authorization': this.getCache("token")
    }
  },
  buildUrl: function (path, params) {
    var url = this.globalData.domain + path;
    var _paramUrl = "";
    if (params) {
      _paramUrl = Object.keys(params).map(function (k) {
        return [encodeURIComponent(k), encodeURIComponent(params[k])].join("=");
      }).join("&");
      _paramUrl = "?" + _paramUrl;
    }
    return url + _paramUrl;
  },
  getCache: function (key) {
    var value = undefined;
    try {
      value = wx.getStorageSync(key);
    } catch (e) {
    }
    return value;
  },
  setCache: function (key, value) {
    wx.setStorage({
      key: key,
      data: value
    });
  },
  //用户点击授权登陆调用函数
  login:function(that){
    var _this = this;
    // 获取用户信息
    wx.getSetting({
      success: res => {

        if (res.authSetting['scope.userInfo']) {
          // 已经授权，可以直接调用 getUserInfo 获取头像昵称
          wx.getUserInfo({
            success: res => {
              // 可以将 res 发送给后台解码出 unionId
              //写入用户微信信息
              var user_info = res.userInfo;
              // 登录
              wx.login({
                success: res => {
                  // 发送 res.code 到后台换取 openId, sessionKey, unionId
                  //写入用户微信信息
                  _this.code = res.code
                  wx.setStorage({
                    key: 'user_code',
                    data: res.code,
                  })
                  wx.request({
                    url: _this.http + '/api/member/login',
                    method: 'GET',
                    data: {
                      code: _this.code,
                      nickName: user_info.nickName,
                      gender: user_info.gender,
                      avatarUrl: user_info.avatarUrl,
                      city: user_info.city
                    },
                    header: getApp().getRequestHeader(),
                    dataType: 'json',
                    success: function (r) {
                      if (r.data.code == 200) {
                        _this.setCache('token', r.data.data.token)
                        _this.setCache('openid', r.data.data.openId)
                        _this.setCache('user_info', user_info)
                      } else {
                        wx.showToast({
                          title: '请注册后登录',
                          icon: 'none',
                        })
                      }
                    }
                  })
                }
              })

              // 由于 getUserInfo 是网络请求，可能会在 Page.onLoad 之后才返回
              // 所以此处加入 callback 以防止这种情况
              if (this.userInfoReadyCallback) {
                this.userInfoReadyCallback(res)
              }
            }
          })
        }
      }
    })

  
  }
})