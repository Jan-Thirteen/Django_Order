// 面向对象
// 1. 添加属性
// 通过this关键字，绑定属性，并且指定他的值。
// 原型链
// 2. 添加方法
// 在Banner.prototype上绑定方法就可以了。

// function Banner() {
//     // 这个里面写的代码
//     // 相当于是Python中的__init__方法的代码
//     console.log('构造函数');
//     this.person = 'zhiliao';
// }
//
// Banner.prototype.greet = function (word) {
//     console.log('hello ',word);
// };
//
// var banner = new Banner();
// console.log(banner.person);
// banner.greet('zhiliao');

/**
 * @constructor
 */
function Banner() {
    this.bannerWidth = 798;
    this.bannerGroup = $("#banner-group");//选择轮播图最外面的大盒子
    this.index = 1;//为0则加载时第一张图会等待两次
    this.leftArrow = $(".left-arrow");//选择左右箭头
    this.rightArrow = $(".right-arrow");
    this.bannerUl = $("#banner-ul");////获取ul元素，通过id选择器找到轮播图元素
    this.liList = this.bannerUl.children("li");//获取轮播图子标签li列表
    this.bannerCount = this.liList.length;//获取有多少个轮播图
    this.pageControl = $(".page-control");//小圆点的大盒子
}

/**
 * 初始化轮播图
 * 在轮播图的ul上左边添加最后一张图，右边添加第一张图
 * 轮播图在自动播放的时候就会一直朝着同一个方向滑动
 * 在滑动到最左边或者最右边，就切换到原本第三张和第一张的位置
 */
Banner.prototype.initBanner = function () {
    var self = this;
    var firstBanner = self.liList.eq(0).clone();//获取并复制第一张轮播图
    var lastBanner = self.liList.eq(self.bannerCount-1).clone();//获取并复制最后一张
    self.bannerUl.append(firstBanner);//添加到最后面
    self.bannerUl.prepend(lastBanner);
    //修改轮播图css ul宽度 默认加载时从第一张而不是添加到最前面的那一张
    self.bannerUl.css({"width":self.bannerWidth*(self.bannerCount+2),'left':-self.bannerWidth});
};


/**
 * 动态设置轮播图小圆点
 */
Banner.prototype.initPageControl = function () {
    var self = this;

    for(var i=0; i<self.bannerCount; i++){
        var circle = $("<li></li>");//jq创建一个li标签
        self.pageControl.append(circle);//添加到pageControl
        if(i === 0){
            circle.addClass("active");
        }
    }
    self.pageControl.css({"width":self.bannerCount*12 + 8*2 + 16*(self.bannerCount-1)});//设置轮播图小圆点宽度
};

/**
 * 监听小圆点点击事件
 */
Banner.prototype.listenPageControl = function () {
    var self = this;
    self.pageControl.children("li")//获得小圆点大盒子下的所有子节点
        .each(function (index,obj) {//each遍历所有标签，obj代表li本身,$(obj)将obj包装为jq对象
        $(obj).click(function () {
            self.index = index;
            self.animate();
            // $(obj).addClass("active").//为当前点击的li标签添加active
            //     siblings().removeClass("active");//并删除其他兄弟节点的active
        });
    });
};

/**
 * 监听hover事件，鼠标移动到轮播图的展示页面时
 */
Banner.prototype.listenBannerHover = function () {
    var self = this;
    this.bannerGroup.hover(function () {
        // 第一个函数是，把鼠标移动到banner上会执行的函数
        clearInterval(self.timer);//关闭定时器,如果没有self = this;则self代表当前的function ()
        self.toggleArrow(true);
    },function () {
        // 第二个函数是，把鼠标从banner上移走会执行的函数
        self.loop();//重启定时器
        self.toggleArrow(false);
    });
};

/**
 * 自动轮播
 */
Banner.prototype.animate = function () {
    var self = this;
    self.bannerUl.stop().animate({"left":-798*self.index},500);//该方法修改css时提供过度效果,可指定过度时间
    var index = self.index;
    if (index === 0){
        index = self.bannerCount-1;
    }else if (index === self.bannerCount + 1) {
        index = 0;
    } else {
        index = self.index - 1;
    }
    self.pageControl.children("li").eq(index)//获取当前小圆点
        .addClass("active")//为当前点击的li标签添加active
        .siblings().removeClass("active");//并删除其他兄弟节点的active
};

