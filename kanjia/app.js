//app.js
App({
  http: 'http://www.17bctech.com/api/',
  user_info : '',
  code : '',
  token : '',
  onLaunch: function () {
    var _this = this
    // 展示本地存储能力
    var logs = wx.getStorageSync('logs') || []
    logs.unshift(Date.now())
    wx.setStorageSync('logs', logs)

    // // 获取用户信息
    // wx.getSetting({
    //   success: res => {
       
    //     if (res.authSetting['scope.userInfo']) {
    //       // 已经授权，可以直接调用 getUserInfo 获取头像昵称
    //       wx.getUserInfo({
    //         success: res => {
    //           // 可以将 res 发送给后台解码出 unionId
    //           //写入用户微信信息
    //           _this.user_info = res.userInfo;
    //           wx.setStorage({
    //             key: 'user_info',
    //             data: res.userInfo,
    //           })

    //           // 由于 getUserInfo 是网络请求，可能会在 Page.onLoad 之后才返回
    //           // 所以此处加入 callback 以防止这种情况
    //           if (this.userInfoReadyCallback) {
    //             this.userInfoReadyCallback(res)
    //           }
    //         }
    //       })
    //     }
    //   }
    // })

    // // 登录
    // wx.login({
    //   success: res => {
    //     // 发送 res.code 到后台换取 openId, sessionKey, unionId
    //     //写入用户微信信息
    //     _this.code = res.code
    //     wx.setStorage({
    //       key: 'user_code',
    //       data: res.code,
    //     })
    //     wx.getStorage({
    //       key: 'user_info',
    //       success: function (res) {
    //         _this.user_info = res
    //         wx.request({
    //           url: _this.http + 'member/login',
    //           method: 'GET',
    //           data: {
    //             code: _this.code,
    //             nickName: res.data.nickName,
    //             gender: res.data.gender,
    //             avatarUrl: res.data.avatarUrl,
    //             city: res.data.city
    //           },
    //           header: { "Content-Type": "application/x-www-form-urlencoded" },
    //           dataType: 'json',
    //           success: function (r) {
    //             if (r.data.code == 200) {
    //               _this.token = r.data.data.token;
    //             } else {
    //               wx.showToast({
    //                 title: '请注册后登录',
    //                 icon: 'none',
    //               })
    //             }
    //           }
    //         })
    //       },
    //     })
    //   }
    // })
  },
  globalData: {
    userInfo: null
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
              _this.user_info = res.userInfo;
              wx.setStorage({
                key: 'user_info',
                data: res.userInfo,
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
        wx.getStorage({
          key: 'user_info',
          success: function (res) {
            _this.user_info = res
            wx.request({
              url: _this.http + 'member/login',
              method: 'GET',
              data: {
                code: _this.code,
                nickName: res.data.nickName,
                gender: res.data.gender,
                avatarUrl: res.data.avatarUrl,
                city: res.data.city
              },
              header: { "Content-Type": "application/x-www-form-urlencoded" },
              dataType: 'json',
              success: function (r) {
                if (r.data.code == 200) {
                  _this.token = r.data.data.token;
                } else {
                  wx.showToast({
                    title: '请注册后登录',
                    icon: 'none',
                  })
                }
              }
            })
          },
        })
      }
    })
  }
})