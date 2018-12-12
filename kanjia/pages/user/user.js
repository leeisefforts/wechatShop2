// pages/user/user.js
Page({

  /**
   * 页面的初始数据
   */
  data: {
    height: 0,
    topshow: false,
    nav1: 'nav_click',
    nav2: '',
    nav3: '',
    scroll_top: 0
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
  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    var _this = this;
    // 获取屏幕可见区域
    wx.getSystemInfo({
      success: function (res) {
        _this.setData({
          height: res.windowHeight + 'px'
        })
        console.log(res.windowHeight);
      },
    })
  },

  // 点击导航
  nav1: function () {
    wx.showLoading({
      title: '加载中···',
    })
    var _this = this;
    _this.setData({
      nav1: 'nav_click',
      nav2: '',
      nav3: '',
    });
    wx.hideLoading();
  },
  nav2: function () {
    wx.showLoading({
      title: '加载中···',
    })
    var _this = this;
    _this.setData({
      nav1: '',
      nav2: 'nav_click',
      nav3: '',
    });
    wx.hideLoading();
  },
  nav3: function () {
    wx.showLoading({
      title: '加载中···',
    })
    var _this = this;
    _this.setData({
      nav1: '',
      nav2: '',
      nav3: 'nav_click',
    });
    wx.hideLoading();
  },
  // 点击进入商品详情
  list_click: function () {
    wx.navigateTo({
      url: '../info/info'
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