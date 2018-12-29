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
    height: 0,
    topshow: false,
    nav1: 'nav_click',
    nav2: '',
    dd_nav1: 'nav_click',
    dd_nav2: '',
    dd_nav3: '',
    scroll_top: 0,
    dd_show : '',
    kj_show: 'show',
    dd_list : '',
    kj_list : '',
    page: 1
    
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
    _this.setData({
      openid: app.getCache('openid'),
      token: app.getCache('token')
    })
    // 判断是否授权登陆过
    if (_this.data.token == ''){
      _this.setData({
        sq_show: true
      })
    }else{
      _this.setData({
        sq_show: false
      })
    }
    // 获取屏幕可见区域
    wx.getSystemInfo({
      success: function (res) {
        _this.setData({
          height: res.windowHeight + 'px'
        })
      },
    })
    //获取数据
    wx.request({
      url: app.http + 'api/coupon/list',
      method: 'GET',
      data: {
        p: _this.data.page,
        mix_kw: ''
      },
      header: app.getRequestHeader(),
      dataType: 'json',
      success: function (r) {
        if (r.data.code == 200) {
          if(r.data.data.list.length > 0){
            _this.setData({
              kj_list: r.data.data.list,
            })
          }else{
            wx.showToast({
              title: '暂时没有数据',
              icon: 'none',
              duration: 2500
            })
          }
         
        }
      }
    });

  },

  // 砍价列表
  nav1: function () {
    wx.showLoading({
      title: '加载中···',
    })
    var _this = this;
    _this.setData({
      nav1: 'nav_click',
      nav2: '',
      dd_show: '',
      kj_show: 'show'
    });
    //获取数据
    wx.request({
      url: app.http + 'api/coupon/list',
      method: 'GET',
      data: {
        p: _this.data.page,
        mix_kw: ''
      },
      header: app.getRequestHeader(),
      dataType: 'json',
      success: function (r) {
        wx.hideLoading();
        if (r.data.code == 200) {
          if (r.data.data.list.length > 0){
            _this.setData({
              kj_list: r.data.data.list
            })
          }else{
            wx.showToast({
              title: '暂时没有数据',
              icon: 'none',
              duration: 2500
            })
          }
        }
      }
    });
  },
  //订单列表
  nav2: function () {
    wx.showLoading({
      title: '加载中···',
    })
    var _this = this;
    _this.setData({
      nav1: '',
      nav2: 'nav_click',
      dd_show: 'show',
      kj_show: ''
    });
    //获取订单未完成数据
    wx.request({
      url: app.http + 'api/order/list',
      method: 'GET',
      data: {
        status : -8
      },
      header: app.getRequestHeader(),
      dataType: 'json',
      success: function (r) {
        wx.hideLoading();
        if (r.data.code == 200) {
          if (r.data.data.pay_order_list.length > 0) {
            _this.setData({
              dd_list: r.data.data.pay_order_list
            })
          } else {
            wx.showToast({
              title: '暂时没有数据',
              icon: 'none',
              duration: 2500
            })
          }
        }
      }
    });

  },

  //订单列表获取数据函数
  dd_requset: function (status) {
    var _this = this;
    //获取订单未完成数据
    wx.request({
      url: app.http + 'api/order/list',
      method: 'GET',
      data: {
        status: status
      },
      header: app.getRequestHeader(),
      dataType: 'json',
      success: function (r) {
        wx.hideLoading();
        if (r.data.code == 200) {
          if (r.data.data.pay_order_list.length > 0) {
            _this.setData({
              dd_list: r.data.data.pay_order_list
            })
          } else {
            _this.setData({
              dd_list: []
            })
            wx.showToast({
              title: '暂时没有数据',
              icon: 'none',
              duration: 2500
            })
          }
        }
      }
    });
  },


  //订单未完成
  dd_nav1 : function(){
    wx.showLoading({
      title: '加载中···',
    })
    var _this = this;
    _this.setData({
      dd_nav1: 'nav_click',
      dd_nav2: '',
      dd_nav3: '',
    });
    _this.dd_requset(-8)
  },

  //订单待使用
  dd_nav2: function () {
    wx.showLoading({
      title: '加载中···',
    })
    var _this = this;
    _this.setData({
      dd_nav1: '',
      dd_nav2: 'nav_click',
      dd_nav3: '',
    });
    //获取订单未完成数据
    _this.dd_requset(-7)
  },

  //订单已完成
  dd_nav3: function () {
    wx.showLoading({
      title: '加载中···',
    })
    var _this = this;
    _this.setData({
      dd_nav1: '',
      dd_nav2: '',
      dd_nav3: 'nav_click',
    });
    //获取数据
    _this.dd_requset(1)
  },

  // 砍价列表点击进入详情
  kj_click: function (e) {
    wx.navigateTo({
      url: '../kj_list_info/kj_list_info?id=' + e.currentTarget.dataset.id
    })
  },

  // 订单列表点击进入详情
  dd_click: function (e) {
    wx.navigateTo({
      url: '../dd_list_info/dd_list_info?ordersn=' + e.currentTarget.dataset.order_sn
    })
  },
  
  // 页面滚动监听
  //监听屏幕滚动 判断上下滚动
  onPageScroll: function (ev) {
    var _this = this;
    //当滚动的top值最大或最小时，为什么要做这一步是因为在手机实测小程序的时候会发生滚动条回弹，所以为了处理回弹，设置默认最大最小值
    if (ev.scrollTop <= 0) {
      ev.scrollTop = 0;
    } else if (ev.scrollTop > wx.getSystemInfoSync().windowHeight) {
      ev.scrollTop = wx.getSystemInfoSync().windowHeight;
    }
    //判断浏览器滚动条上下滚动
    if (ev.scrollTop > this.data.scrollTop || ev.scrollTop == wx.getSystemInfoSync().windowHeight) {
      console.log('1111')
      //向下滚动
    } else {
      //向上滚动
    }
    //给scrollTop重新赋值
    setTimeout(function () {
      _this.setData({
        scrollTop: ev.scrollTop
      })
    }, 0)
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
    console.log('000')
    var _this = this;
    var _url = wx.getStorageSync('url');
    console.log(_url)
    if(_url){
      _this.setData({
        nav1: '',
        nav2: 'nav_click',
        dd_show: 'show',
        kj_show: ''
      });
      //获取数据
      wx.request({
        url: app.http + 'api/order/list',
        method: 'GET',
        data: {
          status: -8
        },
        header: app.getRequestHeader(),
        dataType: 'json',
        success: function (r) {
          wx.removeStorageSync('url')
          if (r.data.code == 200) {
            if (r.data.data.pay_order_list.length > 0) {
              _this.setData({
                dd_list: r.data.data.pay_order_list
              })
            } else {
              wx.showToast({
                title: '暂时没有数据',
                icon: 'none',
                duration: 2500
              })
            }
          }
        }
      });
    }else{
      _this.setData({
        nav1: 'nav_click',
        nav2: '',
        dd_show: '',
        kj_show: 'show'
      });
    }
    //获取砍价列表数据
    wx.request({
      url: app.http + 'api/coupon/list',
      method: 'GET',
      data: {
        p: _this.data.page,
        mix_kw: ''
      },
      header: app.getRequestHeader(),
      dataType: 'json',
      success: function (r) {
        if (r.data.code == 200) {
          if (r.data.data.list.length > 0) {
            _this.setData({
              kj_list: r.data.data.list
            })
          } else {
            wx.showToast({
              title: '暂时没有数据',
              icon: 'none',
              duration: 2500
            })
          }
        }
      }
    });
    
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