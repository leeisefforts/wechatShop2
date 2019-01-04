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
    price: 0,
    name: '',
    desc: '',
    pic_url: '',
    stock: 0,
    shop_info: '',
    order_sn : '',
    qrCode_Url : '',
    status: '',
    data_name: '',
    data_phone: '',
    data_address: '',
    data_imageUrl: ''
  },

  // 点击购买
  goumai: function () {
    var _this = this;
    wx.showLoading({
      title: '加载中',
    });
    wx.request({
      url: app.http + 'api/order/pay',
      method: 'POST',
      data: {
        order_sn: _this.data.order_sn
      },
      header: app.getRequestHeader(),
      dataType: 'json',
      success: function (r) {
        if (r.data.code == 200) {
          wx.hideLoading()
          wx.requestPayment({
            timeStamp: r.data.data.pay_info.timeStamp,
            nonceStr: r.data.data.pay_info.nonceStr,
            package: r.data.data.pay_info.package,
            signType: 'MD5',
            paySign: r.data.data.pay_info.paySign,
            success(res) {
              wx.showToast({
                title: '支付成功',
                icon: 'success',
                duration: 2000
              })
             },
            fail(res) {
             }
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

  //拨打商家电话
  PhoneCall: function () {
    console.log(this.data.data_phone)
    var phone = this.data.data_phone
    wx.makePhoneCall({
      phoneNumber: phone // 仅为示例，并非真实的电话号码
    })
  },

  //去首页
  home: function () {
    wx.switchTab({
      url: '../index/index',
    })
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    var _this = this;

    _this.setData({
      openid: app.getCache('openid'),
      token: app.getCache('token'),
      user_info: app.getCache('user_info'),
      order_sn: options.ordersn
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
      url: app.http + 'api/order/info',
      method: 'POST',
      data: {
        order_sn: options.ordersn
      },
      header: app.getRequestHeader(),
      dataType: 'json',
      success: function (r) {
        if (r.data.code == 200) {
          _this.setData({
            name: r.data.data.info.goods[0].name,
            pic_url: r.data.data.info.goods[0].pic_url,
            price: r.data.data.info.goods[0].price,
            qrCode_Url: r.data.data.info.qrCode_Url,
            status: r.data.data.info.status,
          })
        }
      }
    });


    //获取商家信息
    wx.request({
      url: app.http + 'api/merchant/info',
      method: 'GET',
      data: {
        id: _this.data.openid
      },
      header: app.getRequestHeader(),
      dataType: 'json',
      success: function (r) {
        if (r.data.code == 200) {
          _this.setData({
            data_name: r.data.data.name,
            data_phone: r.data.data.phone,
            data_address: r.data.data.address,
            data_imageUrl: r.data.data.imageUrl
          })
        }
        if (r.data.data.name) {
          _this.setData({
            button_show: false,
            input_disabled: true
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