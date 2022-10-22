
function GoodsList() {

}

GoodsList.prototype.listenSubmitEvent = function () {//发表评论按钮点击事件
    var submitBtn = $('.submit-btn');
    var textarea = $("textarea[name='comment']");
    submitBtn.click(function () {
        var content = textarea.val();
        var goods_id = submitBtn.attr('data-goods-id');//评论按钮上绑定的goodsid
        myajax.post({
            'url': '/goods/public_comment/',
            'data':{
                'content': content,
                'goods_id': goods_id
            },
            'success': function (result) {
                console.log(result);
                if(result['code'] === 200){
                    var comment = result['data'];
                    var tpl = template('comment-item',{"comment":comment});
                    var commentListGroup = $(".comment-list");
                    commentListGroup.prepend(tpl);
                    window.messageBox.showSuccess('评论发表成功！');
                    textarea.val("");//清空输入框
                }else{
                    window.messageBox.showError(resuldata-goods-idt['message']);
                }
            }
        });
    });
};

GoodsList.prototype.run = function () {
    this.listenSubmitEvent();
};


$(function () {
    var goodsList = new GoodsList();
    goodsList.run();
});