
function CMSNewsList() {

}

CMSNewsList.prototype.initDatePicker = function () {
    var startPicker = $("#start-picker");
    var endPicker = $("#end-picker");

    var todayDate = new Date();
    var todayStr = todayDate.getFullYear() + '/' + (todayDate.getMonth()+1) + '/' + todayDate.getDate();
    var options = {
        'showButtonPanel': true,
        'format': 'yyyy/mm/dd',
        'startDate': '2017/6/1',
        'endDate': todayStr,
        'language': 'zh-CN',
        'todayBtn': 'linked',
        'todayHighlight': true,
        'clearBtn': true,
        'autoclose': true
    };
    startPicker.datepicker(options);
    endPicker.datepicker(options);
};

CMSNewsList.prototype.listenDeleteEvent = function () {
    var deleteBtns = $(".delete-btn");
    deleteBtns.click(function () {
        var btn = $(this);
        var goods_id = btn.attr('data-goods-id');
        myalert.alertConfirm({
            'text': '您是否要删除这篇新闻吗？',
            'confirmCallback': function () {
                myajax.post({
                    'url': '/cms/delete_goods/',
                    'data': {
                        'goods_id': goods_id
                    },
                    'success': function (result) {
                        if(result['code'] === 200){
                            window.location = window.location.href; //刷新浏览器
                            // window.location.reload()
                        }
                    }
                });
            }
        });
    });
};


CMSNewsList.prototype.run = function () {
    this.initDatePicker();
    this.listenDeleteEvent();
};

$(function () {
    var newsList = new CMSNewsList();
    newsList.run();
});