// pages/tixian/tixian.js
const app = getApp()
Page({

  /**
   * 页面的初始数据
   */
  data: {
    tx_je : '',
    skm_img : '',
    skm_img_url: '',
    height: 0,
    width: 0,
    merchantId : ''
  },

  // 提现金额
  tx_je: function (e) {
    this.setData({
      tx_je: e.detail.value
    })
  },

  // 上传收款码
  skm_img: function () {
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
            if (obj.code == 200) {
              _this.setData({
                skm_img_url: app.http + 'static/upload/' + obj.data
              })
            }
          }
        })

      }
    })
  },

  // 点击提交
  sj_tj_bind: function () {
    var _this = this;
    if (_this.data.tx_je == '') {
      wx.showToast({
        title: '请输入提现金额',
        image: '../../img/x.png',
        duration: 2000
      })
      return false;
    } 
    else if (_this.data.skm_img_url == '') {
      wx.showToast({
        title: '请上传收款码',
        image: '../../img/x.png',
        duration: 2000
      })
      return false;
    } 
    else {
      wx.showLoading({
        title: '提交中',
      })
      wx.request({
        url: app.http + 'api/receipt',
        method: 'POST',
        data: {
          merchantId: _this.data.merchantId,
          balance: _this.data.tx_je,
          receipt_qrcode: _this.data.skm_img_url
        },
        header: app.getRequestHeader(),
        dataType: 'json',
        success: function (r) {
          if (r.data.code == 200) {
            wx.hideLoading()
            wx.showToast({
              title: '提现成功',
              icon: 'success',
              duration: 2000
            })
          }
        }
      });
    }

  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    var _this = this;
    _this.setData({
      merchantId : options.merchantId
    })
    // 获取屏幕可见区域
    wx.getSystemInfo({
      success: function (res) {
        _this.setData({
          height: res.windowHeight + 'px',
          width: (res.windowWidth - 50) + 'px'
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