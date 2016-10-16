
// log
var log = function () {
    console.log(arguments);
};

// long time ago
    var longTimeAgo = function(timeStamp) {
      var timeAgo = function(time, ago) {
        return Math.round(time) + ago;
      };
      log('开始处理时间');
      $(timeStamp).each(function(i, e){
        var past = parseInt(e.dataset.time);
        var now = Math.round(new Date().getTime() / 1000);
        var seconds = now - past;
        var ago = seconds / 60;
        // log('time ago', e, past, now, ago);
        var oneHour = 60;
        var oneDay = oneHour * 24;
        // var oneWeek = oneDay * 7;
        var oneMonth = oneDay * 30;
        var oneYear = oneMonth * 12;
        var s = '';
        if(seconds < 60) {
            s = timeAgo(seconds, '秒前')
        } else if (ago < oneHour) {
            s = timeAgo(ago, '分钟前');
        } else if (ago < oneDay) {
            s = timeAgo(ago/oneHour, '小时前');
        } else if (ago < oneMonth) {
            s = timeAgo(ago / oneDay, '天前');
        } else if (ago < oneYear) {
            s = timeAgo(ago / oneMonth, '月前');
        }
        $(e).text(s);
      });
    };

// form 可以对一类的值进行处理与获取
var formFromKeys = function(keys, prefix) {
    var form = {};
    for(var i = 0; i < keys.length; i++) {
        var key = keys[i];
        var tagid = prefix + key;
        var value = $('#' + tagid).val();
        if (value.length < 1) {
            // alert('字段不能为空');
            break;
        }
        $('#' + tagid).val('');
        form[key] = value;
    }
    return form;
};

// weibo API
var weibo = {};

var tweetForm = function () {
    var keys = [
        'content',
    ];
    var tweetPrefix = 'id-textarea-';
    var form = formFromKeys(keys, tweetPrefix);
    return form;
};

var tweet_add = function () {
    var form = tweetForm();
    var success = function (r) {
        log('r, ', r);
        if (r.success){
            log(r.message);
            var addContent = (`
                        <div class="pp-panel pp-flex-row" data-id="${r.data.id}">
                            <div class="pp-avatar pp-avatar-config">
                                <img class="pp-avatar-me" src="/static/img/head-min.jpg">
                            </div>
                            <div class="pp-main flex-1">
                                <div class="pp-main-header">
                                    <strong class="pp-full-name">${r.data.username}</strong>
                                    <span class="pp-timestamp" data-time=${r.data.created_time}></span>
                                </div>
                                <div class="pp-main-content">
                                    <p class="pp-weibo-text">${r.data.content}</p>
                                </div>
                               <!-- <div class="pp-main-pic">
                                    <img class="pp-weibo-pic" src="/static/img/main-pic.jpg">
                                </div> -->
                                <div class="pp-main-footer">
                                    <a class="btn icon-share-alt" title="转发"> 0</a>
                                    <a class="btn icon-comment" title="评论"> 0</a>
                                    <a class="btn icon-thumbs-up" title="赞"> 0</a>
                                    <a class="btn icon-cog" title="设置"></a>
                                </div>
                            </div>
                        </div>
                                `);
            var insertPlace = $('#id-div-insert');
            insertPlace.prepend(addContent);
        }else {
            alert('发布失败');
        }
    };
    var error = function (err) {
        log('reg, ', err);
    };
    weibo.tweet_add(form, success, error);
};

weibo.post = function(url, form, success, error) {
    var data = JSON.stringify(form);
    var request = {
        url: url,
        type: 'post',
        contentType: 'application/json',
        data: data,
        success: function (r) {
            log('post success', url, r);
            success(r);
        },
        error: function (err) {
            log('post err', url, err);
            error(err);
        }
    };
    $.ajax(request);
};

weibo.register = function(form, success, error) {
    var url = '/register';
    this.post(url, form, success, error);
};

weibo.login = function(form, success, error) {
    var url = '/login';
    this.post(url, form, success, error);
};

weibo.tweet_add = function (form, success, error) {
    var url = '/tweet/add';
    this.post(url, form, success, error);
};