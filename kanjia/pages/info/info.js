// pages/info/info.js
Page({

  /**
   * 页面的初始数据
   */
  data: {
    height: 0,
    width: 0,
    img_w:0,
    kj_box: false,
    scroll_top: 0
  },


  //点击砍价
  kanjia:function(){
    this.setData({
      kj_box : true
    })
  } ,
  // 点击购买
  goumai : function(){
    wx.requestPayment({
      timeStamp: '',
      nonceStr: '',
      package: '',
      signType: 'MD5',
      paySign: '',
      success(res) { },
      fail(res) { }
    })
  },

  //点击关闭
  close : function(){
    this.setData({
      kj_box: false
    })
  } ,

  //转发
  onShareAppMessage: function () {
    return {
      title: '你的标题',
      path: '/pages/index/index',
      // imageUrl: '转发的图片，不填的话  就是页面截图',
    }
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
          height: res.windowHeight + 'px',
          width: res.windowWidth + 'px',
          img_w: res.windowWidth-50+'px'
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