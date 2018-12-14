// pages/info/info.js
const app = getApp()
Page({

  /**
   * 页面的初始数据
   */
  data: {
    canIUse: wx.canIUse('button.open-type.getUserInfo'),
    sq_show: false,
    user_info: '',
    height: 0,
    width: 0,
    img_w:0,
    kj_box: false,
    scroll_top: 0,
    list : '',
    openid : '',
    pic_id : '',
    shop_info: ''
  },


  //点击砍价
  kanjia:function(){

    this.setData({
      kj_box : true
    })
  } ,
  // 点击购买
  goumai : function(){
    var _this = this;
    wx.showLoading({
      title: '正在生成订单',
    });
    console.log(_this.data.shop_info)
    wx.request({
      url: 'http://127.0.0.1:5000/api/order/create',
      method: 'POST',
      header: app.getRequestHeader(),
      data: { 'openId': _this.data.openid,'goods': JSON.stringify(_this.data.shop_info)},
      success: function(res){

        wx.showLoading({
          title: '',
        }).close()
      }
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
      path: '/pages/info/info?openid = ' + this.data.openid ,
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
      pic_id : options
    });

    // 获取详情
    wx.request({
      url: 'http://127.0.0.1:5000/api/shopinfo?id=' + options.id,
      method: 'GET',
      data: { },
      header: { "Content-Type": "application/x-www-form-urlencoded" },
      dataType: 'json',
      success: function (r) {
        if (r.data.code == 200) {
          
          _this.setData({
            shop_info: r.data.data
          })
        }
      }
    });

    console.log(options)
    wx.showShareMenu({
      withShareTicket: true
    });
    // 获取小程序启动时的参数
    // console.log(wx.getLaunchOptionsSync())
    
    wx.getStorage({
      key: 'user_info',
      success: function (res) {
        _this.setData({
          openid : res.data.openid
        })
      }
    })


    // 获取数据
    wx.request({
      url: app.http + 'api/shoplist',
      method: 'GET',
      data: {
        p: 1,
        mix_kw: ''
      },
      header: { "Content-Type": "application/x-www-form-urlencoded" },
      dataType: 'json',
      success: function (r) {
        if (r.data.code == 200) {
          _this.setData({
            list: r.data.data.list
          })
        }
      }
    });

    //取出用户微信信息
    wx.getStorage({
      key: 'user_info',
      success: function (res) {
        _this.setData({
          user_info: res
        })
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