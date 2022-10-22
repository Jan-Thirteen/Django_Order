function CartList() {

}

CartList.prototype.listenSwtichCartEvent = function () {
    var cart = $('.cart');
    cart.click(function () {
        console.log(111111);
        myajax.get({
            'url': '/cart/',
            'success': function (result) {
                console.log(result);
                if(result['code'] !== 200){
                    window.location.href="http://127.0.0.1:8000/";
                    window.messageBox.showError(resuldata-goods-idt['message']);
                }
            }
        });
    });
}

/**
 * 添加到购物车
 */
CartList.prototype.listenAddCartEvent = function () {//添加到购物车按钮点击事件
    var buybtn = $('.buy-btn');
    // var textarea = $("textarea[name='comment']");
    buybtn.unbind();
    buybtn.click(function () {
        // var content = textarea.val();
        var goods_id = buybtn.attr('data-goods-id');//添加到购物车按钮上绑定的goodsid
        var goods_price = buybtn.attr('data-goods-price');//添加到购物车按钮上绑定的goodsid
        myajax.get({
            'url': '/cart/add_cart/',
            'data':{
                // 'content': content,
                'goods_id': goods_id,
                'goods_price': goods_price
            },
            'success': function (result) {
                console.log(result);
                if(result['code'] === 200){
                    window.messageBox.showSuccess('添加成功！请到购物车中查看');
                }else{
                    window.messageBox.showError(resuldata-goods-idt['message']);
                }
            }
        });
    });
};

CartList.prototype.listenRemoveCartEvent = function () {
    var delbtn = $('.delete-btn');
    delbtn.unbind();
    delbtn.click(function () {
        var goods_id = delbtn.attr('data-goods-id');//添加到移除按钮上绑定的goodsid
        var order_id = delbtn.attr('data-order-id');//添加到移除按钮上绑定的order_id
        var item_id = delbtn.attr('data-id');//主键
        myajax.post({
            'url': '/cart/delete_cart/',
            'data':{
                'goods_id': goods_id,
                'order_id': order_id,
                'item_id': item_id
            },
            'success': function (result) {
                console.log(result);
                if(result['code'] === 200){
                    window.messageBox.showSuccess('移除成功');
                    window.location.reload();
                }else{
                    window.messageBox.showError(resuldata-goods-idt['message']);
                }
            }
        });
    });
};

CartList.prototype.listenCheckOutEvent = function () {
    var pays = $('.pays');
    pays.click(function () {
        var order = pays.attr('data-order');//绑定到结算按钮上的订单主键
        myajax.post({
            'url': '/cart/check_out/',
            'dataType': 'JSON',
            'data':{
                // csrfmiddlewaretoken: csrf_token,
                'order': order
            },
            'success': function (result) {
                console.log(result);
                if(result['data']['status'] === 1){
                    console.log(result['data']['url']);
                    // 跳转到支付链接
                    location.href = result['data']['url']
                    // window.messageBox.showSuccess("OK!");
                    // window.location.reload();
                }else{
                    window.messageBox.showError(resuldata-goods-idt['message']);
                }
            }
        });
    });
}

CartList.prototype.run = function () {
    this.listenAddCartEvent();
    this.listenRemoveCartEvent();
    this.listenCheckOutEvent();
    this.listenSwtichCartEvent();
};


$(function () {
    var cartList = new CartList();
    cartList.run();
});