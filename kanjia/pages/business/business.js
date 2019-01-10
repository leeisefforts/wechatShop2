// pages/business/business.js
//获取应用实例
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
    iphone_value : '',
    iphone_length : 0,
    name_length: 0,
    name_value: '',
    add_length: 0,
    add_value: '',
    height: 0,
    width: 0,
    set_img : '',
    sj:0,
    data_name :'',
    data_phone : '',
    data_address : '',
    data_imageUrl : '',
    button_show : true,
    input_disabled : false,
    sp_list : '',
    sp_list_size : 0,
    sqsh_show : true,
    shzx_show : false,
    merchantId : '',
    dqyue : '0',
    today_order_count: '0',
    total_order_count : '0',
    receipt_count: '0',
    coupon_count :'0'
  },

  // 姓名
  name_length: function (e) {
    this.setData({
      name_length: e.detail.value.length,
      name_value: e.detail.value
    })
  },
  // 手机号
  iphone_length : function(e){
    this.setData({
      iphone_length: e.detail.value.length,
      iphone_value: e.detail.value
    })
  },
  // 地址
  add_length: function (e) {
    this.setData({
      add_length: e.detail.value.length,
      add_value: e.detail.value
    })
  },
  // 点击提交
  sj_tj_bind : function(){
    var _this = this;
    if (this.data.name_length < 1) {
      wx.showToast({
        title: '请输入店名',
        image: '../../img/x.png',
        duration: 2000
      })
      return false;
    } else if (this.data.iphone_length < 1){
      wx.showToast({
        title: '请输入电话',
        image: '../../img/x.png',
        duration: 2000
      })
      return false;
    } else if (this.data.add_length < 1) {
      wx.showToast({
        title: '请输入地址',
        image: '../../img/x.png',
        duration: 2000
      })
      return false;
    } 
     else if (this.data.set_img == '') {
      wx.showToast({
        title: '请上传图片',
        image: '../../img/x.png',
        duration: 2000
      })
      return false;
    }
    else{
      wx.showLoading({
        title: '提交中',
      })
      wx.request({
        url: app.http + 'api/addmerchant',
        method: 'GET',
        data: {
          id: _this.data.sj,
          name: _this.data.name_value,
          phone: _this.data.iphone_value,
          address: _this.data.add_value,
          imageUrl: _this.data.set_img,
          openId: _this.data.openid,
        },
        header: app.getRequestHeader(),
        dataType: 'json',
        success: function (r) {
          if (r.data.code == 200) {
            wx.hideLoading()
            wx.showToast({
              title: '提交成功',
              icon: 'success',
              duration: 2000
            })
            _this.setData({
              button_show : false,
              input_disabled : true
            })
          }
        }
      });
    }
    
  },
  // 上传图片
  add_img : function(){
    var _this = this;
    wx.chooseImage({
      count: 1,
      sizeType: ['compressed'],
      sourceType: ['album', 'camera'],
      success(res) {
        // 上传
        wx.uploadFile({
          url: app.http + 'api/upload',
          filePath: res.tempFilePaths[0],
          name: 'pic',
          success(res) {
            var obj = JSON.parse(res.data)
            if (obj.code == 200){
              _this.setData({
                set_img: app.http + 'static/upload/' +obj.data
              })
            }
          }
        })
      
      }
    })
  },


  // 用户点击授权登录
  bindGetUserInfo: function (e) {
    app.login(this)
    if (e.detail && e.detail.rawData) {
      this.setData({ sq_show: false })
    }
  },

  // 提现
  tixian: function () {
    var _this = this;
    wx.navigateTo({
      url: '../tixian/tixian?merchantId=' + _this.data.merchantId,
    })
  },

  tixian_jl: function () {
    var _this = this;
    wx.navigateTo({
      url: '../tixian_jl/tixian_jl?merchantId=' + _this.data.merchantId,
    })
  },


  //扫码
  scanCode : function(){
    var _this = this;
    wx.scanCode({
      success(res) {
        wx.showLoading({
          title: '加载中···',
        })
        wx.request({
          url: res.result,
          method: 'GET',
          data: {
            merchantId: _this.data.merchantId
          },
          header: app.getRequestHeader(),
          dataType: 'json',
          success: function (r) {
            wx.hideLoading()
            if (r.data.code == 200) {
              _this.setData({
                
              })
            }
          }
        });
      }
    })
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
    setTimeout(function () {
      if (_this.data.token == '') {
        _this.setData({
          sq_show: true
        })
      } else {
        _this.setData({
          sq_show: false
        })
      }
    }, 2000)
    // 获取屏幕可见区域
    wx.getSystemInfo({
      success: function (res) {
        _this.setData({
          height: res.windowHeight + 'px',
          width: res.windowWidth + 'px'
        })
      },
    })

    wx.showLoading({
      title: '加载中···',
    })
      //获取数据
    if (_this.data.openid){
      wx.request({
        url: app.http + 'api/merchant/info',
        method: 'GET',
        data: {
          id: _this.data.openid
        },
        header: app.getRequestHeader(),
        dataType: 'json',
        success: function (r) {
          wx.hideLoading()
          if (r.data.code == 200) {
            _this.setData({
              data_name: r.data.data.name || _this.data.name_value,
              data_phone: r.data.data.phone || _this.data.iphone_value,
              data_address: r.data.data.address || _this.data.add_value,
              data_imageUrl: r.data.data.imageUrl || _this.data.set_img,
              sp_list: r.data.shop_list,
              sp_list_size: r.data.shop_list.length,
              dqyue: (parseInt(r.data.data.freezeBalance) + parseInt(r.data.data.totalBalance)).toFixed(2),
              today_order_count: r.data.data.today_order_count,
              total_order_count: r.data.data.total_order_count,
              receipt_count: r.data.data.receipt_count,
              coupon_count: r.data.data.coupon_count
            })
             //显示商户中心
            if (r.data.data.name) {
              wx.setNavigationBarTitle({
                title : '商户中心'
              })
              _this.setData({
                sqsh_show : false,
                shzx_show : true
              })
            }
          }
          if (r.data.data.name) {
            _this.setData({
              button_show: false,
              input_disabled: true
            })
          }
        }
      });
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

    var _this = this;
    //显示商户中心
    if (_this.data.data_name) {
      wx.setNavigationBarTitle({
        title: '商户中心'
      })
      _this.setData({
        sqsh_show: false,
        shzx_show: true
      })
    }
    _this.setData({
      openid: app.getCache('openid'),
      token: app.getCache('token')
    })
    // 判断是否授权登陆过
    setTimeout(function () {
      if (_this.data.token == '') {
        _this.setData({
          sq_show: true
        })
      } else {
        _this.setData({
          sq_show: false
        })
      }
    }, 2000)


    //获取数据
    if (_this.data.openid) {
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
              data_name: r.data.data.name || _this.data.name_value,
              data_phone: r.data.data.phone || _this.data.iphone_value,
              data_address: r.data.data.address || _this.data.add_value,
              data_imageUrl: r.data.data.imageUrl || _this.data.set_img,
              merchantId: r.data.data.id
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
    }

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