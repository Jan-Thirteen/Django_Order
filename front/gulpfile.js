var gulp = require("gulp");
var cssnano = require("gulp-cssnano");
var rename = require("gulp-rename");
var uglify = require("gulp-uglify");
var concat = require("gulp-concat");
var cache = require('gulp-cache');
var htmlmin = require('gulp-htmlmin')
// var imagemin = require('gulp-imagemin');
var bs = require('browser-sync').create();
const sass = require('gulp-sass')(require('sass'));
// // gulp-util：这个插件中有一个方法log，可以打印出当前js错误的信息
var util = require("gulp-util");
var sourcemaps = require("gulp-sourcemaps");
//gulp-sourcemaps当js文件报错，在console根据原js文件打印信息

var webserver = require('gulp-webserver');

var path = {  //保存静态文件的路径
    'html': './templates/**/',
    'css': './src/css/**/',
    'js': './src/js/',
    'images': './src/images/',
    'html_dist': './dist/html/',
    'css_dist': './dist/css/',
    'js_dist': './dist/js/',
    'images_dist': './dist/images/'
};

// 处理html文件的任务
const html = function () {
    return gulp
        .src(path.html + '*.html')
        .pipe(htmlmin({
            collapseWhitespace: true,   //移除空格
            removeEmptyAttributes:true, //移除空属性，仅限于原生属性
            collapseBooleanAttributes:true,         //移除checked类似的布尔值属性
            removeAttributeQuotes:true, //移除属性上的双引号
            minifyCSS: true,            //压缩内嵌式css代码（只能基本压缩，不能添加前缀）
            minifyJS: true,             //压缩内嵌式js代码（只能基本压缩，不能进行转码）
            removeStyleLinkTypeAttributes: true,    //移除style和link标签上的type
        }))
        .pipe(gulp.dest(path.html_dist))
        .pipe(bs.stream())
}
module.exports.html = html

// 定义一个css的任务
const css = function () {
    return gulp
        .src(path.css + '*.scss')
        .pipe(sass())
        .pipe(cssnano())
        .pipe(rename({"suffix":".min"}))
        .pipe(gulp.dest(path.css_dist))
        .pipe(bs.stream())
}
module.exports.css = css

// 定义处理js文件的任务
const js = function () {
    return gulp
        .src(path.js + '*.js')
        .pipe(sourcemaps.init())
        .pipe(uglify().on('error',util.log))
        .pipe(rename({"suffix":".min"}))
        .pipe(sourcemaps.write())
        .pipe(gulp.dest(path.js_dist))
        .pipe(bs.stream())
}
module.exports.js = js

// 定义处理图片文件的任务
const images = function () {
    return gulp
        .src(path.images + '*.*')
        // .pipe(cache(imagemin()))
        .pipe(gulp.dest(path.images_dist))
        .pipe(bs.stream())
}
module.exports.images = images

// 定义监听文件修改的任务
const watch = function () {
    gulp.watch(path.css + '*.scss',css)
    gulp.watch(path.html + '*.html',html);
    gulp.watch(path.js + '*.js',js);
    gulp.watch(path.images + '*.*',images);
}
module.exports.watch = watch

//初始化browser-sync的任务
const bst = function () {
    bs.init({
        'server': {
            'baseDir': './'
        }
    });
}
module.exports.bst = bst

gulp.task('bs',function(){
  return gulp
  	.src('./dist')
    .pipe(webserver({
    	host:'localhost',//域名，可以自定义
    	port:'8000',//端口
    	livereload:true,//当文件被修改，是否自动刷新
    	open:'html/news/index.html'//默认打开哪一个文件，从./dist后书写
  }))
})

// 创建一个默认的任务
// gulp.task("default",gulp.series(watch));
// module.exports.default = gulp.series('bs',watch)
module.exports.default = gulp.series(watch)