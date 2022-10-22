function Goods() {
    this.progressGroup = $("#progress-group");
}

/**
 * 初始化ueditor
 */
Goods.prototype.initUEditor = function () {
    window.ue = UE.getEditor('editor',{
        'initialFrameHeight': 400,//设置高度
        'serverUrl': '/ueditor/upload/'
    });
};

/**
 * 上传文件到自己的服务器
 */
Goods.prototype.listenUploadFielEvent = function () {
    var uploadBtn = $('#thumbnail-btn');
    uploadBtn.change(function () {  //选择文件事件
        var file = uploadBtn[0].files[0];
        var formData = new FormData();
        formData.append('file',file);
        myajax.post({
            'url': '/cms/upload_file/',
            'data': formData,
            'processData': false,//不需要再处理
            'contentType': false,
            'success': function (result) {
                if(result['code'] === 200){
                    var url = result['data']['url'];
                    var thumbnailInput = $("#thumbnail-form");
                    thumbnailInput.val(url);
                }
            }
        });
    });
};

/**
 * 上传文件到七牛云
 */
Goods.prototype.listenQiniuUploadFileEvent = function () {
    var self = this;
    var uploadBtn = $('#thumbnail-btn');
    uploadBtn.change(function () {
        var file = this.files[0];//获取文件
        myajax.get({
            'url': '/cms/qntoken/',
            'success': function (result) {
                if(result['code'] === 200){
                    var token = result['data']['token'];
                    // a.b.jpg = ['a','b','jpg']
                    // 198888888 + . + jpg = 1988888.jpg
                    var key = (new Date()).getTime() + '.' + file.name.split('.')[1];
                    var putExtra = {
                        fname: key,
                        params:{},
                        mimeType: ['image/png','image/jpeg','image/gif','video/x-ms-wmv']//限制上传的文件类型
                    };
                    var config = {
                        useCdnDomain: true,//是否使用cdn加速
                        retryCount: 6,//重复发送请求次数
                        region: qiniu.region.z0//上传到哪一个空间
                    };
                    var observable = qiniu.upload(file,key,token,putExtra,config);
                    observable.subscribe({
                        'next': self.handleFileUploadProgress,//进度信息
                        'error': self.handleFileUploadError,//上传错误信息
                        'complete': self.handleFileUploadComplete//完成回调
                    });
                }
            }
        });
    });
};

Goods.prototype.handleFileUploadProgress = function (response) {
    var total = response.total;
    var percent = total.percent;
    var percentText = percent.toFixed(0)+'%';//toFixed(0)去掉小数
    // 24.0909，89.000....
    var progressGroup = Goods.progressGroup;//上传进度条
    progressGroup.show();
    var progressBar = $(".progress-bar");
    progressBar.css({"width":percentText});//更改进度条宽度
    progressBar.text(percentText);//设置进度条文字
};

Goods.prototype.handleFileUploadError = function (error) {
    window.messageBox.showError(error.message);
    var progressGroup = $("#progress-group");
    progressGroup.hide();
    console.log(error.message);
};

Goods.prototype.handleFileUploadComplete = function (response) {
    console.log(response);
    var progressGroup = $("#progress-group");
    progressGroup.hide();//隐藏进度条

    var domain = 'http://r9nruh1se.hd-bkt.clouddn.com/';//七牛云测试域名
    var filename = response.key;//获取文件名
    var url = domain + filename;
    var thumbnailInput = $("input[name='thumbnail']");//输入框
    thumbnailInput.val(url);//姜路径设置到输入框
};

Goods.prototype.listenSubmitEvent = function () {
    var submitBtn = $("#submit-btn");
    submitBtn.click(function (event) {
        event.preventDefault();//清除默认行为
        var btn = $(this);
        var pk = btn.attr('data-goods-id');

        var name = $("input[name='name']").val();
        var category = $("select[name='category']").val();
        var price = $("input[name='price']").val();
        // var desc = $("input[name='desc']").val();
        var thumbnail = $("input[name='thumbnail']").val();
        var content = window.ue.getContent();

        var url = '';
        if(pk){
            url = '/cms/edit_goods/';    //修改
        }else{
            url = '/cms/write_goods/';   //新增
        }

        myajax.post({
            'url': url,
            'data': {
                'name': name,
                'category': category,
                // 'desc': desc,
                'price': price,
                'thumbnail': thumbnail,
                'content': content,
                'pk': pk
            },
            'success': function (result) {
                if(result['code'] === 200){
                    myalert.alertSuccess('恭喜！新品发表成功！',function () {
                        window.location.reload();
                    });
                }
            }
        });
    });
};

Goods.prototype.run = function () {
    var self = this;
    self.initUEditor();
    // self.listenQiniuUploadFileEvent();
    self.listenSubmitEvent();
    self.listenUploadFielEvent();//上传文件到自己服务器 
};


$(function () {
    var goods = new Goods();
    goods.run();

   Goods.progressGroup = $('#progress-group');
});