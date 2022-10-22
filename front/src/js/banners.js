
function Banners() {

}

/**
 * 加载数据
 */
Banners.prototype.loadData = function () {
    var self = this;
    myajax.get({
        'url': '/cms/banner_list/',
        'success': function (result) {
            if(result['code'] === 200){
                var banners = result['data'];
                console.log(banners);
                for(var i=0; i<banners.length;i++){
                    var banner = banners[i];
                    self.createBannerItem(banner);
                }
            }
        }
    });
};
/**
 * 添加轮播图到容器中并绑定点击事件
 * @param banner
 */
Banners.prototype.createBannerItem = function (banner) {
    var self = this;
    var tpl = template("banner-item",{"banner":banner});
    var bannerListGroup = $(".banner-list-group");

    var bannerItem = null;
    if(banner){
        bannerListGroup.append(tpl);
        bannerItem = bannerListGroup.find(".banner-item:last");
    }else{
        bannerListGroup.prepend(tpl);
        bannerItem = bannerListGroup.find(".banner-item:first");
    }
    self.addImageSelectEvent(bannerItem);
    self.addRemoveBannerEvent(bannerItem);
    self.addSaveBannerEvent(bannerItem);
};

/**
 * 添加轮播图
 */
Banners.prototype.listenAddBannerEvent = function () {
    var self = this;
    var addBtn = $("#add-banner-btn");
    addBtn.click(function () {
        var bannerListGroup = $('.banner-list-group');
        var length = bannerListGroup.children().length;
        if(length >= 6){
            window.messageBox.showInfo('最多只能添加6张轮播图！');
            return;
        }
        self.createBannerItem();
    });
};
/**
 * 给略缩图添加点击事件，打开文件选择器
 * @param bannerItem
 */
Banners.prototype.addImageSelectEvent = function (bannerItem) {
    var image = bannerItem.find('.thumbnail');
    var imageInput = bannerItem.find('.image-input');
    // 图片是不能够打开文件选择框的，只能通过input[type='file']
    image.click(function () {
        imageInput.click();
    });

    imageInput.change(function () {
        var file = this.files[0];
        var formData = new FormData();
        formData.append("file",file);
        myajax.post({
            'url': '/cms/upload_file/',
            'data': formData,
            'processData': false,
            'contentType': false,
            'success': function (result) {
                if(result['code'] === 200){
                    var url = result['data']['url'];
                    image.attr('src',url);
                }
            }
        });
    });
};


/**
 * 删除轮播图功能
 * @param bannerItem
 */
Banners.prototype.addRemoveBannerEvent = function (bannerItem) {
    var closeBtn = bannerItem.find('.close-btn');

    closeBtn.click(function () {
        var bannerId = bannerItem.attr('data-banner-id');
        if(bannerId){//在模板中如果该轮播图是存在于数据库中，则绑定了bannerId
            myalert.alertConfirm({
                'text': '您确定要删除这个轮播图吗?',
                'confirmCallback': function () {
                    myajax.post({
                        'url': '/cms/delete_banner/',
                        'data': {
                            'banner_id': bannerId
                        },
                        'success': function (result) {
                            if(result['code'] === 200){
                                bannerItem.remove();
                                window.messageBox.showSuccess('轮播图删除才成功！');
                            }
                        }
                    });
                }
            });
        }else{
            bannerItem.remove();
        }
    });
};

/**
 * 保存轮播图到数据库
 * @param bannerItem
 */
Banners.prototype.addSaveBannerEvent = function (bannerItem) {
    var saveBtn = bannerItem.find('.save-btn');
    var imageTag = bannerItem.find(".thumbnail");
    var priorityTag = bannerItem.find("input[name='priority']");
    var linktoTag = bannerItem.find("input[name='link_to']");
    var prioritySpan = bannerItem.find('span[class="priority"]');
    var bannerId = bannerItem.attr("data-banner-id");
    var url = '';
    if(bannerId){//bannerId存在表明数据库中有该条数据，本次操作为修改；如果没有，本次操作为添加
        url = '/cms/edit_banner/';
    }else{
        url = '/cms/add_banner/';
    }
    saveBtn.click(function () {
        var image_url = imageTag.attr('src');
        var priority = priorityTag.val();
        var link_to = linktoTag.val();
        myajax.post({
            'url': url,
            'data':{
                'image_url': image_url,
                'priority': priority,
                'link_to': link_to,
                'pk': bannerId
            },
            'success': function (result) {
                if(result['code'] === 200){
                    if(bannerId){
                        window.messageBox.showSuccess('轮播图修改成功！');
                    }else{
                        bannerId = result['data']['banner_id'];
                        bannerItem.attr('data-banner-id',bannerId);
                        window.messageBox.showSuccess('轮播图添加完成！');
                    }
                    prioritySpan.text("优先级："+priority);
                }
            }
        });
    });
};

Banners.prototype.run = function () {
    this.listenAddBannerEvent();
    this.loadData();
};

$(function () {
    var banners = new Banners();
    banners.run();
});