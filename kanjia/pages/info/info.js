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
    openid: '',
    token: '',
    height: 0,
    width: 0,
    img_w: 0,
    kj_box: false,
    scroll_top: 0,
    list: '',
    pic_id: '',
    price: 0,
    name: '',
    desc: '',
    pic_url: '',
    stock: 0,
    shop_info: '',
    coupon : 0
  },


  //点击砍价
  kanjia: function () {
    console.log(this.data.coupon)
    if(this.data.coupon == 1){
      wx.showToast({
        title: '已是砍价商品',
        icon: 'success',
        duration: 2000,
        success : function(){
         
        }
      })
      setTimeout(function(){
        wx.switchTab({
          url: '../user/user',
        })
      },2000)
    }else{
      this.setData({
        kj_box: true
      })
    }

  },
  // 点击购买
  goumai: function () {
    var _this = this;
    wx.showLoading({
      title: '正在生成订单',
    });
    // console.log(_this.data.shop_info)
    wx.request({
      url: app.http + 'api/order/create',
      method: 'POST',
      header: app.getRequestHeader(),
      data: { 'openId': _this.data.openid, 'goods': JSON.stringify(_this.data.shop_info) },
      success: function (res) {
        if(res.data.code == 200){
          wx.switchTab({
            url: '../user/user',
          })
          wx.setStorageSync('url', 'kj_list_info')
        }else{
          wx.showToast({
            title: res.data.msg,
            icon: 'none',
            duration: 2000
          })
        }
      }
    })
  },

  //点击关闭
  close: function () {
    this.setData({
      kj_box: false
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
      token: app.getCache('token'),
      pic_id: options.id,
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



    // 获取详情
    wx.request({
      url: app.http + 'api/shopinfo?id=' + options.id,
      method: 'GET',
      data: {},
      header: app.getRequestHeader(),
      dataType: 'json',
      success: function (r) {
        if (r.data.code == 200) {
          _this.setData({
            price: r.data.data.price,
            name: r.data.data.name,
            desc: r.data.data.desc,
            pic_url: r.data.data.pic_url,
            stock: r.data.data.stock,
            shop_info: r.data.data,
            coupon : r.data.coupon
          })
        }
      }
    });

    wx.showShareMenu({
      withShareTicket: true
    });
    // 获取小程序启动时的参数
    // console.log(wx.getLaunchOptionsSync())

    _this.setData({
      openid: app.getCache('openid')
    })


    // 获取屏幕可见区域
    wx.getSystemInfo({
      success: function (res) {
        _this.setData({
          height: res.windowHeight + 'px',
          width: res.windowWidth + 'px',
          img_w: res.windowWidth - 50 + 'px'
        })
      },
    })
  },


  //转发
  onShareAppMessage: function () {
    var _this = this;
    var shopId = _this.data.pic_id;
    var toOpenId = _this.data.openid;
    var avatarUrl = _this.data.user_info.avatarUrl ;
    var nickName = _this.data.user_info.nickName;
    return {
      title: '快来帮我砍一刀！' + _this.data.name,
      imageUrl : _this.data.pic_url,
      path: '/pages/info/info?id=' + _this.data.pic_id + '&open_id=' + _this.data.openid,
      success: function (res) {
        _this.onLoad()
        console.log('分享成功' + _this.data.pic_id + _this.data.openid)
        // 获取详情
        wx.request({
          url: app.http + 'api/member/share',
          method: 'POST',
          data: {
            url: '/pages/info/info',
            shopId: shopId,
            toOpenId: toOpenId,
            avatarUrl: avatarUrl,
            nickName: nickName
          },
          header: app.getRequestHeader(),
          dataType: 'json',
          success: function (r) {
            if (r.data.code == 200) {
              console.log('回调成功' + r.data)
            }
          }
        });
      },
      fail: function (res) {
        console.log('失败' + res)
      }
    }
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

})