/**
 * 轮播图滚动
 */
Banner.prototype.loop = function () {
    var self = this;
    this.timer = setInterval(function () {//定时器，间隔多久执行一次代码 this.timer将变量绑定到Banner
        if (self.index>=self.bannerCount + 1){//原本是-1，在ul的受委分别添加后，判定条件就变成了+1
            self.bannerUl.css({"left":-self.bannerWidth});//跳转到原本的第一个
            self.index = 2;
        }else{
            self.index++;
        }
        self.animate();
    },4000)
}

//左右箭头点击事件
Banner.prototype.listenArrowClick = function () {
    var self = this;
    self.leftArrow.click(function () {
        if(self.index === 0){
            // ==：1 == '1'：true
            // ==== 1 != '1'
            self.bannerUl.css({"left":-self.bannerCount*self.bannerWidth});
            self.index = self.bannerCount - 1;
        }else{
            self.index--;
        }
        self.animate();
    });

    self.rightArrow.click(function () {
        if(self.index === self.bannerCount + 1){
            self.bannerUl.css({"left":-self.bannerWidth});
            self.index = 2;//index表示下一次需要轮播的图片下标
        }else{
            self.index++;
        }
        self.animate();
    });
};

//展示、隐藏左右箭头
Banner.prototype.toggleArrow = function (isShow) {
    var self = this;
    if(isShow){
        self.leftArrow.show();//展示
        self.rightArrow.show();
    }else{
        self.leftArrow.hide();//隐藏
        self.rightArrow.hide();
    }
};


/**
 * 查看更多按钮
 */
function Index() {
    var self = this;
    self.page = 2;
    self.category_id = 0;
    self.loadBtn = $("#load-more-btn");
    // console.log("idnex====================")
}

/**
 * 监听查看更多按钮点击事件
 */
Index.prototype.listenLoadMoreEvent = function () {
    var self = this;
    var loadBtn = $("#load-more-btn");
    loadBtn.click(function () {
        myajax.get({
            'url': '/goods/list/',
            'data':{
                'p': self.page,
                'category_id': self.category_id
            },
            'success': function (result) {
                if(result['code'] === 200){
                    // console.log(result['data'])
                    var goods = result['data'];
                    if(goods.length > 0){
                        var tpl = template("news-item",{"goods":goods});//将数据传递给模板
                        var ul = $(".list-inner-group");
                        ul.append(tpl);
                        self.page += 1;
                    }else{
                        loadBtn.hide();
                    }
                }
            }
        });
    });
};
/**
 * 分类点击事件
 */
Index.prototype.listenCategorySwitchEvent = function () {
    var self = this;
    var tabGroup = $(".list-tab");
    tabGroup.children().click(function () {
        // this：代表当前选中的这个li标签
        var li = $(this);
        var category_id = li.attr("data-category");
        var page = 1;
        myajax.get({
            'url': '/goods/list/',
            'data': {
                'category_id': category_id,
                'p': page
            },
            'success': function (result) {
                if(result['code'] === 200){
                    var goods = result['data'];
                    var tpl = template("news-item",{"goods":goods});
                    // empty：可以将这个标签下的所有子元素都删掉
                    var newsListGroup = $(".list-inner-group");
                    newsListGroup.empty();
                    newsListGroup.append(tpl);//拼接在ul上
                    self.page = 2;
                    self.category_id = category_id;
                    li.addClass('active').siblings().removeClass('active');
                    self.loadBtn.show();
                }
            }
        });
    });
};



Index.prototype.run = function () {
    var self = this;
    self.listenLoadMoreEvent();
    self.listenCategorySwitchEvent();
};

/**
 * 运行方法
 */
Banner.prototype.run = function () {
    this.initBanner();
    this.initPageControl();
    this.loop();
    this.listenPageControl()
    this.listenBannerHover();
    this.listenArrowClick();
};

//整个文档所有元素都加载完毕，再执行此代码
$(function () {
    var banner = new Banner();
    banner.run();

    var index = new Index();
    index.run();
});