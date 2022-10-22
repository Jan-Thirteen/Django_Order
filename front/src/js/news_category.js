/**
 * Created by hynev on 2018/7/2.
 */

function GoodsCategory() {

};

GoodsCategory.prototype.run = function () {
    var self = this;
    self.listenAddCategoryEvent();
    self.listenEditCategoryEvent();
    self.listenDeleteCategoryEvent();
};

GoodsCategory.prototype.listenAddCategoryEvent = function () {
    var addBtn = $('#add-btn');
    addBtn.click(function () {
        myalert.alertOneInput({
            'title': '添加新品分类',
            'placeholder': '请输入新品分类名称',
            'confirmCallback': function (inpuValue) {
                myajax.post({
                    'url': '/cms/add_goods_category/',
                    'data': {
                        'name': inpuValue
                    },
                    'success': function (result) {
                        if(result['code'] === 200){
                            console.log(result);
                            window.location.reload();
                        }else{
                            myalert.close();
                        }
                    }
                });
            }
        });
    });
};

GoodsCategory.prototype.listenEditCategoryEvent = function () {
    console.log("run");
    var self = this;
    var editBtn = $(".edit-btn");
    editBtn.click(function () {
        var currentBtn = $(this);
        var tr = currentBtn.parent().parent();
        var pk = tr.attr('data-pk');
        var name = tr.attr('data-name');
        myalert.alertOneInput({
            'title': '修改分类名称',
            'placeholder': '请输入新的分类名称',
            'value': name,
            'confirmCallback': function (inputValue) {
                myajax.post({
                    'url': '/cms/edit_goods_category/',
                    'data': {
                        'pk': pk,
                        'name': inputValue
                    },
                    'success': function (result) {
                        if(result['code'] === 200){
                            window.location.reload();
                        }else{
                            myalert.close();
                        }
                    }
                });
            }
        });
    });
};

GoodsCategory.prototype.listenDeleteCategoryEvent = function () {
    var deleteBtn = $(".delete-btn");
    deleteBtn.click(function () {
        var currentBtn = $(this);
        var tr = currentBtn.parent().parent();
        var pk = tr.attr('data-pk');
        myalert.alertConfirm({
            'title': '您确定要删除这个分类吗？',
            'confirmCallback': function () {
                myajax.post({
                    'url': '/cms/delete_goods_category/',
                    'data': {
                        'pk': pk
                    },
                    'success': function (result) {
                        if(result['code'] === 200){
                            window.location.reload();
                        }
                    }
                });
            }
        });
    });
};


$(function () {
    var category = new GoodsCategory();
    category.run();
});